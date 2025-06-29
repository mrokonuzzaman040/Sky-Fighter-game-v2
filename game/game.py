import pygame
import sys
import random
import math
from pygame.locals import *

from game.player import Player
from game.enemy import Enemy, EnemyBullet
from game.cloud import Cloud
from game.bullet import Bullet
from game.boss import Boss, BossBullet
from game.powerup import PowerUp, PowerUpManager

class Game:
    def __init__(self, difficulty="normal", multiplayer=False, client=None):
        self.difficulty = difficulty
        self.width = 800
        self.height = 600
        self.multiplayer = multiplayer
        self.client = client
        self.player_id = 0  # Will be set by server in multiplayer mode
        
        # Set up display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sky Warr - In Game")
        
        # Set up clock
        self.clock = pygame.time.Clock()
        
        # Load assets
        self.load_assets()
        
        # Game state
        self.running = True
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        
        # Level system
        self.enemies_killed_this_level = 0
        self.enemies_needed_for_next_level = 10
        self.boss_active = False
        self.boss_defeated = False
        
        # Power-up system
        self.powerup_manager = PowerUpManager()
        self.powerup_message = ""
        self.powerup_message_time = 0
        
        # Set initial game difficulty settings (before player creation)
        self.set_game_difficulty(difficulty)
        
        # Initialize game objects
        self.init_game_objects()
        
        # Set player-specific difficulty settings (after player creation)
        self.set_player_difficulty(difficulty)
        
        # Multiplayer initialization if needed
        if self.multiplayer and self.client:
            self.init_multiplayer()
    
    def init_multiplayer(self):
        """Initialize multiplayer-specific components"""
        # Get player ID from server
        self.player_id = self.client.get_player_id()
        
        # Create the remote player object
        self.remote_player = Player(self.width // 2, self.height - 100)
        if self.player_id == 1:
            # If we're player 1, remote player should be positioned differently
            self.remote_player.rect.y = 100  # Position at top
            self.remote_player.image.fill((255, 0, 0, 0))  # Mark with different color
            pygame.draw.polygon(self.remote_player.image, (255, 0, 0), 
                             [(0, 0), (25, 40), (50, 0)])  # Flip orientation
    
    def load_assets(self):
        """Load game assets like images and sounds"""
        # Background
        try:
            self.background = pygame.image.load("assets/images/sky_bg.jpg").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except:
            self.background = None
            
        # Load fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load sounds
        pygame.mixer.init()
        try:
            self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.mp3")
            self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.mp3")
        except:
            self.shoot_sound = None
            self.explosion_sound = None
    
    def init_game_objects(self):
        """Initialize game objects"""
        # Create the player
        self.player = Player(self.width // 2, self.height - 100)
        
        # Create enemy group
        self.enemies = pygame.sprite.Group()
        self.spawn_enemies(5)
        
        # Create cloud group (decorative)
        self.clouds = pygame.sprite.Group()
        self.spawn_clouds(10)
        
        # Create bullet groups
        self.bullets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        # Boss
        self.boss = None
        
        # Power-ups
        self.powerups = pygame.sprite.Group()
    
    def set_game_difficulty(self, difficulty):
        """Set game-level difficulty parameters"""
        if difficulty == "easy":
            self.enemy_speed = 2
            self.enemy_spawn_rate = 60  # frames
            self.powerup_manager.spawn_chance = 0.008
        elif difficulty == "normal":
            self.enemy_speed = 3
            self.enemy_spawn_rate = 45  # frames
            self.powerup_manager.spawn_chance = 0.005
        elif difficulty == "hard":
            self.enemy_speed = 5
            self.enemy_spawn_rate = 30  # frames
            self.powerup_manager.spawn_chance = 0.003
    
    def set_player_difficulty(self, difficulty):
        """Set player-specific difficulty parameters"""
        if difficulty == "easy":
            self.player.max_health = 5
            self.player.health = 5
        elif difficulty == "normal":
            self.player.max_health = 3
            self.player.health = 3
        elif difficulty == "hard":
            self.player.max_health = 2
            self.player.health = 2
    
    
    def spawn_enemies(self, count):
        """Spawn a number of enemies"""
        # Reduce enemies in multiplayer mode
        if self.multiplayer:
            count = max(1, count // 2)
        
        # Don't spawn enemies during boss fight
        if self.boss_active:
            return
        
        for _ in range(count):
            # Choose enemy type based on level
            if self.level <= 2:
                enemy_types = ["fighter"] * 4 + ["interceptor"]  # Mostly fighters
            elif self.level <= 5:
                enemy_types = ["fighter"] * 2 + ["interceptor"] * 2 + ["bomber"]  # Mixed
            else:
                enemy_types = ["fighter", "interceptor"] * 2 + ["bomber"] * 2  # More dangerous
            
            enemy_type = random.choice(enemy_types)
            enemy = Enemy(random.randint(50, self.width - 50), 
                         random.randint(-300, 0),
                         self.enemy_speed, enemy_type)
            self.enemies.add(enemy)
    
    def spawn_clouds(self, count):
        """Spawn decorative clouds"""
        for _ in range(count):
            cloud = Cloud(random.randint(0, self.width), 
                         random.randint(0, self.height))
            self.clouds.add(cloud)
    
    def spawn_boss(self):
        """Spawn a boss based on current level"""
        if self.boss_active or self.boss:
            return
            
        # Determine boss type based on level
        if self.level <= 3:
            boss_type = "basic"
        elif self.level <= 7:
            boss_type = "advanced"
        else:
            boss_type = "final"
        
        self.boss = Boss(self.width // 2, -100, boss_type)
        self.boss_active = True
        self.boss_defeated = False
        
        # Clear existing enemies for boss fight
        self.enemies.empty()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                if self.multiplayer and self.client:
                    self.client.disconnect()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    if self.multiplayer and self.client:
                        self.client.disconnect()
                elif event.key == K_p:
                    self.paused = not self.paused
                elif event.key == K_SPACE and not self.game_over and not self.paused:
                    self.handle_shooting()
                elif event.key == K_r and self.game_over:
                    # Restart game (single player only)
                    if not self.multiplayer:
                        self.restart_game()
    
    def handle_shooting(self):
        """Handle player shooting with power-ups"""
        rapid_fire = self.powerup_manager.is_active("rapid_fire")
        triple_shot = self.powerup_manager.is_active("triple_shot")
        
        if self.player.can_shoot(rapid_fire):
            positions = self.player.get_bullet_positions(triple_shot)
            
            for pos in positions:
                bullet = Bullet(pos[0], pos[1])
                self.bullets.add(bullet)
            
            if self.shoot_sound:
                self.shoot_sound.play()
            
            # Send bullet fire event in multiplayer
            if self.multiplayer and self.client:
                self.client.send_bullet()
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
            
        # Update power-ups
        self.powerup_manager.update_powerups(self.player)
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.width)
        
        # In multiplayer, send our position and get remote player's position
        if self.multiplayer and self.client:
            # Send our position
            self.client.send_position(self.player.rect.centerx, self.player.rect.centery)
            
            # Get remote player position
            remote_x, remote_y = self.client.get_remote_position()
            if remote_x and remote_y:  # Only update if we got valid coordinates
                self.remote_player.rect.centerx = remote_x
                self.remote_player.rect.centery = remote_y
            
            # Process any remote bullets
            remote_bullets = self.client.get_remote_bullets()
            for bullet_pos in remote_bullets:
                bullet = Bullet(bullet_pos[0], bullet_pos[1])
                # Adjust bullet direction for player 2
                if self.player_id == 1:
                    bullet.speed = -bullet.speed
                self.bullets.add(bullet)
        
        # Update enemies
        self.enemies.update(self.height)
        
        # Enemy shooting - limit total enemy bullets on screen
        max_enemy_bullets = 15  # Maximum enemy bullets allowed on screen
        current_enemy_bullets = len(self.enemy_bullets)
        
        for enemy in self.enemies:
            if enemy.can_fire() and current_enemy_bullets < max_enemy_bullets:
                patterns = enemy.get_bullet_patterns((self.player.rect.centerx, self.player.rect.centery))
                for pattern in patterns:
                    if current_enemy_bullets < max_enemy_bullets:
                        enemy_bullet = EnemyBullet(
                            pattern['x'], 
                            pattern['y'], 
                            pattern['direction'], 
                            pattern['speed'],
                            enemy  # Pass enemy as owner
                        )
                        self.enemy_bullets.add(enemy_bullet)
                        enemy.bullets.add(enemy_bullet)  # Track bullet in enemy's group
                        current_enemy_bullets += 1
        
        # Update boss
        if self.boss:
            self.boss.update(self.width, self.height, self.player)
            
            # Boss shooting
            if self.boss.can_fire():
                positions = self.boss.get_bullet_positions()
                for pos in positions:
                    boss_bullet = BossBullet(pos[0], pos[1])
                    self.boss_bullets.add(boss_bullet)
        
        # Update bullets
        self.bullets.update()
        self.boss_bullets.update()
        self.enemy_bullets.update()
        
        # Update clouds
        self.clouds.update()
        
        # Update power-ups
        self.powerups.update()
        
        # Check collisions
        self.check_collisions()
        
        # Spawn new enemies (not during boss fight)
        if not self.boss_active:
            if len(self.enemies) < 5 + self.level and random.randint(0, self.enemy_spawn_rate) == 0:
                self.spawn_enemies(1)
        
        # Spawn new clouds
        if len(self.clouds) < 10 and random.randint(0, 100) == 0:
            self.spawn_clouds(1)
        
        # Spawn power-ups
        if self.powerup_manager.should_spawn_powerup():
            powerup_type = self.powerup_manager.get_random_powerup_type()
            powerup = PowerUp(random.randint(50, self.width - 50), -50, powerup_type)
            self.powerups.add(powerup)
        
        # Check for level progression
        self.check_level_progression()
        
        # Update power-up message timer
        if self.powerup_message_time > 0:
            self.powerup_message_time -= 1
    
    def check_collisions(self):
        """Check all collision types"""
        # Bullet/enemy collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for bullet, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                # Clean up enemy's bullets when enemy dies
                enemy.destroy_bullets()
                # Remove enemy bullets from main group
                for enemy_bullet in list(self.enemy_bullets):
                    if enemy_bullet.owner == enemy:
                        enemy_bullet.kill()
                
                score_gain = 10 * self.powerup_manager.get_score_multiplier()
                self.score += score_gain
                self.enemies_killed_this_level += 1
                self.player.add_experience(5)
                
                if self.explosion_sound:
                    self.explosion_sound.play()
        
        # Bullet/boss collisions
        if self.boss:
            boss_hits = pygame.sprite.spritecollide(self.boss, self.bullets, True)
            for hit in boss_hits:
                if self.boss.take_damage():
                    # Boss defeated
                    score_gain = self.boss.score_value * self.powerup_manager.get_score_multiplier()
                    self.score += score_gain
                    self.player.add_experience(50)
                    self.boss_defeated = True
                    self.boss_active = False
                    self.boss = None
                    
                    if self.explosion_sound:
                        self.explosion_sound.play()
        
        # Player/enemy collisions
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            has_shield = self.powerup_manager.has_shield()
            if self.player.take_damage(1, has_shield):
                self.game_over = True
                if self.multiplayer and self.client:
                    self.client.send_game_over()
            elif not has_shield and self.explosion_sound:
                self.explosion_sound.play()
        
        # Player/boss bullet collisions
        if pygame.sprite.spritecollide(self.player, self.boss_bullets, True):
            has_shield = self.powerup_manager.has_shield()
            damage = self.boss.damage if self.boss else 2
            if self.player.take_damage(damage, has_shield):
                self.game_over = True
            elif not has_shield and self.explosion_sound:
                self.explosion_sound.play()
        
        # Player/enemy bullet collisions
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            has_shield = self.powerup_manager.has_shield()
            if self.player.take_damage(1, has_shield):
                self.game_over = True
            elif not has_shield and self.explosion_sound:
                self.explosion_sound.play()
        
        # Player/boss collisions
        if self.boss and pygame.sprite.collide_rect(self.player, self.boss):
            has_shield = self.powerup_manager.has_shield()
            if self.player.take_damage(3, has_shield):
                self.game_over = True
            elif not has_shield and self.explosion_sound:
                self.explosion_sound.play()
        
        # Player/power-up collisions
        collected_powerups = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in collected_powerups:
            message = self.powerup_manager.apply_powerup(self.player, powerup.powerup_type)
            self.powerup_message = message
            self.powerup_message_time = 120  # 2 seconds at 60 FPS
        
        # In multiplayer, check if remote player is hit
        if self.multiplayer:
            if pygame.sprite.spritecollide(self.remote_player, self.enemies, True):
                # Let the server handle remote player health
                pass
    
    def check_level_progression(self):
        """Check if player should advance to next level"""
        if not self.boss_active and self.enemies_killed_this_level >= self.enemies_needed_for_next_level:
            # Time for boss fight
            self.spawn_boss()
        elif self.boss_defeated:
            # Boss defeated, advance to next level
            self.level += 1
            self.enemies_killed_this_level = 0
            self.enemies_needed_for_next_level += 5  # Increase enemies needed
            self.enemy_speed += 0.3  # Increase enemy speed
            self.boss_defeated = False
    
    def restart_game(self):
        """Restart the game"""
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.enemies_killed_this_level = 0
        self.enemies_needed_for_next_level = 10
        self.boss_active = False
        self.boss_defeated = False
        self.boss = None
        
        # Reset power-ups
        self.powerup_manager = PowerUpManager()
        self.powerup_message = ""
        self.powerup_message_time = 0
        
        # Reinitialize game objects (this creates new player)
        self.init_game_objects()
        self.set_player_difficulty(self.difficulty)
        
        # Reset player stats to defaults (since we just created a new player)
        self.player.reset_to_defaults()
    
    def render(self):
        """Render the game"""
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((135, 206, 235))  # Sky blue
        
        # Draw clouds
        self.clouds.draw(self.screen)
        
        # Draw power-ups
        self.powerups.draw(self.screen)
        
        # Draw bullets
        self.bullets.draw(self.screen)
        self.boss_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        
        # Draw enemies
        self.enemies.draw(self.screen)
        
        # Draw boss
        if self.boss:
            self.screen.blit(self.boss.image, self.boss.rect)
            # Draw boss health bar
            self.draw_boss_health_bar()
        
        # Draw player
        self.screen.blit(self.player.image, self.player.rect)
        
        # Draw shield effect if active
        if self.powerup_manager.has_shield():
            self.draw_shield_effect()
        
        # Draw remote player in multiplayer mode
        if self.multiplayer:
            self.screen.blit(self.remote_player.image, self.remote_player.rect)
        
        # Draw UI
        self.draw_ui()
        
        # Draw pause screen
        if self.paused:
            self.draw_pause_screen()
        
        # Draw game over
        if self.game_over:
            self.draw_game_over_screen()
        
        # Update display
        pygame.display.flip()
    
    def draw_boss_health_bar(self):
        """Draw boss health bar"""
        if not self.boss:
            return
            
        bar_width = 400
        bar_height = 20
        bar_x = (self.width - bar_width) // 2
        bar_y = 50
        
        # Background
        pygame.draw.rect(self.screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_pct = self.boss.get_health_percentage()
        pygame.draw.rect(self.screen, (255, 0, 0), 
                       (bar_x, bar_y, bar_width * health_pct, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Label
        boss_text = self.font.render(f"BOSS - {self.boss.boss_type.upper()}", True, (255, 255, 255))
        text_rect = boss_text.get_rect(center=(self.width//2, bar_y - 15))
        self.screen.blit(boss_text, text_rect)
    
    def draw_shield_effect(self):
        """Draw shield effect around player"""
        center = (self.player.rect.centerx, self.player.rect.centery)
        radius = 40
        pygame.draw.circle(self.screen, (0, 191, 255, 100), center, radius, 3)
        pygame.draw.circle(self.screen, (173, 216, 230, 50), center, radius - 10, 2)
    
    def draw_ui(self):
        """Draw the user interface"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Level
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 50))
        
        # Player level
        player_level = getattr(self.player, 'player_level', 1)  # Default to 1 if attribute missing
        player_level_text = self.small_font.render(f"Player Lv: {player_level}", True, (255, 255, 255))
        self.screen.blit(player_level_text, (10, 90))
        
        # Progress to next level
        if not self.boss_active:
            progress_text = self.small_font.render(
                f"Enemies: {self.enemies_killed_this_level}/{self.enemies_needed_for_next_level}", 
                True, (255, 255, 255)
            )
            self.screen.blit(progress_text, (10, 110))
        
        # Draw player indicator in multiplayer
        if self.multiplayer:
            player_text = self.font.render(f"You are Player {self.player_id + 1}", True, (255, 255, 255))
            self.screen.blit(player_text, (10, 130))
        
        # Draw health bar
        self.draw_health_bar()
        
        # Draw experience bar
        self.draw_experience_bar()
        
        # Draw active power-ups
        self.draw_active_powerups()
        
        # Draw power-up message
        if self.powerup_message_time > 0:
            message_text = self.font.render(self.powerup_message, True, (255, 255, 0))
            text_rect = message_text.get_rect(center=(self.width//2, self.height//2 - 100))
            self.screen.blit(message_text, text_rect)
    
    def draw_health_bar(self):
        """Draw player health bar"""
        health_pct = self.player.health / self.player.max_health
        bar_width = 100
        bar_height = 20
        bar_x = self.width - bar_width - 10
        bar_y = 10
        
        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), 
                       (bar_x, bar_y, bar_width * health_pct, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Health text
        health_text = self.small_font.render(f"HP: {self.player.health}/{self.player.max_health}", 
                                           True, (255, 255, 255))
        self.screen.blit(health_text, (bar_x, bar_y + 25))
    
    def draw_experience_bar(self):
        """Draw player experience bar"""
        exp_pct = getattr(self.player, 'get_level_progress', lambda: 0)()
        if callable(exp_pct):
            exp_pct = 0  # Fallback if method doesn't exist
            
        bar_width = 100
        bar_height = 10
        bar_x = self.width - bar_width - 10
        bar_y = 60
        
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 0, 255), 
                       (bar_x, bar_y, bar_width * exp_pct, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Experience text
        exp_text = self.small_font.render(f"EXP: {int(exp_pct * 100)}%", True, (255, 255, 255))
        self.screen.blit(exp_text, (bar_x, bar_y + 15))
    
    def draw_active_powerups(self):
        """Draw active power-ups indicators"""
        y_offset = 100
        for powerup_type in ["rapid_fire", "triple_shot", "shield", "speed_boost", "double_score"]:
            if self.powerup_manager.is_active(powerup_type):
                remaining = self.powerup_manager.get_remaining_time(powerup_type)
                text = self.small_font.render(f"{powerup_type.replace('_', ' ').title()}: {remaining:.1f}s", 
                                            True, (255, 255, 0))
                self.screen.blit(text, (self.width - 200, y_offset))
                y_offset += 20
    
    def draw_pause_screen(self):
        """Draw pause overlay"""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(pause_text, text_rect)
        
        continue_text = self.font.render("Press P to continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(self.width//2, self.height//2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game_over_screen(self):
        """Draw game over screen"""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level Reached: {self.level}", True, (255, 255, 255))
        player_level = getattr(self.player, 'player_level', 1)  # Default to 1 if attribute missing
        player_level_text = self.font.render(f"Player Level: {player_level}", True, (255, 255, 255))
        
        if self.multiplayer:
            restart_text = self.font.render("Press ESC to exit", True, (255, 255, 255))
        else:
            restart_text = self.font.render("Press R to restart or ESC to exit", True, (255, 255, 255))
        
        # Center all text
        game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 60))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2 - 20))
        level_rect = level_text.get_rect(center=(self.width//2, self.height//2 + 10))
        player_level_rect = player_level_text.get_rect(center=(self.width//2, self.height//2 + 40))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 80))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(player_level_text, player_level_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()

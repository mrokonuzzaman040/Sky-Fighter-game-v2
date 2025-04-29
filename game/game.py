import pygame
import sys
import random
from pygame.locals import *

from game.player import Player
from game.enemy import Enemy
from game.cloud import Cloud
from game.bullet import Bullet

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
        
        # Load sounds
        pygame.mixer.init()
        try:
            self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
            self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
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
        
        # Create bullet group
        self.bullets = pygame.sprite.Group()
    
    def set_game_difficulty(self, difficulty):
        """Set game-level difficulty parameters"""
        if difficulty == "easy":
            self.enemy_speed = 2
            self.enemy_spawn_rate = 60  # frames
        elif difficulty == "normal":
            self.enemy_speed = 3
            self.enemy_spawn_rate = 45  # frames
        elif difficulty == "hard":
            self.enemy_speed = 5
            self.enemy_spawn_rate = 30  # frames
    
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
            
        for _ in range(count):
            enemy = Enemy(random.randint(50, self.width - 50), 
                         random.randint(-300, 0),
                         self.enemy_speed)
            self.enemies.add(enemy)
    
    def spawn_clouds(self, count):
        """Spawn decorative clouds"""
        for _ in range(count):
            cloud = Cloud(random.randint(0, self.width), 
                         random.randint(0, self.height))
            self.clouds.add(cloud)
    
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
                elif event.key == K_SPACE and not self.game_over:
                    # Fire bullet
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                    self.bullets.add(bullet)
                    if self.shoot_sound:
                        self.shoot_sound.play()
                    
                    # Send bullet fire event in multiplayer
                    if self.multiplayer and self.client:
                        self.client.send_bullet()
                        
                elif event.key == K_r and self.game_over:
                    # Restart game (single player only)
                    if not self.multiplayer:
                        self.init_game_objects()
                        self.score = 0
                        self.game_over = False
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
            
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
        
        # Update bullets
        self.bullets.update()
        
        # Update clouds
        self.clouds.update()
        
        # Check for bullet/enemy collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for bullet, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                self.score += 10
                if self.explosion_sound:
                    self.explosion_sound.play()
        
        # Check for player/enemy collisions
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            self.player.health -= 1
            if self.explosion_sound:
                self.explosion_sound.play()
            
            if self.player.health <= 0:
                self.game_over = True
                if self.multiplayer and self.client:
                    self.client.send_game_over()
        
        # In multiplayer, check if remote player is hit
        if self.multiplayer:
            if pygame.sprite.spritecollide(self.remote_player, self.enemies, True):
                # Let the server handle remote player health
                pass
        
        # Spawn new enemies
        if len(self.enemies) < 5 + self.level and random.randint(0, self.enemy_spawn_rate) == 0:
            self.spawn_enemies(1)
        
        # Spawn new clouds
        if len(self.clouds) < 10 and random.randint(0, 100) == 0:
            self.spawn_clouds(1)
        
        # Level up every 200 points
        if self.score > 0 and self.score // 200 > self.level - 1:
            self.level += 1
            self.enemy_speed += 0.5
    
    def render(self):
        """Render the game"""
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((135, 206, 235))  # Sky blue
        
        # Draw clouds
        self.clouds.draw(self.screen)
        
        # Draw bullets
        self.bullets.draw(self.screen)
        
        # Draw enemies
        self.enemies.draw(self.screen)
        
        # Draw player
        self.screen.blit(self.player.image, self.player.rect)
        
        # Draw remote player in multiplayer mode
        if self.multiplayer:
            self.screen.blit(self.remote_player.image, self.remote_player.rect)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 50))
        
        # Draw player indicator in multiplayer
        if self.multiplayer:
            player_text = self.font.render(f"You are Player {self.player_id + 1}", True, (255, 255, 255))
            self.screen.blit(player_text, (10, 90))
        
        # Draw health bar
        health_pct = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, (255, 0, 0), (self.width - 110, 10, 100, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), 
                       (self.width - 110, 10, 100 * health_pct, 20))
        
        # Draw game over
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, (255, 0, 0))
            
            if self.multiplayer:
                restart_text = self.font.render("Press ESC to exit", True, (255, 255, 255))
            else:
                restart_text = self.font.render("Press R to restart", True, (255, 255, 255))
            
            text_rect = game_over_text.get_rect(center=(self.width//2, self.height//2))
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
            
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()

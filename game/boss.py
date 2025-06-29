import pygame
import random
import math

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, boss_type="basic"):
        super().__init__()
        
        self.boss_type = boss_type
        self.setup_boss_stats()
        
        # Load boss image based on type
        self.create_boss_image()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        
        # Movement patterns
        self.original_x = x
        self.movement_time = 0
        self.last_shot = 0
        self.shot_cooldown = self.fire_rate
        
        # States
        self.entering = True
        self.target_y = 100
        
    def setup_boss_stats(self):
        """Setup boss statistics based on type"""
        if self.boss_type == "basic":
            self.max_health = 50
            self.health = 50
            self.speed = 2
            self.fire_rate = 1500  # 1.5 seconds between shots
            self.damage = 2
            self.score_value = 500
            self.size = (120, 100)
        elif self.boss_type == "advanced":
            self.max_health = 100
            self.health = 100
            self.speed = 3
            self.fire_rate = 1200  # 1.2 seconds between shots
            self.damage = 3
            self.score_value = 1000
            self.size = (150, 120)
        elif self.boss_type == "final":
            self.max_health = 200
            self.health = 200
            self.speed = 4
            self.fire_rate = 1000  # 1 second between shots (more aggressive)
            self.damage = 4
            self.score_value = 2000
            self.size = (180, 150)
    
    def create_boss_image(self):
        """Create boss image based on type"""
        try:
            # Try to load a boss image (you can add different boss images later)
            self.image = pygame.image.load(f"assets/images/boss_{self.boss_type}.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)
        except:
            # Create a default boss aircraft based on type
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            
            if self.boss_type == "basic":
                self.create_heavy_fighter()
            elif self.boss_type == "advanced":
                self.create_bomber_boss()
            elif self.boss_type == "final":
                self.create_mothership()
    
    def create_heavy_fighter(self):
        """Create a heavy fighter boss (basic)"""
        # Main fuselage (dark red)
        pygame.draw.ellipse(self.image, (150, 20, 20), (40, 15, 40, 70))
        
        # Large wings
        pygame.draw.polygon(self.image, (120, 15, 15), [
            (10, 40), (110, 40), (100, 55), (20, 55)
        ])
        
        # Cockpit
        pygame.draw.ellipse(self.image, (100, 0, 0), (52, 20, 16, 20))
        
        # Wing mounted weapons
        pygame.draw.rect(self.image, (80, 80, 80), (8, 45, 12, 6))
        pygame.draw.rect(self.image, (80, 80, 80), (100, 45, 12, 6))
        
        # Engine exhausts
        pygame.draw.rect(self.image, (255, 100, 0), (50, 75, 8, 10))
        pygame.draw.rect(self.image, (255, 100, 0), (62, 75, 8, 10))
        
        # Armor plating details
        for i in range(3):
            pygame.draw.rect(self.image, (100, 10, 10), (45 + i*10, 25 + i*8, 8, 4))
    
    def create_bomber_boss(self):
        """Create a bomber boss (advanced)"""
        # Main fuselage (dark gray)
        pygame.draw.ellipse(self.image, (80, 80, 80), (50, 10, 50, 100))
        
        # Large bomber wings
        pygame.draw.polygon(self.image, (60, 60, 60), [
            (0, 50), (150, 50), (140, 70), (10, 70)
        ])
        
        # Multiple engine pods
        for x in [15, 45, 105, 135]:
            pygame.draw.ellipse(self.image, (40, 40, 40), (x, 75, 10, 25))
            pygame.draw.rect(self.image, (255, 150, 0), (x+1, 90, 8, 15))
        
        # Cockpit/command center
        pygame.draw.ellipse(self.image, (100, 120, 150), (62, 15, 26, 30))
        
        # Weapon turrets
        pygame.draw.circle(self.image, (120, 120, 120), (35, 60), 8)
        pygame.draw.circle(self.image, (120, 120, 120), (115, 60), 8)
        pygame.draw.circle(self.image, (100, 100, 100), (75, 85), 6)
        
        # Armor sections
        pygame.draw.rect(self.image, (100, 100, 100), (60, 45, 30, 8))
    
    def create_mothership(self):
        """Create a mothership boss (final)"""
        # Main hull (very dark red/black)
        pygame.draw.ellipse(self.image, (60, 10, 10), (30, 20, 120, 110))
        
        # Command tower
        pygame.draw.rect(self.image, (80, 15, 15), (70, 10, 40, 40))
        pygame.draw.ellipse(self.image, (150, 50, 50), (80, 15, 20, 15))
        
        # Massive wings with weapon hardpoints
        pygame.draw.polygon(self.image, (40, 8, 8), [
            (0, 60), (180, 60), (170, 90), (10, 90)
        ])
        
        # Multiple weapon systems
        weapon_positions = [(20, 70), (50, 65), (130, 65), (160, 70), (90, 75)]
        for x, y in weapon_positions:
            pygame.draw.circle(self.image, (100, 100, 100), (x, y), 6)
            pygame.draw.circle(self.image, (150, 150, 150), (x, y), 4)
        
        # Engine array
        engine_positions = [(40, 115), (60, 120), (80, 122), (100, 122), (120, 120), (140, 115)]
        for x, y in engine_positions:
            pygame.draw.ellipse(self.image, (255, 100, 0), (x, y, 8, 15))
            pygame.draw.ellipse(self.image, (255, 200, 100), (x+1, y+2, 6, 10))
        
        # Armor plating and details
        pygame.draw.rect(self.image, (80, 20, 20), (50, 50, 80, 12))
        pygame.draw.rect(self.image, (100, 30, 30), (60, 35, 60, 8))
        
        # Shield generators (glowing effects)
        for x in [45, 90, 135]:
            pygame.draw.circle(self.image, (0, 100, 255), (x, 45), 5)
            pygame.draw.circle(self.image, (100, 150, 255), (x, 45), 3)
    
    def update(self, screen_width, screen_height, target_player=None):
        """Update boss behavior"""
        self.movement_time += 1
        
        # Entry movement
        if self.entering:
            if self.rect.y < self.target_y:
                self.rect.y += self.speed
            else:
                self.entering = False
        else:
            # Movement patterns based on boss type
            if self.boss_type == "basic":
                # Simple side-to-side movement
                self.rect.x = self.original_x + math.sin(self.movement_time * 0.05) * 100
            elif self.boss_type == "advanced":
                # Figure-8 movement
                self.rect.x = self.original_x + math.sin(self.movement_time * 0.05) * 150
                self.rect.y = self.target_y + math.sin(self.movement_time * 0.1) * 30
            elif self.boss_type == "final":
                # Aggressive tracking movement
                if target_player:
                    if self.rect.centerx < target_player.rect.centerx:
                        self.rect.x += self.speed * 0.5
                    elif self.rect.centerx > target_player.rect.centerx:
                        self.rect.x -= self.speed * 0.5
                
                # Vertical bobbing
                self.rect.y = self.target_y + math.sin(self.movement_time * 0.08) * 20
        
        # Keep boss within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
    
    def can_fire(self):
        """Check if boss can fire with some randomness"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_cooldown:
            # Add some randomness to boss firing (80% chance to fire when ready)
            if random.random() < 0.8:
                self.last_shot = current_time
                return True
        return False
    
    def get_bullet_positions(self):
        """Get positions for boss bullets based on type"""
        if self.boss_type == "basic":
            # Single bullet from center
            return [(self.rect.centerx, self.rect.bottom)]
        elif self.boss_type == "advanced":
            # Three bullets spread
            return [
                (self.rect.centerx - 30, self.rect.bottom),
                (self.rect.centerx, self.rect.bottom),
                (self.rect.centerx + 30, self.rect.bottom)
            ]
        elif self.boss_type == "final":
            # Three bullets in spread pattern (reduced from 5 to avoid spam)
            return [
                (self.rect.centerx - 40, self.rect.bottom),
                (self.rect.centerx, self.rect.bottom),
                (self.rect.centerx + 40, self.rect.bottom)
            ]
    
    def take_damage(self, damage=1):
        """Boss takes damage"""
        self.health -= damage
        return self.health <= 0
    
    def get_health_percentage(self):
        """Get health as percentage for health bar"""
        return self.health / self.max_health
    
    def is_dead(self):
        """Check if boss is dead"""
        return self.health <= 0

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=(0, 1), speed=5):
        super().__init__()
        
        # Create boss bullet (larger and different color)
        self.image = pygame.Surface((8, 20))
        self.image.fill((255, 100, 100))  # Reddish color
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        
        self.speed = speed
        self.direction = direction
    
    def update(self):
        """Update boss bullet movement"""
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Remove bullet if it goes off screen
        if (self.rect.bottom < 0 or self.rect.top > 600 or 
            self.rect.right < 0 or self.rect.left > 800):
            self.kill()
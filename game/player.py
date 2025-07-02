import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Load player image
        try:
            self.image = pygame.image.load("assets/images/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 70))
        except:
            # Create a default player fighter jet if image can't be loaded
            self.image = pygame.Surface((60, 70), pygame.SRCALPHA)
            self.create_fighter_jet()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Player attributes
        self.speed = 7
        self.health = 3
        self.max_health = 3
        
        # Shooting mechanics
        self.last_shot = 0
        self.shot_cooldown = 250  # milliseconds between shots (normal fire rate)
        self.rapid_fire_cooldown = 100  # milliseconds for rapid fire
        
        # Power-up effects tracking
        self.powerup_effects = []
        
        # Experience and level system
        self.experience = 0
        self.player_level = 1
        self.experience_to_next_level = 100
    
    def create_fighter_jet(self):
        """Create a detailed fighter jet for the player"""
        # Main fuselage (blue)
        pygame.draw.ellipse(self.image, (0, 120, 200), (22, 10, 16, 50))
        
        # Wings (slightly darker blue)
        pygame.draw.polygon(self.image, (0, 100, 180), [
            (5, 25), (55, 25), (50, 35), (10, 35)
        ])
        
        # Cockpit (light blue/glass effect)
        pygame.draw.ellipse(self.image, (150, 200, 255), (26, 12, 8, 12))
        
        # Wing tips (missiles/fuel tanks)
        pygame.draw.ellipse(self.image, (100, 100, 100), (3, 27, 6, 8))
        pygame.draw.ellipse(self.image, (100, 100, 100), (51, 27, 6, 8))
        
        # Engine exhaust
        pygame.draw.rect(self.image, (255, 150, 0), (27, 52, 6, 8))
        
        # Tail fins
        pygame.draw.polygon(self.image, (0, 80, 160), [
            (25, 60), (35, 60), (32, 68), (28, 68)
        ])
        
        # Nose cone
        pygame.draw.polygon(self.image, (0, 140, 220), [
            (28, 10), (32, 10), (30, 5)
        ])
    
    def update(self, keys, screen_width, screen_height=600):
        # Move player based on key presses
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed
        if keys[K_UP] or keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_DOWN] or keys[K_s]:
            self.rect.y += self.speed
        
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < screen_height // 2:  # Don't go too high up
            self.rect.top = screen_height // 2
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    
    def can_shoot(self, rapid_fire_active=False):
        """Check if player can shoot based on cooldown"""
        current_time = pygame.time.get_ticks()
        cooldown = self.rapid_fire_cooldown if rapid_fire_active else self.shot_cooldown
        
        if current_time - self.last_shot > cooldown:
            self.last_shot = current_time
            return True
        return False
    
    def get_bullet_positions(self, triple_shot_active=False):
        """Get bullet spawn positions for different shot types"""
        if triple_shot_active:
            # Triple shot: center, left, and right
            return [
                (self.rect.centerx, self.rect.top),          # Center
                (self.rect.centerx - 25, self.rect.top + 10), # Left
                (self.rect.centerx + 25, self.rect.top + 10)  # Right
            ]
        else:
            # Normal single shot
            return [(self.rect.centerx, self.rect.top)]
    
    def take_damage(self, damage=1, has_shield=False):
        """Player takes damage, returns True if player died"""
        if has_shield:
            return False  # Shield blocks damage
        
        self.health -= damage
        return self.health <= 0
    
    def heal(self, amount=1):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)
    
    def add_experience(self, exp):
        """Add experience and check for level up"""
        self.experience += exp
        
        # Check for level up
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the player"""
        self.experience -= self.experience_to_next_level
        self.player_level += 1
        
        # Increase stats on level up
        if self.player_level % 3 == 0:  # Every 3 levels
            self.max_health += 1
            self.health = self.max_health  # Full heal on health increase
        
        if self.player_level % 2 == 0:  # Every 2 levels
            self.speed = min(self.speed + 0.5, 12)  # Cap speed at 12
        
        # Increase experience needed for next level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.2)
        
        return True  # Return True to indicate level up occurred
    
    def get_level_progress(self):
        """Get progress to next level as percentage"""
        return self.experience / self.experience_to_next_level
    
    def reset_to_defaults(self):
        """Reset player stats to default values (for game restart)"""
        self.health = 3
        self.max_health = 3
        self.speed = 7
        self.experience = 0
        self.player_level = 1
        self.experience_to_next_level = 100

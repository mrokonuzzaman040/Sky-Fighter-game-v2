import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, enemy_type="fighter"):
        super().__init__()
        
        self.enemy_type = enemy_type
        self.setup_enemy_stats()
        
        # Load enemy image
        try:
            self.image = pygame.image.load(f"assets/images/enemy_{enemy_type}.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)
        except:
            # Create a default enemy plane if image can't be loaded
            self.create_default_plane()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Enemy attributes
        self.speed = speed
        self.health = self.max_health
        self.last_shot = 0
        self.can_shoot = self.enemy_type in ["bomber", "interceptor"]
    
    def setup_enemy_stats(self):
        """Setup enemy stats based on type"""
        if self.enemy_type == "fighter":
            self.max_health = 1
            self.size = (45, 60)
            self.score_value = 10
            self.fire_rate = 0  # Doesn't shoot
        elif self.enemy_type == "bomber":
            self.max_health = 3
            self.size = (55, 70)
            self.score_value = 25
            self.fire_rate = 80  # Slow shooting
        elif self.enemy_type == "interceptor":
            self.max_health = 2
            self.size = (40, 55)
            self.score_value = 15
            self.fire_rate = 60  # Medium shooting
    
    def create_default_plane(self):
        """Create a default plane-like enemy"""
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        
        if self.enemy_type == "fighter":
            # Red fighter jet
            # Main fuselage
            pygame.draw.ellipse(self.image, (180, 30, 30), (15, 5, 15, 50))
            # Wings
            pygame.draw.polygon(self.image, (150, 20, 20), [(5, 25), (40, 25), (35, 35), (10, 35)])
            # Cockpit
            pygame.draw.ellipse(self.image, (100, 100, 255), (18, 8, 9, 12))
            # Engine exhaust
            pygame.draw.rect(self.image, (255, 100, 0), (19, 48, 6, 8))
            
        elif self.enemy_type == "bomber":
            # Gray bomber
            # Main fuselage (larger)
            pygame.draw.ellipse(self.image, (100, 100, 100), (15, 5, 25, 60))
            # Wings (broader)
            pygame.draw.polygon(self.image, (80, 80, 80), [(0, 30), (55, 30), (50, 40), (5, 40)])
            # Cockpit
            pygame.draw.ellipse(self.image, (150, 150, 200), (22, 8, 11, 15))
            # Engine pods
            pygame.draw.ellipse(self.image, (60, 60, 60), (8, 50, 8, 15))
            pygame.draw.ellipse(self.image, (60, 60, 60), (39, 50, 8, 15))
            
        elif self.enemy_type == "interceptor":
            # Dark blue interceptor
            # Main fuselage (sleek)
            pygame.draw.ellipse(self.image, (30, 30, 150), (12, 5, 16, 45))
            # Swept wings
            pygame.draw.polygon(self.image, (20, 20, 120), [(3, 20), (37, 20), (32, 30), (8, 30)])
            # Cockpit
            pygame.draw.ellipse(self.image, (200, 200, 255), (16, 8, 8, 10))
            # Afterburner
            pygame.draw.rect(self.image, (0, 100, 255), (17, 42, 6, 10))
    
    def update(self, screen_height):
        # Move enemy down
        self.rect.y += self.speed
        
        # If enemy goes off screen, reset it to the top
        if self.rect.top > screen_height:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, 800 - self.rect.width)
    
    def can_fire(self):
        """Check if enemy can fire a bullet"""
        if not self.can_shoot or self.fire_rate == 0:
            return False
            
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate:
            self.last_shot = current_time
            return True
        return False
    
    def take_damage(self, damage=1):
        """Enemy takes damage, returns True if destroyed"""
        self.health -= damage
        return self.health <= 0
    
    def get_bullet_position(self):
        """Get position for enemy bullet"""
        return (self.rect.centerx, self.rect.bottom)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=4):
        super().__init__()
        
        # Create enemy bullet (different from player bullets)
        self.image = pygame.Surface((6, 12))
        self.image.fill((255, 50, 50))  # Red color
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        
        self.speed = speed
    
    def update(self):
        """Update enemy bullet movement"""
        self.rect.y += self.speed
        
        # Remove bullet if it goes off screen
        if self.rect.top > 600:
            self.kill()

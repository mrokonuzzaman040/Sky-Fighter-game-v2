import pygame
import random
import math

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
        
        # For tracking bullets spawned by this enemy
        self.bullets = pygame.sprite.Group()
    
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
            self.fire_rate = 2000  # Fire every 2 seconds (much slower)
            self.fire_chance = 0.3  # 30% chance to fire when fire_rate allows
        elif self.enemy_type == "interceptor":
            self.max_health = 2
            self.size = (40, 55)
            self.score_value = 15
            self.fire_rate = 1500  # Fire every 1.5 seconds
            self.fire_chance = 0.4  # 40% chance to fire when fire_rate allows
    
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
            # Clean up bullets before resetting position
            self.destroy_bullets()
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, 800 - self.rect.width)
    
    def can_fire(self):
        """Check if enemy can fire a bullet with randomness to reduce spam"""
        if not self.can_shoot or self.fire_rate == 0:
            return False
            
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate:
            # Add randomness to prevent bullet spam
            if random.random() < getattr(self, 'fire_chance', 0.5):
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
    
    def get_bullet_patterns(self, player_pos=None):
        """Get bullet patterns based on enemy type"""
        patterns = []
        
        if self.enemy_type == "bomber":
            # Bombers fire spread shots in multiple directions
            base_angles = [-30, 0, 30]  # Degrees
            selected_angles = random.sample(base_angles, random.randint(1, 2))  # 1-2 bullets
            
            for angle in selected_angles:
                # Convert angle to radians and calculate direction
                angle_rad = math.radians(angle)
                dx = math.sin(angle_rad) * 0.8
                dy = math.cos(angle_rad) * 0.9  # Mostly downward but with spread
                
                patterns.append({
                    'x': self.rect.centerx + random.randint(-5, 5),
                    'y': self.rect.bottom,
                    'direction': (dx + random.uniform(-0.1, 0.1), dy),
                    'speed': random.uniform(2.0, 3.0)
                })
                
        elif self.enemy_type == "interceptor":
            # Interceptors have varied attack patterns
            pattern_type = random.choice(["aimed", "spread", "diagonal"])
            
            if pattern_type == "aimed" and player_pos:
                # Aim toward player with some inaccuracy
                dx = player_pos[0] - self.rect.centerx
                dy = player_pos[1] - self.rect.centery
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    # Normalize with inaccuracy
                    accuracy = random.uniform(0.5, 0.8)
                    dx = (dx / distance) * accuracy + random.uniform(-0.3, 0.3)
                    dy = (dy / distance) * accuracy + random.uniform(-0.1, 0.1)
                    
                    patterns.append({
                        'x': self.rect.centerx,
                        'y': self.rect.bottom,
                        'direction': (dx, dy),
                        'speed': random.uniform(3.0, 4.0)
                    })
            
            elif pattern_type == "spread":
                # Fire 2-3 bullets in spread pattern
                angles = [-45, 0, 45]  # Degrees
                num_bullets = random.randint(2, 3)
                selected_angles = random.sample(angles, num_bullets)
                
                for angle in selected_angles:
                    angle_rad = math.radians(angle)
                    dx = math.sin(angle_rad) * 0.7
                    dy = math.cos(angle_rad) * 0.8
                    
                    patterns.append({
                        'x': self.rect.centerx,
                        'y': self.rect.bottom,
                        'direction': (dx, dy),
                        'speed': random.uniform(2.5, 3.5)
                    })
            
            else:  # diagonal
                # Fire diagonally (left or right)
                direction = random.choice([-1, 1])  # Left or right
                dx = direction * random.uniform(0.4, 0.7)
                dy = random.uniform(0.7, 1.0)
                
                patterns.append({
                    'x': self.rect.centerx,
                    'y': self.rect.bottom,
                    'direction': (dx, dy),
                    'speed': random.uniform(3.0, 4.0)
                })
        
        elif self.enemy_type == "fighter":
            # Fighters don't normally shoot, but if they somehow do, make it simple
            patterns.append({
                'x': self.rect.centerx,
                'y': self.rect.bottom,
                'direction': (random.uniform(-0.2, 0.2), 1),
                'speed': 3.0
            })
        
        return patterns
    
    def destroy_bullets(self):
        """Remove all bullets spawned by this enemy"""
        self.bullets.empty()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=(0, 1), speed=4, owner=None):
        super().__init__()
        
        # Normalize direction vector to ensure consistent speed
        dir_length = math.sqrt(direction[0]**2 + direction[1]**2)
        if dir_length > 0:
            self.direction = (direction[0] / dir_length, direction[1] / dir_length)
        else:
            self.direction = (0, 1)  # Default downward
        
        # Create enemy bullet with different styles based on owner type and direction
        if owner and owner.enemy_type == "bomber":
            # Larger, slower bullets for bombers
            self.image = pygame.Surface((10, 18))
            self.image.fill((255, 80, 80))  # Orange-red
            # Add a small highlight for 3D effect
            pygame.draw.rect(self.image, (255, 120, 120), (2, 2, 6, 14))
        elif owner and owner.enemy_type == "interceptor":
            # Smaller, faster bullets for interceptors  
            self.image = pygame.Surface((6, 12))
            self.image.fill((255, 40, 40))  # Bright red
            # Add a glow effect
            pygame.draw.rect(self.image, (255, 100, 100), (1, 1, 4, 10))
        else:
            # Default bullet
            self.image = pygame.Surface((7, 14))
            self.image.fill((255, 60, 60))  # Standard red
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        
        self.speed = speed
        self.owner = owner  # Reference to the enemy that created this bullet
    
    def update(self):
        """Update enemy bullet movement"""
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Remove bullet if it goes off screen (expanded bounds for diagonal bullets)
        if (self.rect.bottom < -50 or self.rect.top > 650 or 
            self.rect.right < -50 or self.rect.left > 850):
            self.kill()
            # Remove from owner's bullet group if owner exists
            if self.owner and self in self.owner.bullets:
                self.owner.bullets.remove(self)

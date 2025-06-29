import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type="health"):
        super().__init__()
        
        self.powerup_type = powerup_type
        self.setup_powerup()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        
        # Movement
        self.speed = 2
        self.bob_time = 0
        
    def setup_powerup(self):
        """Setup powerup based on type"""
        size = (40, 40)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        
        if self.powerup_type == "health":
            # Red cross for health
            pygame.draw.rect(self.image, (255, 0, 0), (15, 5, 10, 30))
            pygame.draw.rect(self.image, (255, 0, 0), (5, 15, 30, 10))
            self.description = "Health +1"
            
        elif self.powerup_type == "rapid_fire":
            # Yellow lightning bolt for rapid fire
            pygame.draw.polygon(self.image, (255, 255, 0), [
                (10, 5), (20, 5), (15, 20), (25, 20), (15, 35), (5, 20), (10, 20)
            ])
            self.description = "Rapid Fire!"
            
        elif self.powerup_type == "triple_shot":
            # Blue triple arrows for triple shot
            color = (0, 100, 255)
            # Three arrows pointing up
            for i, x_offset in enumerate([-10, 0, 10]):
                pygame.draw.polygon(self.image, color, [
                    (20 + x_offset, 10), (15 + x_offset, 20), (25 + x_offset, 20)
                ])
            self.description = "Triple Shot!"
            
        elif self.powerup_type == "shield":
            # Light blue circle for shield
            pygame.draw.circle(self.image, (173, 216, 230), (20, 20), 18, 3)
            pygame.draw.circle(self.image, (0, 191, 255), (20, 20), 15, 2)
            self.description = "Shield Protection!"
            
        elif self.powerup_type == "speed_boost":
            # Green double arrows for speed
            color = (0, 255, 0)
            pygame.draw.polygon(self.image, color, [
                (8, 25), (8, 15), (18, 20)
            ])
            pygame.draw.polygon(self.image, color, [
                (22, 25), (22, 15), (32, 20)
            ])
            self.description = "Speed Boost!"
            
        elif self.powerup_type == "double_score":
            # Gold coin for double score
            pygame.draw.circle(self.image, (255, 215, 0), (20, 20), 18)
            pygame.draw.circle(self.image, (218, 165, 32), (20, 20), 15, 2)
            # Draw "2X" in the center
            font = pygame.font.Font(None, 20)
            text = font.render("2X", True, (0, 0, 0))
            text_rect = text.get_rect(center=(20, 20))
            self.image.blit(text, text_rect)
            self.description = "Double Score!"
    
    def update(self):
        """Update powerup movement"""
        # Move down
        self.rect.y += self.speed
        
        # Add slight bobbing motion
        self.bob_time += 0.2
        self.rect.x += int(math.sin(self.bob_time) * 0.5)
        
        # Remove if off screen
        if self.rect.top > 600:
            self.kill()

# Import math for bobbing motion
import math

class PowerUpManager:
    """Manages power-up spawning and effects"""
    
    def __init__(self):
        self.active_powerups = {}  # Store active power-up effects
        self.spawn_chance = 0.005  # Chance per frame to spawn a power-up
        
        # Power-up types and their spawn weights
        self.powerup_types = {
            "health": 25,
            "rapid_fire": 20,
            "triple_shot": 15,
            "shield": 10,
            "speed_boost": 20,
            "double_score": 10
        }
    
    def should_spawn_powerup(self):
        """Check if a power-up should spawn"""
        return random.random() < self.spawn_chance
    
    def get_random_powerup_type(self):
        """Get a random power-up type based on weights"""
        total_weight = sum(self.powerup_types.values())
        r = random.randint(1, total_weight)
        
        current_weight = 0
        for powerup_type, weight in self.powerup_types.items():
            current_weight += weight
            if r <= current_weight:
                return powerup_type
        
        return "health"  # Fallback
    
    def apply_powerup(self, player, powerup_type):
        """Apply power-up effect to player"""
        current_time = pygame.time.get_ticks()
        
        if powerup_type == "health":
            if player.health < player.max_health:
                player.health += 1
            return "Health restored!"
            
        elif powerup_type == "rapid_fire":
            self.active_powerups["rapid_fire"] = current_time + 5000  # 5 seconds
            return "Rapid fire activated!"
            
        elif powerup_type == "triple_shot":
            self.active_powerups["triple_shot"] = current_time + 8000  # 8 seconds
            return "Triple shot activated!"
            
        elif powerup_type == "shield":
            self.active_powerups["shield"] = current_time + 10000  # 10 seconds
            return "Shield activated!"
            
        elif powerup_type == "speed_boost":
            self.active_powerups["speed_boost"] = current_time + 6000  # 6 seconds
            player.speed = min(player.speed + 3, 12)  # Increase speed but cap it
            return "Speed boost activated!"
            
        elif powerup_type == "double_score":
            self.active_powerups["double_score"] = current_time + 15000  # 15 seconds
            return "Double score activated!"
    
    def update_powerups(self, player):
        """Update active power-ups and remove expired ones"""
        current_time = pygame.time.get_ticks()
        expired_powerups = []
        
        for powerup_type, end_time in self.active_powerups.items():
            if current_time > end_time:
                expired_powerups.append(powerup_type)
        
        # Remove expired power-ups
        for powerup_type in expired_powerups:
            del self.active_powerups[powerup_type]
            
            # Reset effects
            if powerup_type == "speed_boost":
                player.speed = max(player.speed - 3, 7)  # Reset to normal speed
    
    def is_active(self, powerup_type):
        """Check if a power-up is currently active"""
        current_time = pygame.time.get_ticks()
        return (powerup_type in self.active_powerups and 
                current_time < self.active_powerups[powerup_type])
    
    def get_remaining_time(self, powerup_type):
        """Get remaining time for a power-up in seconds"""
        if not self.is_active(powerup_type):
            return 0
        
        current_time = pygame.time.get_ticks()
        return max(0, (self.active_powerups[powerup_type] - current_time) / 1000.0)
    
    def has_shield(self):
        """Check if shield is active"""
        return self.is_active("shield")
    
    def get_score_multiplier(self):
        """Get current score multiplier"""
        return 2 if self.is_active("double_score") else 1
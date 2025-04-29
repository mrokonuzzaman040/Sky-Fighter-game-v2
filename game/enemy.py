import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        
        # Load enemy image
        try:
            self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        except:
            # Create a default enemy ship if image can't be loaded
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (255, 0, 0), [(0, 0), (40, 0), (20, 40)])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Enemy attributes
        self.speed = speed
        
    def update(self, screen_height):
        # Move enemy down
        self.rect.y += self.speed
        
        # If enemy goes off screen, reset it to the top
        if self.rect.top > screen_height:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, 800 - self.rect.width)

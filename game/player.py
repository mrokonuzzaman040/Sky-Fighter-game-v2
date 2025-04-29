import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Load player image
        try:
            self.image = pygame.image.load("assets/images/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
        except:
            # Create a default player ship if image can't be loaded
            self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (0, 128, 255), [(0, 40), (25, 0), (50, 40)])
            pygame.draw.rect(self.image, (100, 100, 100), (15, 25, 20, 15))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Player attributes
        self.speed = 7
        self.health = 3
        self.max_health = 3
    
    def update(self, keys, screen_width):
        # Move player based on key presses
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed
        
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

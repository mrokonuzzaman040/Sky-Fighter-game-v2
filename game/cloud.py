import pygame
import random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Create cloud images
        try:
            self.image = pygame.image.load("assets/images/cloud.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 60))
        except:
            # Create a default cloud if image can't be loaded
            self.image = pygame.Surface((100, 60), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (255, 255, 255, 180), (0, 20, 50, 40))
            pygame.draw.ellipse(self.image, (255, 255, 255, 180), (30, 10, 50, 50))
            pygame.draw.ellipse(self.image, (255, 255, 255, 180), (60, 20, 40, 40))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Cloud attributes
        self.speed = random.uniform(0.5, 1.5)
        
    def update(self):
        # Move cloud down slowly
        self.rect.y += self.speed
        
        # If cloud goes off screen, reset it to the top
        if self.rect.top > 600:
            self.rect.y = random.randint(-100, -50)
            self.rect.x = random.randint(0, 800 - self.rect.width)
            self.speed = random.uniform(0.5, 1.5)

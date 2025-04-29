import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Create bullet
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 255, 0))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        # Bullet attributes
        self.speed = 10
        
    def update(self):
        # Move bullet up
        self.rect.y -= self.speed
        
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()

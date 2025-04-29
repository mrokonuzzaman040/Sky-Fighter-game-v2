import os
from PIL import Image, ImageDraw, ImageFilter

def create_directories():
    """Create required directories"""
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    
def create_menu_bg():
    """Create a basic menu background"""
    img = Image.new('RGB', (800, 600), color=(30, 50, 100))
    draw = ImageDraw.Draw(img)
    
    # Draw some stars
    for i in range(100):
        x = (i * 17) % 800
        y = (i * 23) % 600
        size = (i % 3) + 1
        draw.rectangle((x, y, x+size, y+size), fill=(255, 255, 255))
    
    # Add a gradient
    for y in range(600):
        for x in range(800):
            r, g, b = img.getpixel((x, y))
            factor = 1 - (y / 800)
            img.putpixel((x, y), (int(r + 20 * factor), int(g + 20 * factor), int(b)))
    
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img.save("assets/images/menu_bg.jpg")
    
def create_sky_bg():
    """Create a basic game background"""
    img = Image.new('RGB', (800, 600), color=(100, 150, 255))
    draw = ImageDraw.Draw(img)
    
    # Add some clouds
    for i in range(5):
        x = (i * 160) % 800
        y = (i * 100) % 200
        draw.ellipse((x, y, x+120, y+60), fill=(255, 255, 255, 180))
        draw.ellipse((x+40, y-20, x+160, y+40), fill=(255, 255, 255, 180))
    
    img.save("assets/images/sky_bg.jpg")
    
def create_player():
    """Create basic player ship image"""
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw triangular ship
    draw.polygon([(32, 10), (10, 50), (54, 50)], fill=(0, 128, 255))
    draw.rectangle((22, 30, 42, 45), fill=(100, 100, 100))
    
    img.save("assets/images/player.png")
    
def create_enemy():
    """Create basic enemy ship image"""
    img = Image.new('RGBA', (50, 50), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw triangular enemy
    draw.polygon([(5, 5), (45, 5), (25, 45)], fill=(255, 50, 50))
    
    img.save("assets/images/enemy.png")

def create_cloud():
    """Create basic cloud image"""
    img = Image.new('RGBA', (100, 60), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw cloud from overlapping ellipses
    draw.ellipse((0, 20, 50, 40), fill=(255, 255, 255, 180))
    draw.ellipse((30, 10, 80, 50), fill=(255, 255, 255, 180))
    draw.ellipse((60, 20, 100, 40), fill=(255, 255, 255, 180))
    
    img.save("assets/images/cloud.png")

if __name__ == "__main__":
    create_directories()
    create_menu_bg()
    create_sky_bg()
    create_player()
    create_enemy()
    create_cloud()
    print("Basic assets created!")

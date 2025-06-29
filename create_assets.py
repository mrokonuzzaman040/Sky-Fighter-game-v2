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
    """Create detailed player fighter jet image"""
    img = Image.new('RGBA', (60, 70), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main fuselage (blue)
    draw.ellipse((22, 10, 38, 60), fill=(0, 120, 200))
    
    # Wings
    draw.polygon([(5, 25), (55, 25), (50, 35), (10, 35)], fill=(0, 100, 180))
    
    # Cockpit
    draw.ellipse((26, 12, 34, 24), fill=(150, 200, 255))
    
    # Wing tips
    draw.ellipse((3, 27, 9, 35), fill=(100, 100, 100))
    draw.ellipse((51, 27, 57, 35), fill=(100, 100, 100))
    
    # Engine exhaust
    draw.rectangle((27, 52, 33, 60), fill=(255, 150, 0))
    
    # Tail fins
    draw.polygon([(25, 60), (35, 60), (32, 68), (28, 68)], fill=(0, 80, 160))
    
    # Nose cone
    draw.polygon([(28, 10), (32, 10), (30, 5)], fill=(0, 140, 220))
    
    img.save("assets/images/player.png")

def create_enemy():
    """Create basic enemy fighter jet image"""
    img = Image.new('RGBA', (45, 60), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main fuselage
    draw.ellipse((15, 5, 30, 55), fill=(180, 30, 30))
    
    # Wings
    draw.polygon([(5, 25), (40, 25), (35, 35), (10, 35)], fill=(150, 20, 20))
    
    # Cockpit
    draw.ellipse((18, 8, 27, 20), fill=(100, 100, 255))
    
    # Engine exhaust
    draw.rectangle((19, 48, 25, 56), fill=(255, 100, 0))
    
    img.save("assets/images/enemy.png")

def create_enemy_variants():
    """Create different enemy aircraft types"""
    
    # Fighter
    img = Image.new('RGBA', (45, 60), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((15, 5, 30, 55), fill=(180, 30, 30))
    draw.polygon([(5, 25), (40, 25), (35, 35), (10, 35)], fill=(150, 20, 20))
    draw.ellipse((18, 8, 27, 20), fill=(100, 100, 255))
    draw.rectangle((19, 48, 25, 56), fill=(255, 100, 0))
    img.save("assets/images/enemy_fighter.png")
    
    # Bomber
    img = Image.new('RGBA', (55, 70), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((15, 5, 40, 65), fill=(100, 100, 100))
    draw.polygon([(0, 30), (55, 30), (50, 40), (5, 40)], fill=(80, 80, 80))
    draw.ellipse((22, 8, 33, 23), fill=(150, 150, 200))
    draw.ellipse((8, 50, 16, 65), fill=(60, 60, 60))
    draw.ellipse((39, 50, 47, 65), fill=(60, 60, 60))
    img.save("assets/images/enemy_bomber.png")
    
    # Interceptor
    img = Image.new('RGBA', (40, 55), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((12, 5, 28, 50), fill=(30, 30, 150))
    draw.polygon([(3, 20), (37, 20), (32, 30), (8, 30)], fill=(20, 20, 120))
    draw.ellipse((16, 8, 24, 18), fill=(200, 200, 255))
    draw.rectangle((17, 42, 23, 52), fill=(0, 100, 255))
    img.save("assets/images/enemy_interceptor.png")

def create_boss():
    """Create basic boss aircraft image"""
    img = Image.new('RGBA', (150, 120), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main fuselage
    draw.ellipse((40, 15, 80, 85), fill=(150, 20, 20))
    
    # Large wings
    draw.polygon([(10, 40), (140, 40), (130, 55), (20, 55)], fill=(120, 15, 15))
    
    # Cockpit
    draw.ellipse((52, 20, 68, 40), fill=(100, 0, 0))
    
    # Wing weapons
    draw.rectangle((8, 45, 20, 51), fill=(80, 80, 80))
    draw.rectangle((130, 45, 142, 51), fill=(80, 80, 80))
    
    # Engine exhausts
    draw.rectangle((50, 75, 58, 85), fill=(255, 100, 0))
    draw.rectangle((62, 75, 70, 85), fill=(255, 100, 0))
    
    img.save("assets/images/boss.png")

def create_boss_variants():
    """Create different boss aircraft types"""
    
    # Basic Boss - Heavy Fighter
    img = Image.new('RGBA', (120, 100), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((40, 15, 80, 85), fill=(150, 20, 20))
    draw.polygon([(10, 40), (110, 40), (100, 55), (20, 55)], fill=(120, 15, 15))
    draw.ellipse((52, 20, 68, 40), fill=(100, 0, 0))
    draw.rectangle((8, 45, 20, 51), fill=(80, 80, 80))
    draw.rectangle((100, 45, 112, 51), fill=(80, 80, 80))
    draw.rectangle((50, 75, 58, 85), fill=(255, 100, 0))
    draw.rectangle((62, 75, 70, 85), fill=(255, 100, 0))
    img.save("assets/images/boss_basic.png")
    
    # Advanced Boss - Strategic Bomber
    img = Image.new('RGBA', (150, 120), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 10, 100, 110), fill=(80, 80, 80))
    draw.polygon([(0, 50), (150, 50), (140, 70), (10, 70)], fill=(60, 60, 60))
    # Engine pods
    for x in [15, 45, 105, 135]:
        draw.ellipse((x, 75, x+10, 100), fill=(40, 40, 40))
        draw.rectangle((x+1, 90, x+9, 105), fill=(255, 150, 0))
    draw.ellipse((62, 15, 88, 45), fill=(100, 120, 150))
    img.save("assets/images/boss_advanced.png")
    
    # Final Boss - Mothership
    img = Image.new('RGBA', (180, 150), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((30, 20, 150, 130), fill=(60, 10, 10))
    draw.rectangle((70, 10, 110, 50), fill=(80, 15, 15))
    draw.ellipse((80, 15, 100, 30), fill=(150, 50, 50))
    draw.polygon([(0, 60), (180, 60), (170, 90), (10, 90)], fill=(40, 8, 8))
    # Multiple engines
    engine_positions = [(40, 115), (60, 120), (80, 122), (100, 122), (120, 120), (140, 115)]
    for x, y in engine_positions:
        draw.ellipse((x, y, x+8, y+15), fill=(255, 100, 0))
    img.save("assets/images/boss_final.png")

def create_cloud():
    """Create basic cloud image"""
    img = Image.new('RGBA', (100, 60), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw cloud from overlapping ellipses
    draw.ellipse((0, 20, 50, 40), fill=(255, 255, 255, 180))
    draw.ellipse((30, 10, 80, 50), fill=(255, 255, 255, 180))
    draw.ellipse((60, 20, 100, 40), fill=(255, 255, 255, 180))
    
    img.save("assets/images/cloud.png")

def create_powerup_icons():
    """Create power-up icon images"""
    # Health power-up
    img = Image.new('RGBA', (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((15, 5, 25, 35), fill=(255, 0, 0))
    draw.rectangle((5, 15, 35, 25), fill=(255, 0, 0))
    img.save("assets/images/powerup_health.png")
    
    # Rapid fire power-up
    img = Image.new('RGBA', (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(10, 5), (20, 5), (15, 20), (25, 20), (15, 35), (5, 20), (10, 20)], fill=(255, 255, 0))
    img.save("assets/images/powerup_rapid_fire.png")
    
    # Triple shot power-up
    img = Image.new('RGBA', (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i, x_offset in enumerate([-10, 0, 10]):
        draw.polygon([(20 + x_offset, 10), (15 + x_offset, 20), (25 + x_offset, 20)], fill=(0, 100, 255))
    img.save("assets/images/powerup_triple_shot.png")
    
    # Shield power-up
    img = Image.new('RGBA', (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((2, 2, 38, 38), outline=(0, 191, 255), width=3)
    draw.ellipse((7, 7, 33, 33), outline=(173, 216, 230), width=2)
    img.save("assets/images/powerup_shield.png")
    
    # Speed boost power-up
    img = Image.new('RGBA', (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(8, 25), (8, 15), (18, 20)], fill=(0, 255, 0))
    draw.polygon([(22, 25), (22, 15), (32, 20)], fill=(0, 255, 0))
    img.save("assets/images/powerup_speed.png")
    
    # Double score power-up
    img = Image.new('RGBA', (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((2, 2, 38, 38), fill=(255, 215, 0))
    draw.ellipse((7, 7, 33, 33), outline=(218, 165, 32), width=2)
    # Add 2X text (simplified)
    draw.text((12, 12), "2X", fill=(0, 0, 0))
    img.save("assets/images/powerup_double_score.png")

if __name__ == "__main__":
    create_directories()
    create_menu_bg()
    create_sky_bg()
    create_player()
    create_enemy()
    create_enemy_variants()
    create_cloud()
    create_boss()
    create_boss_variants()
    create_powerup_icons()
    print("All aircraft assets created including realistic planes, bosses, and power-ups!")

#!/usr/bin/env python3
"""
Generate the cutest picture - enhanced version.
Kitten hugging a sleeping duckling with daisy crown, mint scarf, blue eyes.
Based on top performers on leaderboard.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT_DIR = Path("/output")


def draw_circle(draw, center, radius, fill, outline=None, width=1):
    """Draw a circle."""
    x, y = center
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill, outline=outline, width=width)


def draw_ellipse(draw, bbox, fill, outline=None, width=1):
    """Draw an ellipse."""
    draw.ellipse(bbox, fill=fill, outline=outline, width=width)


def draw_rect(draw, bbox, fill, outline=None, width=1):
    """Draw a rectangle."""
    draw.rectangle(bbox, fill=fill, outline=outline, width=width)


def draw_line(draw, p1, p2, fill, width=1):
    """Draw a line."""
    draw.line([p1, p2], fill=fill, width=width)


def draw_triangle(draw, p1, p2, p3, fill, outline=None, width=1):
    """Draw a triangle."""
    draw.polygon([p1, p2, p3], fill=fill, outline=outline, width=width)


def draw_arc(draw, bbox, start, end, fill=None, width=1):
    """Draw an arc."""
    draw.arc(bbox, start, end, fill=fill, width=width)


def draw_eye(draw, center, size, color_white, color_black, color_highlight):
    """Draw a cute eye with sparkle."""
    x, y = center
    # White part
    draw_circle(draw, (x, y), size, color_white)
    # Black pupil
    draw_circle(draw, (x, y), size * 0.55, color_black)
    # Large highlight
    draw_circle(draw, (x - size * 0.25, y - size * 0.25), size * 0.2, (255, 255, 255))
    # Small highlight
    draw_circle(draw, (x - size * 0.15, y - size * 0.35), size * 0.1, (255, 255, 255))


def draw_face(draw, center, width, height, color, eye_color_white, eye_color_black, eye_color_highlight, nose_color=(255, 150, 150)):
    """Draw a cute face."""
    cx, cy = center
    # Ears (large and floppy for kitten)
    ear_width = width // 3
    ear_height = height // 2
    # Left ear
    draw_triangle(draw, (cx - width // 2 + 10, cy - height // 2 + 5),
                  (cx - width // 2 - ear_width // 2, cy - height // 2 - ear_height // 2),
                  (cx - width // 2 + 10 + ear_width // 3, cy - height // 2 + 15), fill=color)
    # Right ear
    draw_triangle(draw, (cx + width // 2 - 10, cy - height // 2 + 5),
                  (cx + width // 2 + ear_width // 2, cy - height // 2 - ear_height // 2),
                  (cx + width // 2 - 10 - ear_width // 3, cy - height // 2 + 15), fill=color)
    # Inner ears
    inner_color = tuple(max(0, c - 50) for c in color)
    draw_triangle(draw, (cx - width // 2 + 15, cy - height // 2 + 10),
                  (cx - width // 2 - ear_width // 2 + 10, cy - height // 2 - ear_height // 2 + 10),
                  (cx - width // 2 + 15 + ear_width // 3, cy - height // 2 + 20), fill=inner_color)
    draw_triangle(draw, (cx + width // 2 - 15, cy - height // 2 + 10),
                  (cx + width // 2 + ear_width // 2 - 10, cy - height // 2 - ear_height // 2 + 10),
                  (cx + width // 2 - 15 - ear_width // 3, cy - height // 2 + 20), fill=inner_color)
    # Head
    draw_ellipse(draw, [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2], fill=color)
    # Eyes (big and cute)
    eye_y = cy - height // 5
    eye_size = width // 7
    draw_eye(draw, (cx - width // 4, eye_y), eye_size, eye_color_white, eye_color_black, eye_color_highlight)
    draw_eye(draw, (cx + width // 4, eye_y), eye_size, eye_color_white, eye_color_black, eye_color_highlight)
    # Eyelashes
    for side in [-1, 1]:
        lx = cx + side * width // 4
        ly = eye_y - eye_size * 0.5
        for i in range(3):
            lx2 = lx + side * (i + 1) * 3
            ly2 = ly - (i + 1) * 2
            draw_line(draw, (lx, ly), (lx2, ly2), (0, 0, 0), 2)
    # Nose
    draw_circle(draw, (cx, cy + height // 5), width // 10, nose_color)
    # Mouth (cute smile)
    mouth_y = cy + height // 4
    draw_arc(draw, (cx - width // 6, mouth_y - 5, cx + width // 6, mouth_y + 10), 180, 360, fill=None, width=2)
    # Blush
    blush_size = width // 8
    draw_ellipse(draw, [cx - width // 3 - blush_size // 2, cy + height // 4 - blush_size // 2, cx - width // 3 + blush_size // 2, cy + height // 4 + blush_size // 2], fill=(255, 150, 150, 100))
    draw_ellipse(draw, [cx + width // 3 - blush_size // 2, cy + height // 4 - blush_size // 2, cx + width // 3 + blush_size // 2, cy + height // 4 + blush_size // 2], fill=(255, 150, 150, 100))


def draw_body(draw, center, width, height, color):
    """Draw body."""
    cx, cy = center
    draw_ellipse(draw, [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2], fill=color)


def draw_tail(draw, start, control1, end, color, width=3):
    """Draw a curved tail."""
    points = []
    for t in range(100):
        t_val = t / 100
        x = (1 - t_val) ** 2 * start[0] + 2 * (1 - t_val) * t_val * control1[0] + t_val ** 2 * end[0]
        y = (1 - t_val) ** 2 * start[1] + 2 * (1 - t_val) * t_val * control1[1] + t_val ** 2 * end[1]
        points.append((int(x), int(y)))
    for i in range(len(points) - 1):
        draw_line(draw, points[i], points[i + 1], fill=color, width=width)


def draw_paw(draw, center, size, color):
    """Draw a cute paw."""
    x, y = center
    draw_ellipse(draw, [x - size // 2, y - size // 4, x + size // 2, y + size // 4], fill=color)
    # Paw pads
    draw_circle(draw, (x - size // 6, y + size // 4), size // 8, (255, 200, 200))
    draw_circle(draw, (x + size // 6, y + size // 4), size // 8, (255, 200, 200))
    draw_circle(draw, (x, y + size // 4), size // 8, (255, 200, 200))


def draw_duckling(draw, center, size, color_white, color_yellow):
    """Draw a cute sleeping duckling."""
    cx, cy = center
    # Body (oval)
    body_width = size * 1.3
    body_height = size * 0.8
    draw_ellipse(draw, [cx - body_width // 2, cy - body_height // 2, cx + body_width // 2, cy + body_height // 2], fill=color_white)
    # Head (smaller, turned to side)
    head_x = cx - body_width // 3
    head_y = cy - body_height // 2 + size // 4
    head_width = size // 2
    head_height = size // 2.5
    draw_ellipse(draw, [head_x - head_width // 2, head_y - head_height // 2, head_x + head_width // 2, head_y + head_height // 2], fill=color_white)
    # Beak
    beak_x = head_x - head_width // 2 + 5
    beak_y = head_y
    draw_triangle(draw, (beak_x - 5, beak_y - 3), (beak_x + 10, beak_y), (beak_x - 5, beak_y + 3), fill=color_yellow)
    # Eye (closed, sleeping)
    eye_y = head_y - head_height // 4
    draw_line(draw, (head_x - head_width // 4, eye_y), (head_x - head_width // 6, eye_y), fill=(0, 0, 0), width=2)
    # Wing (on body)
    wing_x = cx - body_width // 4
    wing_y = cy
    draw_ellipse(draw, [wing_x - size // 4, wing_y - size // 4, wing_x + size // 4, wing_y + size // 4], fill=(255, 240, 220))
    # Feet
    draw_triangle(draw, (cx - body_width // 4, cy + body_height // 2), (cx - body_width // 4 - size // 6, cy + body_height // 2 + size // 4), (cx - body_width // 4 + size // 12, cy + body_height // 2 + size // 4), fill=color_yellow)
    draw_triangle(draw, (cx + body_width // 4, cy + body_height // 2), (cx + body_width // 4 + size // 6, cy + body_height // 2 + size // 4), (cx + body_width // 4 - size // 12, cy + body_height // 2 + size // 4), fill=color_yellow)


def draw_fluffy_fur(draw, center, width, height, color, fur_color):
    """Add fluffy fur texture to body."""
    cx, cy = center
    for i in range(10):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(width // 2 * 0.7, width // 2)
        x = cx + math.cos(angle) * dist
        y = cy + math.sin(angle) * dist * 0.6
        fur_size = random.randint(3, 6)
        draw_circle(draw, (x, y), fur_size, fur_color)
        draw_circle(draw, (x, y), fur_size // 2, color)


def generate_image():
    """Generate the cutest picture - enhanced version."""
    width = 1024
    height = 1024
    
    # Create image with cream background
    img = Image.new('RGB', (width, height), (255, 250, 240))
    draw = ImageDraw.Draw(img)
    
    # Soft gradient background
    for y in range(height):
        alpha = y / height
        r = int(255 - alpha * 15)
        g = int(250 - alpha * 10)
        b = int(240 - alpha * 20)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Subtle heart-shaped bokeh background
    for i in range(30):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        heart_size = random.randint(5, 15)
        # Simple heart shape
        for dy in range(-heart_size, heart_size + 1):
            for dx in range(-heart_size, heart_size + 1):
                if dx * dx + (dy - heart_size * 0.3) ** 2 <= heart_size * heart_size * 0.6:
                    if dy > heart_size * 0.3 or (dx * dx + (dy - heart_size * 0.3) ** 2) <= heart_size * heart_size * 0.25:
                        color = (255, 200, 200) if random.random() > 0.5 else (200, 220, 255)
                        draw.point((x + dx, y + dy), fill=color)
    
    # Ground
    ground_y = height - 120
    draw_rect(draw, [0, ground_y, width, height], (220, 200, 180))
    # Grass
    for x in range(0, width, 10):
        grass_height = random.randint(15, 30)
        grass_color = (100, 180, 100) if random.random() > 0.3 else (80, 160, 80)
        draw_line(draw, (x, ground_y), (x, ground_y - grass_height), fill=grass_color, width=2)
        # Grass blade curve
        if random.random() > 0.5:
            draw_line(draw, (x, ground_y - grass_height // 2), (x + random.randint(-5, 5), ground_y - grass_height), fill=grass_color, width=1)
    
    # Small flowers on ground
    for i in range(5):
        fx = random.randint(100, width - 100)
        fy = ground_y - random.randint(5, 15)
        # Stem
        draw_line(draw, (fx, fy), (fx, fy - 30), fill=(100, 180, 100), width=2)
        # Petals
        for angle in range(0, 360, 72):
            px = fx + math.cos(math.radians(angle)) * 10
            py = fy - 30 + math.sin(math.radians(angle)) * 10
            draw_circle(draw, (px, py), 5, (255, 200, 200))
        draw_circle(draw, (fx, fy - 30), 4, (255, 215, 0))
    
    # Center the scene
    center_x = width // 2
    center_y = height // 2 - 30
    
    # Draw duckling first (being hugged)
    duckling_size = 90
    duckling_x = center_x - 30
    duckling_y = center_y + 40
    draw_duckling(draw, (duckling_x, duckling_y), duckling_size, (255, 250, 240), (255, 180, 50))
    
    # Draw kitten hugging duckling
    kitten_size = 140
    kitten_x = center_x + 20
    kitten_y = center_y - 20
    
    # Body
    draw_body(draw, (kitten_x, kitten_y + 20), kitten_size * 1.2, kitten_size * 1.3, (255, 240, 220))
    # Fluffy fur on body
    draw_fluffy_fur(draw, (kitten_x, kitten_y + 20), kitten_size * 1.2, kitten_size * 1.3, (255, 240, 220), (250, 230, 210))
    
    # Arm hugging (left)
    draw_paw(draw, (kitten_x - kitten_size // 2, kitten_y + 40), kitten_size // 4, (255, 240, 220))
    # Arm hugging (right)
    draw_paw(draw, (kitten_x + kitten_size // 2, kitten_y + 40), kitten_size // 4, (255, 240, 220))
    
    # Head
    head_y = kitten_y - kitten_size // 2 + 30
    draw_face(draw, (kitten_x, head_y), kitten_size // 2, kitten_size // 2, (255, 240, 220), (255, 255, 255), (0, 0, 0), (255, 255, 255))
    
    # Fluffy fur on head
    for _ in range(8):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(kitten_size // 4, kitten_size // 2)
        x = kitten_x + math.cos(angle) * dist
        y = head_y + math.sin(angle) * dist * 0.5
        fur_size = random.randint(4, 8)
        draw_circle(draw, (x, y), fur_size, (250, 230, 210))
    
    # Scarf
    scarf_y = head_y + kitten_size // 4
    draw_ellipse(draw, [kitten_x - kitten_size // 2, scarf_y - kitten_size // 8, kitten_x + kitten_size // 2, scarf_y + kitten_size // 6], fill=(100, 200, 150))
    # Scarf stripes
    for i in range(3):
        stripe_y = scarf_y - kitten_size // 8 + i * kitten_size // 12
        draw_line(draw, (kitten_x - kitten_size // 2 + 5, stripe_y), (kitten_x + kitten_size // 2 - 5, stripe_y), fill=(255, 255, 255), width=2)
    # Scarf tail
    draw_ellipse(draw, [kitten_x + kitten_size // 2 - kitten_size // 8, scarf_y + kitten_size // 8, kitten_x + kitten_size // 2 + kitten_size // 3, scarf_y + kitten_size // 3], fill=(100, 200, 150))
    
    # Daisy crown
    crown_y = head_y - kitten_size // 4
    # Flower centers
    for i in range(5):
        angle = i * math.pi * 2 / 5 - math.pi / 2
        dx = math.cos(angle) * kitten_size // 3
        dy = math.sin(angle) * kitten_size // 4
        petal_x = kitten_x + dx
        petal_y = crown_y + dy
        # Petals
        for j in range(5):
            pa = j * math.pi * 2 / 5
            px = petal_x + math.cos(pa) * kitten_size // 8
            py = petal_y + math.sin(pa) * kitten_size // 8
            draw_ellipse(draw, [px - kitten_size // 10, py - kitten_size // 10, px + kitten_size // 10, py + kitten_size // 10], fill=(255, 220, 220))
        # Center
        draw_circle(draw, (petal_x, petal_y), kitten_size // 10, (255, 215, 0))
    # Base
    draw_ellipse(draw, [kitten_x - kitten_size // 3, crown_y - kitten_size // 6, kitten_x + kitten_size // 3, crown_y + kitten_size // 6], fill=(100, 200, 150))
    
    # Tail (curled)
    tail_start = (kitten_x + kitten_size // 2, kitten_y + 20)
    tail_control = (kitten_x + kitten_size // 2 + kitten_size // 3, kitten_y + 10)
    tail_end = (kitten_x + kitten_size // 2 + kitten_size // 2, kitten_y - 20)
    draw_tail(draw, tail_start, tail_control, tail_end, (255, 240, 220), 4)
    # Tail fluffy tip
    draw_circle(draw, tail_end, kitten_size // 6, (250, 230, 210))
    
    # Sparkles around
    for _ in range(25):
        sparkle_x = random.randint(50, width - 50)
        sparkle_y = random.randint(50, height - 50)
        sparkle_size = random.randint(3, 8)
        # Four-pointed star
        for angle in range(0, 360, 90):
            dx = math.cos(math.radians(angle)) * sparkle_size
            dy = math.sin(math.radians(angle)) * sparkle_size
            draw_line(draw, (sparkle_x - dx, sparkle_y - dy), (sparkle_x + dx, sparkle_y + dy), fill=(255, 255, 200), width=2)
        draw_circle(draw, (sparkle_x, sparkle_y), sparkle_size // 2, (255, 255, 255))
    
    # Small stars
    for _ in range(10):
        star_x = random.randint(50, width - 50)
        star_y = random.randint(50, height - 50)
        star_size = random.randint(2, 4)
        for angle in range(0, 360, 72):
            dx = math.cos(math.radians(angle)) * star_size
            dy = math.sin(math.radians(angle)) * star_size
            draw_line(draw, (star_x - dx, star_y - dy), (star_x + dx, star_y + dy), fill=(255, 255, 255), width=1)
    
    # "Cute Friends" text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36) if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") else ImageFont.load_default()
        text = "Cute Friends"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (width - text_width) // 2
        text_y = height - 70
        # Text shadow
        draw.text((text_x + 1, text_y + 1), text, fill=(200, 180, 160), font=font)
        # Text
        draw.text((text_x, text_y), text, fill=(150, 100, 80), font=font)
    except:
        pass
    
    return img


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "entry.png"
    
    img = generate_image()
    img.save(output_path, "PNG")
    
    print(f"Image saved to {output_path}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")


if __name__ == "__main__":
    main()

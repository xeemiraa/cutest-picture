#!/usr/bin/env python3
"""
Generate the cutest picture - kitten hugging a chick.
Based on analysis of top performers on leaderboard.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT_DIR = Path("/output")


def draw_circle(draw, center, radius, fill, outline=None):
    """Draw a circle."""
    x, y = center
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill, outline=outline)


def draw_ellipse(draw, bbox, fill, outline=None):
    """Draw an ellipse."""
    draw.ellipse(bbox, fill=fill, outline=outline)


def draw_rect(draw, bbox, fill, outline=None):
    """Draw a rectangle."""
    draw.rectangle(bbox, fill=fill, outline=outline)


def draw_rounded_rect(draw, bbox, radius, fill, outline=None):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = bbox
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)


def draw_eye(draw, center, size, color_white, color_black, color_highlight):
    """Draw a cute eye."""
    x, y = center
    # White part
    draw_circle(draw, (x, y), size, color_white)
    # Black pupil
    draw_circle(draw, (x, y), size * 0.6, color_black)
    # Highlight
    draw_circle(draw, (x - size * 0.2, y - size * 0.2), size * 0.15, color_highlight)


def draw_triangle(draw, p1, p2, p3, fill, outline=None):
    """Draw a triangle."""
    draw.polygon([p1, p2, p3], fill=fill, outline=outline)


def draw_arc(draw, bbox, start, end, fill=None, width=1):
    """Draw an arc."""
    draw.arc(bbox, start, end, fill=fill, width=width)


def draw_face(draw, center, width, height, color, eye_color_white, eye_color_black, eye_color_highlight):
    """Draw a cute animal face."""
    cx, cy = center
    # Head
    draw_ellipse(draw, [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2], fill=color)
    # Ears
    ear_size = width // 4
    draw_triangle(draw, (cx - width // 2, cy - height // 2 + ear_size),
                  (cx - width // 2 - ear_size, cy - height // 2 - ear_size),
                  (cx - width // 2 + ear_size, cy - height // 2 - ear_size), fill=color)
    draw_triangle(draw, (cx + width // 2, cy - height // 2 + ear_size),
                  (cx + width // 2 + ear_size, cy - height // 2 - ear_size),
                  (cx + width // 2 - ear_size, cy - height // 2 - ear_size), fill=color)
    # Inner ears
    inner_color = tuple(max(0, c - 40) for c in color)
    draw_triangle(draw, (cx - width // 2 + 5, cy - height // 2 + ear_size - 5),
                  (cx - width // 2 - ear_size + 10, cy - height // 2 - ear_size + 10),
                  (cx - width // 2 + ear_size - 5, cy - height // 2 - ear_size + 10), fill=inner_color)
    draw_triangle(draw, (cx + width // 2 - 5, cy - height // 2 + ear_size - 5),
                  (cx + width // 2 + ear_size - 10, cy - height // 2 - ear_size + 10),
                  (cx + width // 2 - ear_size + 5, cy - height // 2 - ear_size + 10), fill=inner_color)
    # Eyes
    eye_y = cy - height // 6
    draw_eye(draw, (cx - width // 4, eye_y), width // 8, eye_color_white, eye_color_black, eye_color_highlight)
    draw_eye(draw, (cx + width // 4, eye_y), width // 8, eye_color_white, eye_color_black, eye_color_highlight)
    # Nose
    draw_circle(draw, (cx, cy + height // 6), width // 12, (255, 150, 150))
    # Mouth
    draw_arc(draw, (cx - width // 8, cy + height // 4, cx + width // 8, cy + height // 3), 0, 180, fill=None, width=2)


def draw_chick(draw, center, size, color_yellow, color_orange):
    """Draw a cute chick."""
    cx, cy = center
    # Body
    draw_ellipse(draw, [cx - size, cy - size // 2, cx + size, cy + size // 2], fill=color_yellow)
    # Eyes
    eye_y = cy - size // 4
    draw_eye(draw, (cx - size // 3, eye_y), size // 6, (255, 255, 255), (0, 0, 0), (255, 255, 255))
    draw_eye(draw, (cx + size // 3, eye_y), size // 6, (255, 255, 255), (0, 0, 0), (255, 255, 255))
    # Beak
    beak_size = size // 4
    draw_triangle(draw, (cx - beak_size, cy), (cx + beak_size, cy), (cx, cy + beak_size), fill=color_orange)
    # Feet
    draw_triangle(draw, (cx - size // 2, cy + size // 2), (cx - size // 2 - size // 4, cy + size // 2 + size // 3), (cx - size // 4, cy + size // 2 + size // 3), fill=color_orange)
    draw_triangle(draw, (cx + size // 2, cy + size // 2), (cx + size // 2 + size // 4, cy + size // 2 + size // 3), (cx + size // 4, cy + size // 2 + size // 3), fill=color_orange)
    # Wings
    draw_ellipse(draw, [cx - size - size // 4, cy - size // 4, cx - size + size // 4, cy + size // 4], fill=color_yellow)


def draw_curve(draw, start, control1, end, fill):
    """Draw a quadratic bezier curve."""
    points = []
    for t in range(101):
        t_val = t / 100
        x = (1 - t_val) ** 2 * start[0] + 2 * (1 - t_val) * t_val * control1[0] + t_val ** 2 * end[0]
        y = (1 - t_val) ** 2 * start[1] + 2 * (1 - t_val) * t_val * control1[1] + t_val ** 2 * end[1]
        points.append((int(x), int(y)))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=fill, width=3)


def draw_kitten(draw, center, size, color_cream, color_mint, color_orange):
    """Draw a cute kitten hugging a chick."""
    cx, cy = center
    # Body
    body_width = size * 1.2
    body_height = size * 1.5
    draw_ellipse(draw, [cx - body_width // 2, cy - body_height // 2, cx + body_width // 2, cy + body_height // 2], fill=color_cream)
    # Tail
    tail_x = cx + body_width // 2
    tail_y = cy
    draw_curve(draw, (tail_x, tail_y), (tail_x + size // 2, tail_y - size // 3), (tail_x + size // 3, tail_y - size // 2), fill=color_cream)
    # Head
    head_y = cy - body_height // 2 + size // 3
    draw_face(draw, (cx, head_y), size // 2, size // 2, color_cream, (255, 255, 255), (0, 0, 0), (255, 255, 255))
    # Scarf
    scarf_y = head_y + size // 4
    draw_ellipse(draw, [cx - size // 2, scarf_y - size // 8, cx + size // 2, scarf_y + size // 8], fill=color_mint)
    # Scarf tail
    draw_ellipse(draw, [cx + size // 2 - size // 8, scarf_y + size // 8, cx + size // 2 + size // 4, scarf_y + size // 4], fill=color_mint)
    # Daisy crown
    crown_y = head_y - size // 4
    for i in range(5):
        angle = i * math.pi / 2.5
        dx = math.cos(angle) * size // 3
        dy = math.sin(angle) * size // 3
        petal_x = cx + dx
        petal_y = crown_y + dy
        draw_ellipse(draw, [petal_x - size // 8, petal_y - size // 8, petal_x + size // 8, petal_y + size // 8], fill=color_mint)
        draw_circle(draw, (petal_x, petal_y), size // 12, color_orange)
    draw_ellipse(draw, [cx - size // 3, crown_y - size // 6, cx + size // 3, crown_y + size // 6], fill=color_mint)
    # Arms hugging
    arm_y = cy + size // 6
    arm_size = size // 3
    draw_ellipse(draw, [cx - body_width // 2 + size // 4, arm_y - arm_size // 2, cx - body_width // 2 + size // 4 + arm_size, arm_y + arm_size // 2], fill=color_cream)
    draw_ellipse(draw, [cx + body_width // 2 - size // 4 - arm_size, arm_y - arm_size // 2, cx + body_width // 2 - size // 4, arm_y + arm_size // 2], fill=color_cream)


def generate_image():
    """Generate the cutest picture."""
    width = 1024
    height = 1024
    
    # Create image with soft background
    img = Image.new('RGB', (width, height), (255, 248, 240))
    draw = ImageDraw.Draw(img)
    
    # Soft gradient background
    for y in range(height):
        alpha = y / height
        r = int(255 - alpha * 10)
        g = int(248 - alpha * 8)
        b = int(240 - alpha * 15)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Ground
    ground_y = height - 100
    draw_rect(draw, [0, ground_y, width, height], (200, 180, 160))
    # Grass tufts
    for x in range(0, width, 20):
        grass_height = random.randint(10, 20)
        draw.line([(x, ground_y), (x, ground_y - grass_height)], fill=(100, 180, 100), width=2)
    
    # Center the kitten and chick
    center_x = width // 2
    center_y = height // 2 - 50
    
    # Draw chick first (being hugged)
    chick_size = 80
    chick_x = center_x
    chick_y = center_y + 60
    draw_chick(draw, (chick_x, chick_y), chick_size, (255, 220, 100), (255, 150, 50))
    
    # Draw kitten hugging chick
    kitten_size = 120
    kitten_x = center_x
    kitten_y = center_y - 20
    draw_kitten(draw, (kitten_x, kitten_y), kitten_size, (255, 240, 220), (100, 200, 150), (255, 100, 100))
    
    # Sparkles around
    for _ in range(20):
        sparkle_x = random.randint(50, width - 50)
        sparkle_y = random.randint(50, height - 50)
        sparkle_size = random.randint(3, 6)
        draw_circle(draw, (sparkle_x, sparkle_y), sparkle_size, (255, 255, 200))
        draw_circle(draw, (sparkle_x, sparkle_y), sparkle_size // 2, (255, 255, 255))
    
    # Title text (optional, small)
    try:
        font = ImageFont.load_default()
        text = "Cute Friends"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (width - text_width) // 2
        text_y = height - 60
        draw.text((text_x, text_y), text, fill=(100, 80, 60), font=font)
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

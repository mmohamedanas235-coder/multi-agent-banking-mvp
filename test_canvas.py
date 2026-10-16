import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1280
HEIGHT = 720
FPS = 24

FONT_TITLE = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
FONT_SUBTITLE = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 22)
FONT_BODY = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 18)
FONT_MONO = ImageFont.truetype("C:\\Windows\\Fonts\\calibri.ttf", 16)
FONT_BOLD = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 20)

def create_base_canvas():
    img = Image.new("RGB", (WIDTH, HEIGHT), "#070b14")
    draw = ImageDraw.Draw(img)
    # Header bar
    draw.rectangle([0, 0, WIDTH, 60], fill="#0d1322")
    draw.line([0, 60, WIDTH, 60], fill="#1e293b", width=2)
    # Brand
    draw.rectangle([20, 12, 56, 48], fill="#0284c7")
    draw.text((32, 14), "N", font=FONT_TITLE, fill="#ffffff")
    draw.text((70, 18), "NEXUS Core Banking AI — Multi-Agent Operational System", font=FONT_SUBTITLE, fill="#ffffff")
    draw.rectangle([980, 18, 1260, 42], fill="#064e3b", outline="#10b981", width=1)
    draw.text((995, 20), "● ZERO-TRUST AI GATEWAY ACTIVE", font=FONT_MONO, fill="#34d399")
    
    # Footer
    draw.rectangle([0, HEIGHT-35, WIDTH, HEIGHT], fill="#090d16")
    draw.line([0, HEIGHT-35, WIDTH, HEIGHT-35], fill="#1e293b", width=1)
    draw.text((25, HEIGHT-26), "NEXUS Multi-Agent Banking MVP • Submission Demonstration Video • 9-Layer Architecture", font=FONT_MONO, fill="#64748b")
    draw.text((1080, HEIGHT-26), "Target Time: Oct 2026", font=FONT_MONO, fill="#64748b")
    return img, draw

img, draw = create_base_canvas()
img.save("test_frame.png")
print("Base canvas generated successfully! Size:", os.path.getsize("test_frame.png"))
os.remove("test_frame.png")

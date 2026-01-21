"""
Rain simulation with falling droplets.
Run: python toys/rain.py
"""
import sys
import os
import random

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from asciimatics.screen import Screen
from lib.particles import Particle, ParticleSystem


# Rain characters - different intensities
RAIN_CHARS = ["|", "│", "┃", ":", "'", "."]
SPLASH_CHARS = ["·", "°", "˙", "*"]


def rain_demo(screen):
    """Main rain animation loop."""
    system = ParticleSystem(gravity=0.05, wind=0.02, drag=0.01)
    splashes = ParticleSystem(gravity=0.02, drag=0.1)
    
    intensity = 3  # Drops per frame
    
    while True:
        ev = screen.get_key()
        if ev in (ord("q"), ord("Q"), Screen.KEY_ESCAPE):
            return
        if ev == ord("+") or ev == ord("="):
            intensity = min(intensity + 1, 20)
        if ev == ord("-"):
            intensity = max(intensity - 1, 1)
        
        # Spawn new raindrops
        for _ in range(intensity):
            char = random.choice(RAIN_CHARS[:3])
            drop = Particle(
                x=random.uniform(0, screen.width),
                y=0,
                vx=random.uniform(0.1, 0.3),  # Slight wind drift
                vy=random.uniform(1.0, 2.0),
                char=char,
                colour=Screen.COLOUR_CYAN
            )
            system.spawn(drop)
        
        # Check for splashes (drops hitting bottom)
        for p in system.particles:
            if p.y >= screen.height - 2:
                # Create splash particles
                for _ in range(random.randint(1, 3)):
                    splash = Particle(
                        x=p.x,
                        y=screen.height - 1,
                        vx=random.uniform(-0.5, 0.5),
                        vy=random.uniform(-0.3, -0.1),
                        char=random.choice(SPLASH_CHARS),
                        colour=Screen.COLOUR_WHITE,
                        max_age=random.randint(5, 15)
                    )
                    splashes.spawn(splash)
        
        # Update physics
        system.update(screen.width, screen.height)
        splashes.update(screen.width, screen.height)
        
        # Clear and draw
        screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        
        # Draw ground line
        for x in range(screen.width):
            screen.print_at("▁", x, screen.height - 1, colour=Screen.COLOUR_BLUE)
        
        # Draw particles
        system.draw(screen)
        splashes.draw(screen)
        
        # Draw UI
        screen.print_at(f" RAIN  [+/-] intensity: {intensity}  [Q] quit ", 
                       0, 0, colour=Screen.COLOUR_BLACK, bg=Screen.COLOUR_CYAN)
        
        screen.refresh()
        
        # Frame delay
        import time
        time.sleep(0.03)


if __name__ == "__main__":
    Screen.wrapper(rain_demo)

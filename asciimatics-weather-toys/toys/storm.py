"""
Storm simulation with rain, wind, and lightning.
Run: python toys/storm.py
"""
import sys
import os
import random
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from asciimatics.screen import Screen
from lib.particles import Particle, ParticleSystem


RAIN_CHARS = ["|", "│", "/", "\\", ":"]
LIGHTNING_CHARS = ["█", "▓", "░", "╲", "╱", "│", "─"]


class Lightning:
    """A lightning bolt that flashes briefly."""
    
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(10, screen_width - 10)
        self.y = 0
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.age = 0
        self.max_age = random.randint(3, 8)
        self.branches = self._generate_bolt()
    
    def _generate_bolt(self):
        """Generate a jagged lightning bolt path."""
        points = [(self.x, 0)]
        x, y = self.x, 0
        
        while y < self.screen_height - 5:
            # Move down with random horizontal jitter
            y += random.randint(1, 3)
            x += random.randint(-3, 3)
            x = max(0, min(self.screen_width - 1, x))
            points.append((x, y))
            
            # Occasionally branch
            if random.random() < 0.2:
                branch_x, branch_y = x, y
                for _ in range(random.randint(2, 5)):
                    branch_y += 1
                    branch_x += random.choice([-2, -1, 1, 2])
                    branch_x = max(0, min(self.screen_width - 1, branch_x))
                    points.append((branch_x, branch_y))
        
        return points
    
    def update(self):
        self.age += 1
    
    def is_alive(self):
        return self.age < self.max_age
    
    def draw(self, screen):
        # Flash intensity based on age
        if self.age < 2:
            colour = Screen.COLOUR_WHITE
            char = "█"
        else:
            colour = Screen.COLOUR_YELLOW
            char = random.choice(["│", "╲", "╱"])
        
        for x, y in self.branches:
            try:
                screen.print_at(char, int(x), int(y), colour=colour)
            except:
                pass


def storm_demo(screen):
    """Main storm animation loop."""
    rain = ParticleSystem(gravity=0.08, wind=0.15, drag=0.01)
    lightning_bolts = []
    
    intensity = 8
    wind_strength = 0.15
    lightning_chance = 0.02
    flash_timer = 0  # For screen flash effect
    
    while True:
        ev = screen.get_key()
        if ev in (ord("q"), ord("Q"), Screen.KEY_ESCAPE):
            return
        if ev == ord("+") or ev == ord("="):
            intensity = min(intensity + 2, 30)
        if ev == ord("-"):
            intensity = max(intensity - 2, 2)
        if ev == ord("l") or ev == ord("L"):
            # Manual lightning trigger
            lightning_bolts.append(Lightning(screen.width, screen.height))
            flash_timer = 3
        
        rain.wind = wind_strength + random.uniform(-0.05, 0.05)  # Gusty
        
        # Spawn rain
        for _ in range(intensity):
            char = random.choice(RAIN_CHARS)
            drop = Particle(
                x=random.uniform(-20, screen.width + 20),
                y=random.uniform(-5, 0),
                vx=wind_strength * 3 + random.uniform(-0.2, 0.2),
                vy=random.uniform(1.5, 2.5),
                char=char,
                colour=Screen.COLOUR_CYAN
            )
            rain.spawn(drop)
        
        # Random lightning
        if random.random() < lightning_chance:
            lightning_bolts.append(Lightning(screen.width, screen.height))
            flash_timer = 3
        
        # Update rain
        rain.update(screen.width, screen.height)
        
        # Update lightning
        for bolt in lightning_bolts:
            bolt.update()
        lightning_bolts = [b for b in lightning_bolts if b.is_alive()]
        
        # Choose background based on flash
        if flash_timer > 0:
            bg_colour = Screen.COLOUR_WHITE
            flash_timer -= 1
        else:
            bg_colour = Screen.COLOUR_BLACK
        
        screen.clear_buffer(bg_colour, Screen.A_NORMAL, bg_colour)
        
        # Draw clouds (top of screen)
        cloud_char = "▓" if flash_timer > 0 else "░"
        cloud_colour = Screen.COLOUR_WHITE if flash_timer > 0 else Screen.COLOUR_WHITE
        for y in range(3):
            for x in range(screen.width):
                if random.random() < 0.7:
                    screen.print_at(cloud_char, x, y, colour=cloud_colour)
        
        # Draw rain
        rain.draw(screen)
        
        # Draw lightning
        for bolt in lightning_bolts:
            bolt.draw(screen)
        
        # Draw ground
        ground_char = "▁" if flash_timer == 0 else "▔"
        for x in range(screen.width):
            screen.print_at(ground_char, x, screen.height - 1, 
                          colour=Screen.COLOUR_BLUE)
        
        # Draw UI
        screen.print_at(f" STORM  [+/-] intensity: {intensity}  [L] lightning  [Q] quit ", 
                       0, 0, colour=Screen.COLOUR_BLACK, bg=Screen.COLOUR_CYAN)
        
        screen.refresh()
        
        import time
        time.sleep(0.03)


if __name__ == "__main__":
    Screen.wrapper(storm_demo)

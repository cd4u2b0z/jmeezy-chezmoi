"""
Snow simulation with gentle falling flakes.
Run: python toys/snow.py
"""
import sys
import os
import random
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from asciimatics.screen import Screen
from lib.particles import Particle, ParticleSystem


# Snowflake characters
SNOW_CHARS = ["*", "❄", "❅", "❆", "·", "°", "✧", "+", ".", "✦"]


class Snowflake(Particle):
    """Snowflake with sinusoidal drift."""
    
    def __init__(self, *args, drift_amplitude=0.5, drift_frequency=0.1, **kwargs):
        super().__init__(*args, **kwargs)
        self.drift_amplitude = drift_amplitude
        self.drift_frequency = drift_frequency
        self.phase = random.uniform(0, 2 * math.pi)
    
    def update(self, gravity=0.0, wind=0.0, drag=0.0):
        # Add sinusoidal horizontal drift
        drift = self.drift_amplitude * math.sin(self.age * self.drift_frequency + self.phase)
        self.x += drift
        super().update(gravity, wind, drag)


def snow_demo(screen):
    """Main snow animation loop."""
    system = ParticleSystem(gravity=0.01, wind=0.0, drag=0.0)
    
    intensity = 2
    wind_strength = 0.0
    accumulation = [0] * screen.width  # Snow pile height at each x
    
    while True:
        ev = screen.get_key()
        if ev in (ord("q"), ord("Q"), Screen.KEY_ESCAPE):
            return
        if ev == ord("+") or ev == ord("="):
            intensity = min(intensity + 1, 15)
        if ev == ord("-"):
            intensity = max(intensity - 1, 1)
        if ev == Screen.KEY_LEFT:
            wind_strength = max(wind_strength - 0.02, -0.2)
        if ev == Screen.KEY_RIGHT:
            wind_strength = min(wind_strength + 0.02, 0.2)
        if ev == ord("r") or ev == ord("R"):
            accumulation = [0] * screen.width  # Reset snow
        
        system.wind = wind_strength
        
        # Spawn new snowflakes
        for _ in range(intensity):
            char = random.choice(SNOW_CHARS)
            size = random.choice([0.3, 0.5, 0.8, 1.0])  # Depth simulation
            flake = Snowflake(
                x=random.uniform(0, screen.width),
                y=0,
                vx=random.uniform(-0.1, 0.1),
                vy=random.uniform(0.2, 0.5) * size,
                char=char,
                colour=Screen.COLOUR_WHITE,
                drift_amplitude=random.uniform(0.2, 0.8),
                drift_frequency=random.uniform(0.05, 0.15)
            )
            system.spawn(flake)
        
        # Check for accumulation
        new_particles = []
        for p in system.particles:
            ground_level = screen.height - 1 - accumulation[int(p.x) % screen.width]
            if p.y >= ground_level:
                # Accumulate snow (slowly)
                if random.random() < 0.02:  # 2% chance to add to pile
                    idx = int(p.x) % screen.width
                    accumulation[idx] = min(accumulation[idx] + 1, screen.height // 3)
            elif p.is_alive(screen.width, screen.height):
                p.update(system.gravity, system.wind, system.drag)
                new_particles.append(p)
        
        system.particles = new_particles
        
        # Clear and draw
        screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        
        # Draw accumulated snow
        for x in range(screen.width):
            pile_height = accumulation[x]
            for y in range(pile_height):
                screen.print_at("█", x, screen.height - 1 - y, 
                              colour=Screen.COLOUR_WHITE)
        
        # Draw falling snow
        for p in system.particles:
            try:
                screen.print_at(p.char, int(p.x), int(p.y), colour=p.colour)
            except:
                pass
        
        # Draw UI
        wind_indicator = "◀" * int(abs(wind_strength) * 25) if wind_strength < 0 else "▶" * int(wind_strength * 25)
        screen.print_at(f" SNOW  [+/-] intensity: {intensity}  [←/→] wind: {wind_indicator or '○'}  [R] reset  [Q] quit ", 
                       0, 0, colour=Screen.COLOUR_BLACK, bg=Screen.COLOUR_WHITE)
        
        screen.refresh()
        
        import time
        time.sleep(0.05)


if __name__ == "__main__":
    Screen.wrapper(snow_demo)

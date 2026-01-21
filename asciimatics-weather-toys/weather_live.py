#!/usr/bin/env python3
"""
🌦️ Live Weather Animation
Fetches real weather data and displays a matching terminal animation.
Run: python weather_live.py
"""
import sys
import os
import random
import math
import time
from datetime import datetime

from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from lib.weather_api import get_weather, WeatherCondition, WeatherData
from lib.particles import Particle, ParticleSystem


# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTER SETS
# ═══════════════════════════════════════════════════════════════════════════════

RAIN_CHARS = ["│", "|", "┃", ":", "'"]
HEAVY_RAIN_CHARS = ["┃", "║", "│", "|"]
DRIZZLE_CHARS = [".", "·", "'", ","]
SNOW_CHARS = ["*", "❄", "❅", "❆", "·", "°", "✧", "."]
FOG_CHARS = ["░", "▒", "·", ".", " "]
LIGHTNING_CHARS = ["█", "▓", "│", "╲", "╱"]
CLOUD_CHARS = ["█", "▓", "▒", "░"]
STAR_CHARS = ["·", ".", "+", "*", "✦", "✧"]


# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATION EFFECTS
# ═══════════════════════════════════════════════════════════════════════════════

class WeatherAnimation:
    """Base class for weather animations."""
    
    def __init__(self, screen: Screen, weather: WeatherData):
        self.screen = screen
        self.weather = weather
        self.width = screen.width
        self.height = screen.height
        self.frame = 0
    
    def update(self):
        """Update animation state."""
        self.frame += 1
    
    def draw(self):
        """Draw the animation."""
        pass
    
    def draw_ground(self):
        """Draw ground line."""
        for x in range(self.width):
            self.screen.print_at("▁", x, self.height - 1, colour=Screen.COLOUR_BLUE)
    
    def draw_info_bar(self):
        """Draw weather info at top."""
        temp = f"{self.weather.temperature_f:.0f}°F"
        info = f" {self.weather.location} │ {temp} │ {self.weather.description} │ Wind: {self.weather.wind_speed_mph:.0f}mph │ [Q] Quit "
        # Truncate if too long
        if len(info) > self.width:
            info = info[:self.width-1]
        self.screen.print_at(info, 0, 0, colour=Screen.COLOUR_BLACK, bg=Screen.COLOUR_CYAN)


class ClearSkyAnimation(WeatherAnimation):
    """Clear sky with twinkling stars (night) or sun rays (day)."""
    
    def __init__(self, screen: Screen, weather: WeatherData):
        super().__init__(screen, weather)
        self.stars = []
        self.is_night = self._is_night()
        
        # Generate stars for night sky
        if self.is_night:
            for _ in range(int(self.width * self.height * 0.02)):
                self.stars.append({
                    'x': random.randint(0, self.width - 1),
                    'y': random.randint(2, self.height - 3),
                    'char': random.choice(STAR_CHARS),
                    'phase': random.uniform(0, 2 * math.pi),
                    'speed': random.uniform(0.05, 0.15)
                })
    
    def _is_night(self) -> bool:
        hour = datetime.now().hour
        return hour < 6 or hour > 20
    
    def update(self):
        super().update()
    
    def draw(self):
        self.screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        
        if self.is_night:
            # Draw twinkling stars
            for star in self.stars:
                brightness = (math.sin(self.frame * star['speed'] + star['phase']) + 1) / 2
                if brightness > 0.3:
                    colour = Screen.COLOUR_WHITE if brightness > 0.7 else Screen.COLOUR_CYAN
                    self.screen.print_at(star['char'], star['x'], star['y'], colour=colour)
            
            # Draw moon
            moon_x = self.width - 15
            self.screen.print_at("🌙", moon_x, 3, colour=Screen.COLOUR_YELLOW)
        else:
            # Draw sun
            sun_x = self.width // 2 - 5
            sun_y = 4
            sun_art = [
                "    \\   |   /    ",
                "  ─  ░░███░░  ─  ",
                "    ░███████░    ",
                "  ─  ░░███░░  ─  ",
                "    /   |   \\    ",
            ]
            for i, line in enumerate(sun_art):
                self.screen.print_at(line, sun_x, sun_y + i, colour=Screen.COLOUR_YELLOW)
        
        self.draw_ground()
        self.draw_info_bar()


class RainAnimation(WeatherAnimation):
    """Rain with variable intensity based on weather data."""
    
    def __init__(self, screen: Screen, weather: WeatherData):
        super().__init__(screen, weather)
        self.rain = ParticleSystem(gravity=0.05, drag=0.01)
        self.splashes = ParticleSystem(gravity=0.02, drag=0.1)
        
        # Calculate intensity from weather data
        self.intensity = self._calculate_intensity()
        
        # Wind from weather data (convert to animation units)
        wind_dir = 1 if 0 <= weather.wind_direction <= 180 else -1
        self.wind = (weather.wind_speed_mph / 100) * wind_dir
        self.rain.wind = self.wind
        
        self.chars = HEAVY_RAIN_CHARS if weather.condition == WeatherCondition.HEAVY_RAIN else RAIN_CHARS
    
    def _calculate_intensity(self) -> int:
        """Calculate rain intensity from weather data."""
        base = 5
        if self.weather.condition == WeatherCondition.HEAVY_RAIN:
            base = 15
        elif self.weather.condition == WeatherCondition.DRIZZLE:
            base = 2
        
        # Modify by actual rain intensity if available
        if self.weather.rain_intensity > 0:
            base = max(3, min(20, int(self.weather.rain_intensity * 2)))
        
        return base
    
    def update(self):
        super().update()
        
        # Spawn rain drops
        for _ in range(self.intensity):
            char = random.choice(self.chars)
            drop = Particle(
                x=random.uniform(-10, self.width + 10),
                y=random.uniform(-3, 0),
                vx=self.wind * 3 + random.uniform(-0.1, 0.1),
                vy=random.uniform(1.2, 2.0),
                char=char,
                colour=Screen.COLOUR_CYAN
            )
            self.rain.spawn(drop)
        
        # Check for splashes
        for p in self.rain.particles:
            if p.y >= self.height - 2:
                for _ in range(random.randint(1, 2)):
                    splash = Particle(
                        x=p.x,
                        y=self.height - 1,
                        vx=random.uniform(-0.4, 0.4),
                        vy=random.uniform(-0.3, -0.1),
                        char=random.choice(["·", "°"]),
                        colour=Screen.COLOUR_WHITE,
                        max_age=random.randint(5, 10)
                    )
                    self.splashes.spawn(splash)
        
        self.rain.update(self.width, self.height)
        self.splashes.update(self.width, self.height)
    
    def draw(self):
        self.screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        
        # Draw clouds at top
        self._draw_clouds()
        
        self.rain.draw(self.screen)
        self.splashes.draw(self.screen)
        self.draw_ground()
        self.draw_info_bar()
    
    def _draw_clouds(self):
        """Draw cloud layer at top."""
        for y in range(1, 4):
            for x in range(self.width):
                if random.random() < 0.8:
                    char = "▓" if y == 2 else "░"
                    self.screen.print_at(char, x, y, colour=Screen.COLOUR_WHITE)


class SnowAnimation(WeatherAnimation):
    """Snow with drift and accumulation."""
    
    def __init__(self, screen: Screen, weather: WeatherData):
        super().__init__(screen, weather)
        self.snow = ParticleSystem(gravity=0.01, drag=0.0)
        self.accumulation = [0] * self.width
        
        # Calculate intensity
        self.intensity = 3 if weather.condition == WeatherCondition.SNOW else 8
        if weather.snow_intensity > 0:
            self.intensity = max(2, min(15, int(weather.snow_intensity * 3)))
        
        # Wind
        wind_dir = 1 if 0 <= weather.wind_direction <= 180 else -1
        self.wind = (weather.wind_speed_mph / 150) * wind_dir
        self.snow.wind = self.wind
    
    def update(self):
        super().update()
        
        for _ in range(self.intensity):
            char = random.choice(SNOW_CHARS)
            flake = Particle(
                x=random.uniform(0, self.width),
                y=0,
                vx=random.uniform(-0.1, 0.1),
                vy=random.uniform(0.2, 0.5),
                char=char,
                colour=Screen.COLOUR_WHITE
            )
            # Add sinusoidal drift
            flake._drift_phase = random.uniform(0, 2 * math.pi)
            self.snow.spawn(flake)
        
        # Update with drift
        new_particles = []
        for p in self.snow.particles:
            # Sinusoidal drift
            if hasattr(p, '_drift_phase'):
                drift = 0.3 * math.sin(p.age * 0.1 + p._drift_phase)
                p.x += drift
            
            p.update(self.snow.gravity, self.snow.wind, self.snow.drag)
            
            # Check for accumulation
            ground_level = self.height - 1 - self.accumulation[int(p.x) % self.width]
            if p.y >= ground_level:
                if random.random() < 0.015:
                    idx = int(p.x) % self.width
                    self.accumulation[idx] = min(self.accumulation[idx] + 1, self.height // 4)
            elif p.is_alive(self.width, self.height):
                new_particles.append(p)
        
        self.snow.particles = new_particles
    
    def draw(self):
        self.screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        
        # Draw snow accumulation
        for x in range(self.width):
            for y in range(self.accumulation[x]):
                self.screen.print_at("█", x, self.height - 1 - y, colour=Screen.COLOUR_WHITE)
        
        # Draw falling snow
        for p in self.snow.particles:
            try:
                self.screen.print_at(p.char, int(p.x), int(p.y), colour=p.colour)
            except:
                pass
        
        self.draw_info_bar()


class ThunderstormAnimation(WeatherAnimation):
    """Storm with rain, clouds, and lightning."""
    
    def __init__(self, screen: Screen, weather: WeatherData):
        super().__init__(screen, weather)
        self.rain = ParticleSystem(gravity=0.08, drag=0.01)
        self.lightning_bolts = []
        self.flash_timer = 0
        
        # High intensity rain
        self.intensity = 12
        
        # Strong wind
        wind_dir = 1 if 0 <= weather.wind_direction <= 180 else -1
        self.wind = (weather.wind_speed_mph / 60) * wind_dir
        self.rain.wind = self.wind
        
        # Lightning probability based on conditions
        self.lightning_chance = 0.03
    
    def update(self):
        super().update()
        
        # Gusty wind
        self.rain.wind = self.wind + random.uniform(-0.08, 0.08)
        
        # Spawn rain
        for _ in range(self.intensity):
            drop = Particle(
                x=random.uniform(-20, self.width + 20),
                y=random.uniform(-5, 0),
                vx=self.rain.wind * 4 + random.uniform(-0.2, 0.2),
                vy=random.uniform(1.5, 2.5),
                char=random.choice(HEAVY_RAIN_CHARS),
                colour=Screen.COLOUR_CYAN
            )
            self.rain.spawn(drop)
        
        # Random lightning
        if random.random() < self.lightning_chance:
            self.lightning_bolts.append(self._create_lightning())
            self.flash_timer = 4
        
        self.rain.update(self.width, self.height)
        
        # Update lightning
        self.lightning_bolts = [b for b in self.lightning_bolts if b['age'] < b['max_age']]
        for bolt in self.lightning_bolts:
            bolt['age'] += 1
        
        if self.flash_timer > 0:
            self.flash_timer -= 1
    
    def _create_lightning(self):
        """Generate a lightning bolt."""
        x = random.randint(10, self.width - 10)
        points = [(x, 3)]
        
        while points[-1][1] < self.height - 5:
            px, py = points[-1]
            py += random.randint(1, 3)
            px += random.randint(-3, 3)
            px = max(0, min(self.width - 1, px))
            points.append((px, py))
            
            # Branch
            if random.random() < 0.2:
                bx, by = px, py
                for _ in range(random.randint(2, 4)):
                    by += 1
                    bx += random.choice([-2, -1, 1, 2])
                    bx = max(0, min(self.width - 1, bx))
                    points.append((bx, by))
        
        return {'points': points, 'age': 0, 'max_age': random.randint(4, 8)}
    
    def draw(self):
        bg = Screen.COLOUR_WHITE if self.flash_timer > 2 else Screen.COLOUR_BLACK
        self.screen.clear_buffer(bg, Screen.A_NORMAL, bg)
        
        # Draw storm clouds
        cloud_char = "▓" if self.flash_timer > 0 else "░"
        for y in range(1, 5):
            for x in range(self.width):
                if random.random() < 0.8:
                    self.screen.print_at(cloud_char, x, y, colour=Screen.COLOUR_WHITE)
        
        self.rain.draw(self.screen)
        
        # Draw lightning
        for bolt in self.lightning_bolts:
            colour = Screen.COLOUR_WHITE if bolt['age'] < 2 else Screen.COLOUR_YELLOW
            char = "█" if bolt['age'] < 2 else random.choice(["│", "╲", "╱"])
            for px, py in bolt['points']:
                try:
                    self.screen.print_at(char, px, py, colour=colour)
                except:
                    pass
        
        self.draw_ground()
        self.draw_info_bar()


class FogAnimation(WeatherAnimation):
    """Drifting fog banks."""
    
    def __init__(self, screen: Screen, weather: WeatherData):
        super().__init__(screen, weather)
        self.fog_layers = []
        
        # Create fog layers
        for i in range(5):
            layer = {
                'y': self.height // 3 + i * 3,
                'offset': random.uniform(0, 100),
                'speed': random.uniform(0.02, 0.08),
                'density': random.uniform(0.3, 0.7)
            }
            self.fog_layers.append(layer)
    
    def update(self):
        super().update()
        for layer in self.fog_layers:
            layer['offset'] += layer['speed']
    
    def draw(self):
        self.screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        
        # Draw fog layers
        for layer in self.fog_layers:
            for x in range(self.width):
                # Perlin-like noise for fog density
                noise = math.sin((x + layer['offset']) * 0.1) * 0.5 + 0.5
                noise *= math.sin((x + layer['offset']) * 0.03) * 0.3 + 0.7
                
                if noise > (1 - layer['density']):
                    char = "▓" if noise > 0.8 else "░" if noise > 0.5 else "·"
                    colour = Screen.COLOUR_WHITE
                    for dy in range(-1, 2):
                        y = layer['y'] + dy
                        if 2 <= y < self.height - 1:
                            self.screen.print_at(char, x, y, colour=colour)
        
        self.draw_ground()
        self.draw_info_bar()


class CloudyAnimation(WeatherAnimation):
    """Drifting clouds."""
    
    def __init__(self, screen: Screen, weather: WeatherData):
        super().__init__(screen, weather)
        self.clouds = []
        
        # Generate clouds based on cloud coverage
        num_clouds = max(3, int(weather.clouds_percent / 15))
        for _ in range(num_clouds):
            self.clouds.append({
                'x': random.uniform(0, self.width),
                'y': random.randint(3, self.height // 2),
                'width': random.randint(8, 20),
                'height': random.randint(2, 4),
                'speed': random.uniform(0.02, 0.08)
            })
    
    def update(self):
        super().update()
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > self.width + cloud['width']:
                cloud['x'] = -cloud['width']
    
    def draw(self):
        self.screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        
        # Draw clouds
        for cloud in self.clouds:
            cx, cy = int(cloud['x']), cloud['y']
            w, h = cloud['width'], cloud['height']
            
            for dy in range(h):
                indent = abs(dy - h // 2)
                for dx in range(w - indent * 2):
                    x = cx + dx + indent
                    y = cy + dy
                    if 0 <= x < self.width and 2 <= y < self.height - 1:
                        char = "█" if dy == h // 2 else "▓"
                        self.screen.print_at(char, x, y, colour=Screen.COLOUR_WHITE)
        
        self.draw_ground()
        self.draw_info_bar()


# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATION SELECTOR
# ═══════════════════════════════════════════════════════════════════════════════

def get_animation_class(condition: WeatherCondition):
    """Get the appropriate animation class for a weather condition."""
    mapping = {
        WeatherCondition.CLEAR: ClearSkyAnimation,
        WeatherCondition.PARTLY_CLOUDY: CloudyAnimation,
        WeatherCondition.CLOUDY: CloudyAnimation,
        WeatherCondition.FOG: FogAnimation,
        WeatherCondition.DRIZZLE: RainAnimation,
        WeatherCondition.RAIN: RainAnimation,
        WeatherCondition.HEAVY_RAIN: RainAnimation,
        WeatherCondition.FREEZING_RAIN: RainAnimation,
        WeatherCondition.SNOW: SnowAnimation,
        WeatherCondition.HEAVY_SNOW: SnowAnimation,
        WeatherCondition.THUNDERSTORM: ThunderstormAnimation,
        WeatherCondition.UNKNOWN: CloudyAnimation,
    }
    return mapping.get(condition, CloudyAnimation)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def weather_live(screen: Screen):
    """Main weather animation loop."""
    
    # Fetch weather data
    screen.clear()
    screen.print_at("🌦️  Fetching weather data...", 2, 2, colour=Screen.COLOUR_CYAN)
    screen.refresh()
    
    weather = get_weather()
    
    if not weather:
        screen.print_at("❌ Could not fetch weather data. Press any key to exit.", 2, 4, colour=Screen.COLOUR_RED)
        screen.refresh()
        screen.wait_for_input(30)
        return
    
    # Create animation for current weather
    AnimationClass = get_animation_class(weather.condition)
    animation = AnimationClass(screen, weather)
    
    last_fetch = time.time()
    fetch_interval = 300  # Re-fetch every 5 minutes
    
    while True:
        # Handle input
        ev = screen.get_key()
        if ev in (ord('q'), ord('Q'), Screen.KEY_ESCAPE):
            return
        if ev == ord('r') or ev == ord('R'):
            # Force refresh
            weather = get_weather(use_cache=False)
            if weather:
                AnimationClass = get_animation_class(weather.condition)
                animation = AnimationClass(screen, weather)
                last_fetch = time.time()
        
        # Periodic refresh
        if time.time() - last_fetch > fetch_interval:
            new_weather = get_weather(use_cache=False)
            if new_weather and new_weather.condition != weather.condition:
                weather = new_weather
                AnimationClass = get_animation_class(weather.condition)
                animation = AnimationClass(screen, weather)
            last_fetch = time.time()
        
        # Update and draw
        animation.update()
        animation.draw()
        
        screen.refresh()
        time.sleep(0.033)  # ~30 FPS


def main():
    """Entry point."""
    print("🌦️  Live Weather Animation")
    print("Fetching current weather for your location...")
    print("Press [Q] to quit, [R] to refresh\n")
    
    while True:
        try:
            Screen.wrapper(weather_live)
            break
        except ResizeScreenError:
            pass


if __name__ == "__main__":
    main()

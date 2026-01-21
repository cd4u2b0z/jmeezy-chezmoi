# asciimatics-weather-toys

Tiny, self-contained terminal animations and simulations built with Python and **asciimatics**.  
The goal is to create small, expressive, physics-inspired ASCII/ANSI visuals (weather, particles, motion) without heavy frameworks or GUI toolkits.

**🌦️ Now with LIVE WEATHER integration!** Pulls real weather data from OpenWeatherMap API and displays matching animations.

**⚡ Powered by a professional-grade modular engine** with real physics, atmospheric simulation, and AI personality.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Setup (Virtual Environment)](#setup-virtual-environment)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Controls](#controls)
- [Testing](#testing)
- [How It Works](#how-it-works)
- [Engine Architecture](#engine-architecture)
- [Philosophy](#philosophy)

## Features

### Core Features
- **Live Weather Animation** - Fetches real weather and displays matching effects
- **Weather Dashboard** - Full terminal dashboard with sidebar stats + animation (meet **Stormy**, your weather oracle)
- **Multiple Weather Types** - Rain, snow, thunderstorms, fog, clouds, clear sky
- **Easter Egg Creatures** - Rare visitors appear based on weather + time (👻 ghost, 🧚 fairy, 🧜 mermaid)

### Advanced Engine (v2.0)
- **🔬 Physics Engine** - Real Newtonian mechanics with gravity, drag, and wind forces
- **🌡️ Atmospheric Model** - Barometric pressure formula, Pasquill-Gifford stability classification, wind chill & heat index
- **🌀 Procedural Noise** - Perlin, Simplex, Fractal noise + Domain Warping for organic cloud shapes
- **🎭 Personality Engine** - AI mood state machine with memory, callbacks, and weather-aware dialogue
- **📊 Render Stats** - FPS tracking, layer timing, adaptive quality scaling

## Requirements

- Linux or macOS
- Python 3.8+
- Modern terminal emulator (Kitty recommended)

## Quick Start

```bash
# Activate the virtual environment
source .venv/bin/activate

# 🌦️ LIVE WEATHER (fetches real data for your location)
python weather_live.py       # Fullscreen weather animation
python weather_dashboard.py  # Dashboard with stats + animation

# 🎮 STANDALONE TOYS (manual control)
python toys/rain.py          # Rain with splashes
python toys/snow.py          # Snow with accumulation
python toys/storm.py         # Storm with lightning

# 📖 DEMO
python main.py               # Animated title screen
```

## Project Structure

```
asciimatics-weather-toys/
├── config.py              # API keys and settings (edit this!)
├── weather_live.py        # 🌦️ Live weather fullscreen animation
├── weather_dashboard.py   # 📊 Weather dashboard with Stormy AI
├── main.py                # Minimal demo
│
├── engine/                # ⚡ Professional-grade modular engine
│   ├── physics/
│   │   ├── noise.py       # Perlin, Simplex, Fractal, DomainWarp
│   │   ├── particles.py   # Vector2, ParticleSystem, Forces
│   │   └── atmosphere.py  # AtmosphericModel, stability, wind chill
│   ├── rendering/
│   │   └── core.py        # RenderStats, FrameBudget, RenderQueue
│   ├── personality/
│   │   └── core.py        # PersonalityEngine, MoodStateMachine, Memory
│   ├── creatures/         # Easter egg creature system (planned)
│   └── weather/           # Weather processing (planned)
│
├── toys/                  # Individual weather animations
│   ├── rain.py
│   ├── snow.py
│   └── storm.py
│
├── lib/                   # Shared utilities
│   ├── particles.py       # Legacy particle physics
│   └── weather_api.py     # OpenWeatherMap + OpenMeteo client
│
└── tests/
    └── test_engine.py     # 37 unit tests for engine modules
```

## Configuration

Edit `config.py` to customize your location:

```python
# OpenWeatherMap (get free API key at openweathermap.org)
OPENWEATHERMAP_API_KEY = "your_api_key"
OPENWEATHERMAP_CITY_ID = "4597040"  # Your city ID

# Coordinates (for OpenMeteo fallback)
LATITUDE = 32.4840
LONGITUDE = -80.1756
```

## Controls

| Key | Action |
|-----|--------|
| `Q` | Quit |
| `S` or `/` | **Search any location worldwide** |
| `R` | Refresh weather data |
| `F` | Toggle fullscreen (dashboard only) |
| `Space` | Toggle quip mode (Stormy speaks) |
| `A` | View achievements |
| `+/-` | Adjust intensity (toys) |
| `←/→` | Adjust wind (snow toy) |
| `L` | Trigger lightning (storm toy) |

### Location Search

Press `S` or `/` in the dashboard to search for any city worldwide:

```
Examples:
  Summerville, SC
  New York, NY
  San Diego, CA
  Moscow, Russia
  Tokyo, Japan
  London, UK
  Paris, France
```

Uses the same OpenWeatherMap API as your Waybar weather module.

## Testing

```bash
# Run all engine tests (37 tests)
python -m pytest tests/test_engine.py -v

# Quick verification
python -c "from engine import *; print('All engines OK')"
```

## How It Works

1. **Weather API** fetches current conditions from OpenWeatherMap (or OpenMeteo fallback)
2. **Condition Mapping** converts weather codes to animation types
3. **Particle System** simulates rain/snow/etc. with gravity, wind, and drag
4. **Real-time rendering** at ~30 FPS using asciimatics

Weather data is cached for 5 minutes to avoid API rate limits.

## Engine Architecture

The `engine/` module provides professional-grade simulation components:

### 🔬 Physics Engine (`engine/physics/`)

**Noise Generation** - Procedural patterns for organic visuals
```python
from engine.physics.noise import PerlinNoise, SimplexNoise, FractalNoise, DomainWarp

noise = PerlinNoise(seed=42)
value = noise.sample(x, y)  # Ken Perlin's quintic interpolation

# Domain warping for swirling cloud effects
warp = DomainWarp(FractalNoise(), warp_strength=4.0)
organic_value = warp.sample(x, y)
```

**Particle Physics** - Newtonian mechanics with force generators
```python
from engine.physics.particles import ParticleSystem, GravityForce, DragForce, WindForce

system = ParticleSystem(max_particles=1000)
system.add_force_generator(GravityForce(9.81))
system.add_force_generator(DragForce(0.47))
system.add_force_generator(WindForce(wind_x=2.0, wind_y=0.0))
system.update(dt=0.016)  # Euler/Verlet/RK4 integration
```

**Atmospheric Model** - Real meteorological equations
```python
from engine.physics.atmosphere import AtmosphericModel, AtmosphericState

state = AtmosphericState(
    temperature_c=15.0,
    pressure_hpa=1013.25,
    humidity_percent=65.0,
    wind_speed_ms=5.0
)
model = AtmosphericModel(state)

# Barometric formula: P(h) = P₀ × exp(-Mgh/RT)
pressure_at_1km = model.pressure_at_altitude(1000)

# Pasquill-Gifford stability classification
stability = model.classify_stability()  # A (very unstable) to F (stable)

# Feels-like temperature
from engine.physics.atmosphere import calculate_wind_chill, calculate_heat_index
feels_like = calculate_wind_chill(temp_c=5.0, wind_ms=10.0)
```

### 🎨 Rendering Engine (`engine/rendering/`)

```python
from engine.rendering.core import RenderStats, FrameBudget, RenderQueue, RenderLayer

# Performance tracking
stats = RenderStats()
stats.record_frame(frame_time=0.016, particle_count=500)
print(f"FPS: {stats.fps}, P95: {stats.percentile_95}ms")

# Adaptive quality scaling
budget = FrameBudget(target_fps=30)
budget.begin_frame()
# ... render ...
budget.end_frame()  # Auto-adjusts quality_level if over budget

# Layered rendering with z-ordering
queue = RenderQueue()
queue.add(RenderCommand(x=10, y=5, char="*", colour=1, layer=RenderLayer.PRECIPITATION))
queue.execute(screen)
```

### 🎭 Personality Engine (`engine/personality/`)

Stormy's AI personality with mood states and memory:

```python
from engine.personality.core import PersonalityEngine, Mood

engine = PersonalityEngine()

# Mood state machine transitions based on weather
engine.update(weather_type="storm")
print(engine.current_mood)  # Mood.PHILOSOPHICAL, DEADPAN, SARDONIC, etc.

# Weather-aware dialogue
comment = engine.get_weather_comment("thunderstorm")
# "The storm rages. There is wisdom in chaos. Also danger. Mostly danger."

# Meta-aware quips about the simulation
quip = engine.get_quip(meta_chance=0.4)
# "I'm using Perlin noise to render these clouds. Ken Perlin would be proud."

# Memory callbacks for continuity
callback = engine.get_callback()
# "As I said before... [remembered content]"
```

## Philosophy

- One-file toys are encouraged
- No global Python installs
- No GUI frameworks
- Animation logic is explicit and readable
- Characters are treated as particles
- Motion is driven by math, not pre-baked effects
- **Professional architecture** when complexity warrants it

This repo is intentionally small and hackable, but the engine is production-quality.

---

## Setup (Virtual Environment)

### General venv setup (any Python project)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Deactivate when done
deactivate
```

### Setup for this project

```bash
cd asciimatics-weather-toys

# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install asciimatics requests

# Run the dashboard
python weather_dashboard.py
```

### Note
- The `.venv/` folder is NOT included in the repo - you must create it
- Add `.venv/` to `.gitignore` to keep it out of version control
- The dashboard uses all engine modules (`engine/physics`, `engine/rendering`, etc.)


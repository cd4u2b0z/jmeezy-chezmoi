# Changelog

All notable changes to dotfiles will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [1.3.0] - 2026-01-16

### Added
- **Dr. Baklava watermarks** - Hidden and visible attribution throughout configs
- **Credits section** - Acknowledgments for Hyprland, chezmoi, wallust, etc.
- **Inspirational quote** - "The rice is nice, but the workflow is nicer."
- **License section** - MIT license documentation

### Changed
- Waybar layout improvements
- Music player module refinements
- Weather display optimizations

### Fixed
- **update-manager.sh** - Removed "Part 3 done" copy-paste corruption that broke options 4 and Q
- **app-manager.sh** - Removed duplicate Brave browser entry
- **waybar config** - Changed app-tray and music polling interval from 1s to 5s (reduces subprocess overhead)


## [1.2.0] - 2026-01-15

### Added
- **oracle-weather integration** - ASCII weather dashboard in Waybar
- **Music player module** - Spotify/media controls in Waybar
- **Nerd Font glyphs** - Beautiful icons throughout all configs
- **Custom keybinds** - Additional Hyprland shortcuts

### Changed
- Waybar styling for weather integration
- Kitty color scheme refinements
- Fish shell prompt improvements

### Fixed
- Waybar click handlers for oracle-weather
- Font rendering in various applications

## [1.1.0] - 2026-01-14

### Added
- **wallust dynamic theming** - Automatic colorscheme from wallpaper
- **Template variables** - Dynamic color injection into configs
- **Kitty themes** - Terminal colors from wallust
- **Waybar theming** - Bar colors from wallust

### Changed
- Migrated from static colors to wallust-generated palettes
- Improved theme consistency across applications

### Removed
- Static hardcoded colorschemes
- Redundant theme files

## [1.0.0] - 2026-01-13

### Added
- **Initial release** - Complete dotfiles sync from system state
- **Hyprland config** - Full window manager configuration
  - Keybinds for window management
  - Workspace configuration
  - Animation settings
  - Startup applications
- **Waybar config** - Status bar with custom modules
  - Clock module
  - Workspaces
  - System tray
  - Custom scripts
- **Kitty terminal** - GPU-accelerated terminal config
  - Font configuration
  - Colorscheme
  - Keybinds
- **Fish shell** - Modern shell configuration
  - Aliases
  - Functions
  - Prompt customization
- **Rofi** - Application launcher theming
- **chezmoi** - Dotfile management setup

### Infrastructure
- Cross-reference to ansible-system for provisioning
- Structured directory layout
- Template support for dynamic values

---

## Managed Configs

| Config | Description |
|--------|-------------|
| `hyprland/` | Window manager |
| `waybar/` | Status bar |
| `kitty/` | Terminal |
| `fish/` | Shell |
| `rofi/` | Launcher |
| `wallust/` | Theming engine |

---

<sub>Original work by **Dr. Baklava** • [github.com/cd4u2b0z](https://github.com/cd4u2b0z) • 2026</sub>

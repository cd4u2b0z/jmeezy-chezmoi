<!-- Original work by Dr. Baklava • github.com/cd4u2b0z • 2026 -->

# 󰌽 Cdubz's Arch Linux + Hyprland Dotfiles

Dynamic, themeable Arch Linux rice with Hyprland and modern CLI tools.

![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?style=flat&logo=arch-linux&logoColor=white)
![Hyprland](https://img.shields.io/badge/Hyprland-58E1FF?style=flat&logo=wayland&logoColor=black)
![Chezmoi](https://img.shields.io/badge/Chezmoi-4285F4?style=flat&logo=git&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Shell](https://img.shields.io/badge/Shell-Zsh-4EAA25?style=flat&logo=gnu-bash&logoColor=white)

![Desktop Screenshot](assets/screenshot.jpg)


---

## 󰠶 Philosophy: Two Tools, One System

| Tool | Role | Strength |
|------|------|----------|
| **Chezmoi** | **Source of truth** for dotfiles | Daily config edits, templates, cross-machine sync |
| **Ansible** | System provisioner + fallback | Packages, services, full rebuild, disaster recovery |

> **This repo (chezmoi)** manages all user configs. Edit files here for daily use.
> **ansible-system** handles packages/services and pulls from this repo during fresh installs.


### 󰒃 Secrets & Privacy

This repo contains **no secrets**. Sensitive data is handled separately:
- API keys → environment variables or `~/.secrets/` (not tracked)
- SSH keys → manual backup, never in dotfiles
- GPG keys → exported separately, encrypted backup

### 󰈔 .chezmoiignore

Machine-specific files are excluded from sync:
- Systemd symlinks (recreated by `systemctl enable`)
- App state files (`userstate.cbor`, `lazy-lock.json`)
- Backup files (`*.backup*`, `*.bak*`)
- Cache/generated files (`__pycache__/`, `*.pyc`)

## 󰧮 Table of Contents
- [What's Included](#-whats-included)
- [Hyprland Ecosystem](#-hyprland-ecosystem)
  - [Core Components](#core-components-required)
  - [Supporting Libraries](#supporting-libraries-auto-installed-as-dependencies)
  - [Optional Tools](#optional-hypr-tools)
  - [Install Commands](#install-all-hypr-packages)
- [Deploy on New Machine](#-deploy-on-new-machine)
  - [CachyOS (Hyprland Edition)](#cachyos-hyprland-edition)
- [Chezmoi Workflow](#-chezmoi-workflow)
- [Wallust Theming](#-wallust-theming)
- [Key Bindings](#-key-bindings)
  - [Essential](#essential)
  - [Applications](#applications)
  - [Window Navigation](#window-navigation)
  - [Workspaces](#workspaces)
  - [Screenshots](#screenshots)
  - [Volume & Media](#volume--media)
  - [System & Power](#system)
  - [FZF & Zoxide](#fzf-terminal)
- [Structure](#-structure)
- [Troubleshooting](#-troubleshooting)
  - [Quick Fixes](#quick-fixes)
  - [Reloading Services](#reloading-services)
  - [Kill Commands](#kill-commands)
  - [Hyprctl Commands](#hyprctl-commands)
  - [Common Issues](#common-issues)
- [System Info](#-system)

---

## 󰓾 What's Included

| Category | Components |
|----------|------------|
| **WM** | Hyprland (Wayland) |
| **Terminal** | Kitty + Zsh + Starship |
| **Bar** | Waybar |
| **Launcher** | Fuzzel |
| **Notifications** | Mako |
| **Theming** | Wallust (dynamic) |
| **CLI Tools** | fzf, fd, bat, eza, zoxide, ripgrep |

---

## 󱂬 Hyprland Ecosystem

### Core Components (Required)
| Package | Version | Description |
|---------|---------|-------------|
| `hyprland` | 0.53.1 | The Wayland compositor |
| `hypridle` | 0.1.7 | Idle daemon (triggers lock/suspend after inactivity) |
| `hyprlock` | 0.9.2 | GPU-accelerated lock screen |
| `xdg-desktop-portal-hyprland` | 1.3.11 | Portal backend (screen sharing, file pickers) |

### Supporting Libraries (Auto-installed as dependencies)
| Package | Description |
|---------|-------------|
| `hyprcursor` | Cursor theme format and library |
| `hyprgraphics` | Graphics resources and utilities |
| `hyprlang` | Configuration language parser |
| `hyprutils` | Shared utilities across Hypr ecosystem |
| `hyprwayland-scanner` | Wayland protocol code generator |
| `hyprtoolkit` | C++ Wayland-native GUI toolkit |
| `hyprwire` | IPC wire protocol |

### Optional Hypr Tools
| Package | Description | Used? |
|---------|-------------|-------|
| `hyprpaper` | Static wallpaper daemon | ❌ Using swww instead |
| `hyprland-qt-support` | QML styling for Hypr Qt apps | ✅ Installed |
| `hyprland-guiutils` | GUI utilities | ✅ Installed |
| `nwg-displays` | Monitor/display configuration GUI | ✅ Installed |

### Plugins
No Hyprland plugins currently loaded. Vanilla Hyprland setup.

### What's Running
```
Hyprland          # Main compositor
hypridle          # Monitors for idle → triggers lock/sleep
xdg-desktop-portal-hyprland  # Handles screen sharing, file dialogs
swww-daemon       # Wallpaper daemon (animated transitions)
```

### Install All Hypr Packages
```bash
# Core (required)
paru -S hyprland hypridle hyprlock xdg-desktop-portal-hyprland

# Optional tools
paru -S nwg-displays hyprland-qt-support

# Wallpaper (pick one)
paru -S swww       # Animated transitions (recommended)
# paru -S hyprpaper  # Static wallpapers only
```

---

## 󰜎 Deploy on New Machine

### 1. Install Prerequisites
```bash
# Base packages
sudo pacman -S git chezmoi zsh

# Install an AUR helper (pick one)
# Option A: paru
git clone https://aur.archlinux.org/paru.git
cd paru && makepkg -si

# Option B: yay
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si
```

### 2. Apply Dotfiles
```bash
chezmoi init cd4u2b0z/dotfiles --apply
```

### 3. Install Packages
```bash
# Desktop (use paru or yay)
paru -S hyprland waybar kitty mako fuzzel thunar playerctl

# CLI tools
paru -S fzf fd bat eza zoxide ripgrep starship

# Apps
paru -S ncspot fastfetch btop cava spotify-launcher

# Fonts
paru -S ttf-jetbrains-mono-nerd ttf-inter

# Theming
paru -S wallust
```

> **Note**: Replace `paru` with `yay` if you installed yay instead.

### 4. Post-Setup
```bash
# Set zsh as default
chsh -s $(which zsh)

# Enable update timer
systemctl --user daemon-reload
systemctl --user enable --now update-cache.timer

# Apply theme
wallust theme Everforest-Dark-Medium
source ~/.zshrc
```

### CachyOS (Hyprland Edition)

CachyOS uses systemd just like Arch, so everything works the same. Many packages come pre-installed:

```bash
# 1. Install chezmoi and apply
sudo pacman -S chezmoi
chezmoi init cd4u2b0z/dotfiles --apply

# 2. Install what's missing (--needed skips existing)
paru -S --needed zsh starship fzf fd bat eza zoxide ripgrep
paru -S --needed wallust ncspot fastfetch

# 3. Fonts (if not installed)
paru -S --needed ttf-jetbrains-mono-nerd ttf-inter

# 4. Set zsh as default
chsh -s $(which zsh)

# 5. Enable update timer (for Waybar updates module)
systemctl --user daemon-reload
systemctl --user enable --now update-cache.timer

# 6. Apply theme
wallust theme Everforest-Dark-Medium
source ~/.zshrc
```

> **Note**: CachyOS may have its own update notification. You can skip step 5 if you prefer using that instead.

---

## 󰑐 Chezmoi Workflow

### After Making Changes
```bash
# Update single file
chezmoi re-add ~/.zshrc

# Update multiple files
chezmoi re-add ~/.config/hypr/hyprland.conf ~/.config/waybar/style.css

# Add new file to tracking
chezmoi add ~/.config/newapp/config

# Commit and push
chezmoi cd && git add -A && git commit -m "description" && git push
```

### Quick One-Liner
```bash
chezmoi re-add ~/.zshrc && chezmoi cd && git add -A && git commit -m "update zshrc" && git push
```

### On Another Machine
```bash
chezmoi update
```

### Useful Commands
```bash
chezmoi status          # See what's changed
chezmoi diff            # Show all differences
chezmoi diff ~/.zshrc   # Diff single file
chezmoi verify          # Check all files match
chezmoi forget <file>   # Stop tracking file
chezmoi merge <file>    # Interactive merge conflicts
```

---

## 󰉼 Wallust Theming

Switch themes instantly - entire system updates:
```bash
wallust theme Everforest-Dark-Medium
wallust theme Nord
wallust theme Catppuccin-Mocha
wallust theme Dracula
wallust theme list                # List all themes
wallust run /path/to/image.jpg   # Generate from wallpaper
```

**Apps that auto-update:** Kitty, Waybar, Fuzzel, Mako, Hyprland, fzf, ncspot, Starship, tmux, Neovim

### Manual Reload (if needed)
```bash
source ~/.zshrc         # Reload fzf colors
pkill -USR2 waybar      # Reload waybar
makoctl reload          # Reload mako
```

---

## 󰌌 Key Bindings

> `Super` = Windows/Meta key

### Essential
| Key | Action |
|-----|--------|
| `Super + Return` | Terminal (Kitty) |
| `Super + T` | Terminal (alternative) |
| `Super + Q` | Close window |
| `Super + M` | Exit Hyprland |
| `Super + R` | App launcher (Fuzzel) |
| `Super + E` | File manager (Thunar) |
| `Super + V` | Toggle floating |
| `Super + F` | Maximize window |
| `Super + Shift + F` | True fullscreen |

### Applications
| Key | Action |
|-----|--------|
| `Super + B` | Firefox |
| `Super + Shift + B` | Brave |
| `Super + Alt + B` | Brave (alternative) |
| `Super + C` | VS Code |
| `Super + Shift + C` | btop (system monitor) |
| `Super + G` | Steam |
| `Super + Shift + G` | Lutris |
| `Super + .` | fastfetch |
| `Super + ,` | btop |

### Window Navigation
| Key | Action |
|-----|--------|
| `Super + Arrow keys` | Move focus |
| `Super + H/J/K/L` | Move focus (vim-style) |
| `Super + Shift + Arrow` | Move window |
| `Super + Shift + H/J/K/L` | Move window (vim-style) |
| `Super + Ctrl + Arrow` | Resize window |
| `Super + Ctrl + H/J/K/L` | Resize window (vim-style) |
| `Super + U` | Center floating window |

### Workspaces
| Key | Action |
|-----|--------|
| `Super + 1-9` | Switch to workspace |
| `Super + Shift + 1-9` | Move window to workspace |
| `Super + Tab` | Next workspace |
| `Super + Shift + Tab` | Previous workspace |
| `Super + S` | Toggle scratchpad |
| `Super + `` ` | Toggle games workspace |
| `F12` | Dropdown terminal |

### Screenshots
| Key | Action |
|-----|--------|
| `Print` | Fullscreen screenshot |
| `Super + Print` | Area selection |
| `Super + Shift + Print` | Window screenshot |
| `Ctrl + Print` | Fullscreen to clipboard |
| `Super + Shift + S` | Area to file (grim+slurp) |

### Volume & Media
| Key | Action |
|-----|--------|
| `XF86Audio RaiseVolume` | Volume up |
| `XF86Audio LowerVolume` | Volume down |
| `XF86Audio Mute` | Toggle mute |
| `Super + =/-` | Volume up/down |
| `Super + 0` | Toggle mute |
| `XF86Audio Play/Pause` | Play/pause media |
| `XF86Audio Next/Prev` | Next/previous track |

### Waybar Music Player
Dynamic Spotify/ncspot module on the left side of waybar. Auto-hides when no music playing.

| Action | Effect |
|--------|--------|
| **Click** | Play/Pause |
| **Right-click** | Next track |
| **Middle-click** | Previous track |
| **Scroll up/down** | Volume up/down |

**Visual states:**
- 🟢 **Green** = Playing
- ⚫ **Grey italic** = Paused
- 🔴 **Red** = On hover

### Transparency
| Key | Action |
|-----|--------|
| `Ctrl + =` | Increase opacity |
| `Ctrl + -` | Decrease opacity |
| `Super + Shift + T` | Toggle transparency |

### Wallpaper & Themes
| Key | Action |
|-----|--------|
| `Super + W` | Theme switcher menu |
| `Super + Shift + W` | Quick wallpaper picker |
| `Super + Alt + W` | Next wallpaper (slideshow) |
| `Super + Ctrl + W` | Wallpaper status |

### System
| Key | Action |
|-----|--------|
| `Super + Ctrl + L` | Lock screen |
| `Super + Ctrl + S` | Sleep |
| `Super + Ctrl + H` | Hibernate |
| `Super + Ctrl + D` | Display off |
| `Super + Ctrl + P` | Power status |
| `Super + Ctrl + Shift + S` | Shutdown |
| `Super + Ctrl + Shift + R` | Reboot |
| `Super + Shift + Q` | Exit Hyprland |
| `Ctrl + Alt + Delete` | Exit Hyprland |

### Reload
| Key | Action |
|-----|--------|
| `Super + Shift + R` | Reload Hyprland |
| `Super + Alt + R` | Restart Waybar |

### Mouse
| Action | Binding |
|--------|---------|
| `Super + Left Click` | Move window |
| `Super + Right Click` | Resize window |

### FZF (Terminal)
| Key | Action |
|-----|--------|
| `Ctrl + T` | Fuzzy find files |
| `Ctrl + G` | Fuzzy cd into directory |
| `Ctrl + R` | Fuzzy command history |
| `**<Tab>` | Trigger fzf completion |

### Zoxide (Terminal)
```bash
z proj          # Jump to ~/Projects
z dot conf      # Jump to dir matching both words
zi              # Interactive picker with fzf
```

---

## 󰉋 Structure

```
~/.config/
├── hypr/               # Hyprland WM
│   ├── hyprland.conf   # Main config
│   ├── hypridle.conf   # Idle daemon
│   ├── hyprlock.conf   # Lock screen
│   └── scripts/        # Keybind scripts
├── waybar/             # Status bar
│   ├── config          # Modules config
│   ├── style.css       # Styling
│   └── scripts/        # Bar scripts
├── wallust/            # Theme engine
│   ├── wallust.toml    # Config
│   ├── templates/      # Color templates
│   └── scripts/        # Post-theme hooks
├── kitty/              # Terminal
├── mako/               # Notifications
├── fuzzel/             # Launcher
├── nvim/               # Neovim (Lua config)
├── btop/               # System monitor
├── cava/               # Audio visualizer
├── ncspot/             # Spotify TUI
├── ncmpcpp/            # MPD client
├── fastfetch/          # System info
├── tmux/               # Terminal multiplexer
├── starship.toml       # Shell prompt
├── gtk-3.0/            # GTK3 settings
├── gtk-4.0/            # GTK4 settings
├── fontconfig/         # Font settings
├── Thunar/             # File manager
├── MangoHud/           # Game overlay
├── nwg-displays/       # Monitor config
├── systemd/user/       # User services & timers
└── xfce4/              # Thunar settings

~/.local/bin/           # Custom scripts
├── wallpaper-manager   # Wallpaper control
├── theme-switcher      # Theme switching
├── lock-and-sleep      # Lock/sleep/hibernate
├── screenshots/        # Screenshot scripts
└── ...                 # Various utilities

~/.gtkrc-2.0            # GTK2 theme
~/.zshrc                # Shell config
~/.cache/wallust/       # Generated theme files
```

---

## 󰋼 Troubleshooting

### Quick Fixes
| Problem | Solution |
|---------|----------|
| fzf colors not updating | `source ~/.zshrc` |
| Waybar not showing updates | `systemctl --user start update-cache.service` |
| ncspot theme stuck | `~/.config/wallust/scripts/update-ncspot-theme.sh` then restart |
| Chezmoi conflicts | `chezmoi diff <file>` then `chezmoi re-add <file>` |

### Reloading Services

**Hyprland** - Reload config without restarting:
```bash
hyprctl reload
```

**Waybar** - Restart the bar:
```bash
killall waybar && waybar &
# Or just:
pkill -SIGUSR2 waybar    # Reload styles only
```

**Mako** - Reload notifications daemon:
```bash
makoctl reload
```

**Kitty** - Reload config (from within kitty):
```bash
# Press Ctrl+Shift+F5 inside kitty
# Or close and reopen terminal
```

**Wallust** - Regenerate all theme files:
```bash
wallust theme Everforest-Dark-Medium  # Reapply current theme
```

### Why Use `&` (Background Process)

When restarting a GUI app from terminal, use `&` to run it in the background:
```bash
waybar &          # Runs in background, terminal stays usable
waybar            # Blocks terminal until waybar exits (bad)
```

For a clean restart pattern:
```bash
killall waybar && waybar &
```
- `killall waybar` - Stops the running instance
- `&&` - Only continue if kill succeeded
- `waybar &` - Start new instance in background

### Kill Commands

```bash
# Kill by name
killall waybar              # Kill all processes named "waybar"
pkill waybar                # Same thing, pattern matching

# Kill by PID
kill 12345                  # Graceful kill (SIGTERM)
kill -9 12345               # Force kill (SIGKILL) - use as last resort

# Find what's running
pgrep -a waybar             # Show PID and command
ps aux | grep waybar        # Detailed process info
```

### Hyprctl Commands

```bash
# Reload
hyprctl reload                          # Reload config

# Window info
hyprctl activewindow                    # Info about focused window
hyprctl clients                         # List all windows

# Workspaces
hyprctl workspaces                      # List workspaces
hyprctl dispatch workspace 3            # Switch to workspace 3

# Debug
hyprctl version                         # Hyprland version
hyprctl monitors                        # Monitor info
hyprctl layers                          # Layer info (useful for bar issues)

# Live config changes
hyprctl keyword general:gaps_in 10      # Change gaps temporarily
hyprctl keyword decoration:active_opacity 0.9
```

### Common Issues

**Waybar not appearing:**
```bash
hyprctl layers                          # Check if waybar layer exists
killall waybar && waybar &              # Restart it
```

**Screen tearing / stuttering:**
```bash
# Check if VRR is enabled in hyprland.conf
# For NVIDIA, ensure you have proper driver config
```

**Keybind not working:**
```bash
hyprctl binds | grep "your_key"         # Check if bind exists
# Check if another app is capturing the key
```

**App not respecting theme:**
```bash
# Regenerate wallust theme
wallust theme <current-theme>

# Check if app config sources wallust colors
cat ~/.cache/wallust/<app>-colors.*
```

---

## 󰍹 System

- **Resolution**: 3840x2160 (4K @ 1.33x scale)
- **GPU**: NVIDIA RTX 3090
- **Current Theme**: Everforest-Dark-Medium

---

*Managed with chezmoi • Themed with wallust* 󰌽

**— Dr. Baklava**

---

## 󰒋 Related Repository

This dotfiles repo works in tandem with my **Ansible system provisioning**:

| Repository | Purpose |
|------------|---------|
| **[dotfiles](https://github.com/cd4u2b0z/dotfiles)** (this repo) | User configs, themes, keybinds |
| **[ansible-system](https://github.com/cd4u2b0z/ansible-system)** | System packages, services, full rebuild |

### How They Work Together

```
┌─────────────────────────────────────┐
│         Fresh Arch Install          │
└─────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  ansible-playbook -K playbook.yml   │
│  ├─ Installs all packages           │
│  ├─ Enables system services         │
│  └─ Runs: chezmoi init --apply      │◄── Pulls this repo
└─────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│     Full Hyprland System Ready      │
└─────────────────────────────────────┘
```

### Quick Deploy (Full System)

```bash
# From bare Arch install:
sudo pacman -S ansible-core git
git clone https://github.com/cd4u2b0z/ansible-system.git ~/ansible-system
cd ~/ansible-system && ansible-playbook -K playbook.yml
```

### Quick Deploy (Dotfiles Only)

```bash
# If packages already installed:
chezmoi init --apply cd4u2b0z
```

---

## 󰈙 License

MIT License - See [LICENSE](LICENSE) for details.


---

## 󱗗 Credits

- **chezmoi** - Dotfile management made sane
- **Hyprland** - The tiling compositor we deserve
- **Waybar** - Status bar that actually works
- **Kitty** - The terminal that purrs

---

<div align="center">

**"Dotfiles are like snowflakes - no two setups are alike, and both melt under pressure."**

</div>

---

<sub>Original work by **Dr. Baklava** • [github.com/cd4u2b0z](https://github.com/cd4u2b0z) • 2026</sub>

<!-- ZHIuYmFrbGF2YQ== -->

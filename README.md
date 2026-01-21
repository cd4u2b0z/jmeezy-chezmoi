# 🎨 Jmeezy's Dotfiles (Chezmoi)

Dotfiles for CachyOS + Hyprland, managed with chezmoi. Customized for 1080p + GTX 970.

![CachyOS](https://img.shields.io/badge/CachyOS-1793D1?style=flat&logo=arch-linux&logoColor=white)
![Hyprland](https://img.shields.io/badge/Hyprland-58E1FF?style=flat&logo=wayland&logoColor=black)

---

## 🖥️ Hardware Specs

| Component | Spec |
|-----------|------|
| **Motherboard** | ASRock Z97 Extreme 3 |
| **CPU** | Intel i7 4790 |
| **GPU** | NVIDIA GeForce GTX 970 |
| **RAM** | 16GB DDR3 |
| **Resolution** | 1920x1080 (1080p) |

---

## 🚀 Quick Start

```bash
# Install chezmoi if not already installed
sudo pacman -S chezmoi

# Initialize and apply dotfiles
chezmoi init --apply https://github.com/cd4u2b0z/jmeezy-chezmoi.git
```

---

## 📦 What's Included

### Window Manager & Desktop
- **Hyprland** - Wayland compositor config (1080p optimized)
- **Waybar** - Status bar with custom modules
- **Fuzzel** - Application launcher
- **Mako** - Notification daemon
- **Hyprlock/Hypridle** - Lock screen & idle management

### Terminal & Shell
- **Kitty** - GPU-accelerated terminal
- **Zsh** - Shell with plugins
- **Starship** - Cross-shell prompt
- **Tmux** - Terminal multiplexer

### Applications
- **Neovim** - Text editor with LSP
- **Thunar** - File manager
- **btop** - System monitor
- **cava** - Audio visualizer
- **fastfetch** - System info
- **ncspot** - Spotify TUI client
- **ncmpcpp + mpd** - Music player

### Theming
- **Wallust** - Dynamic color theming from wallpapers
- **GTK themes** - Dark mode configured
- **MangoHud** - Gaming overlay

---

## 🔧 Post-Install

After applying dotfiles, you may want to:

1. **Set a wallpaper**:
   ```bash
   # Copy a wallpaper to ~/Pictures/Wallpapers/
   hyprctl hyprpaper wallpaper ",~/Pictures/Wallpapers/your-wallpaper.jpg"
   ```

2. **Generate theme colors** (if using wallust):
   ```bash
   wallust run ~/Pictures/Wallpapers/your-wallpaper.jpg
   ```

3. **Log out and back in** to Hyprland for all changes to take effect.

---

## 📁 Directory Structure

```
~/.config/
├── hypr/          # Hyprland config (1080p monitor)
├── waybar/        # Status bar
├── kitty/         # Terminal
├── nvim/          # Neovim
├── fuzzel/        # App launcher
├── mako/          # Notifications
├── btop/          # System monitor
├── cava/          # Audio visualizer
├── wallust/       # Dynamic theming
└── ...
```

---

## 📝 Credits

Based on [cd4u2b0z/chezmoi](https://github.com/cd4u2b0z/chezmoi), customized for jmeezy's 1080p + GTX 970 setup.

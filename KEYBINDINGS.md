# Keybindings Configuration

## Niri Window Manager

### Default Keybinding (Mod+V)

Add this to your Niri config (`~/.config/niri/cfg/keybinds.kdl`):

```kdl
// Speech-to-Text Keybinding
Mod+V hotkey-overlay-title="Speech to Text" { spawn "~/.local/bin/whisper-stt.sh"; }
```

### Alternative Keybindings

To change the keybinding, modify the hotkey:

```kdl
// Example with different key
Mod+Shift+V hotkey-overlay-title="Speech to Text" { spawn "~/.local/bin/whisper-stt.sh"; }

// Example with function key
F13 hotkey-overlay-title="Speech to Text" { spawn "~/.local/bin/whisper-stt.sh"; }

// Example with Control key
Ctrl+Alt+V hotkey-overlay-title="Speech to Text" { spawn "~/.local/bin/whisper-stt.sh"; }
```

After editing, reload Niri config:

```bash
niri msg action load-config-file
```

## Other Window Managers

### Hyprland

Add to `~/.config/hypr/hyprland.conf`:

```conf
bind = MOD, V, exec, ~/.local/bin/whisper-stt.sh
```

Replace `MOD` with your mod key (e.g., `SUPER`).

### i3/Sway

Add to `~/.config/i3/config` or `~/.config/sway/config`:

```
bindsym $mod+V exec ~/.local/bin/whisper-stt.sh
```

### KDE Plasma

1. Open System Settings → Shortcuts → Custom Shortcuts
2. Add new shortcut → Command/URL
3. Set trigger to Meta+V
4. Set command to `~/.local/bin/whisper-stt.sh`

### GNOME

1. Open Settings → Keyboard → Keyboard Shortcuts
2. Click "+" to add custom shortcut
3. Name: "Speech to Text"
4. Command: `~/.local/bin/whisper-stt.sh`
5. Shortcut: Set to Ctrl+Alt+V (or desired key)

## How to Use

1. **Press your configured key** → Notification: "🎙️ Recording... Press [key] to stop"
2. **Speak clearly** into your microphone
3. **Press the key again** → Notification: "⏳ Processing..." then "✅ Done: [your text]"
4. **Text appears** at your cursor automatically

## Troubleshooting

### Keybinding doesn't work
- Verify the script is executable: `ls -l ~/.local/bin/whisper-stt.sh`
- Check the path in your config matches the actual script location
- Test the script manually: `~/.local/bin/whisper-stt.sh`

### Niri config won't reload
- Check for syntax errors in your config: `niri msg action validate-config`
- Check Niri logs: `journalctl --user -u niri -n 50`

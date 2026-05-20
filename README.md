# Daemon Whisper

"When you whisper into the daemon, the daemon types back"

**CPU-only** local speech-to-text transcription for Linux using Whisper models. Fully offline - your voice never leaves your machine.

## Quick Summary

- **Purpose:** Convert voice to text locally on Linux
- **Backend:** whisper.cpp with CPU-only support
- **Activation:** Mod+V keybinding (configurable)
- **Output:** Auto-typed at cursor using wtype
- **Model:** ggml-small.en.bin (466MB) - can switch to ggml-base.en.bin for speed

## How It Works

1. Press **Mod+V** → Start recording (notification appears)
2. Speak clearly into your microphone
3. Press **Mod+V** again → Stop and transcribe
4. Text appears at your cursor automatically

## Features

- **Toggle recording:** Same key starts/stops recording
- **Visual feedback:** libnotify notifications for recording status
- **Auto-type integration:** Uses wtype to type at cursor position
- **Error handling:** Gracefully handles no-speech detection
- **CPU-only:** No GPU required, works on any Linux system
- **Fully offline:** Your voice data never leaves your machine

## CPU-Only Operation

This project is designed for **CPU-only operation** with no GPU acceleration. The build configuration explicitly disables Vulkan and GPU support:

```bash
cmake -DWHISPER_VULKAN=OFF ..
```

This ensures maximum compatibility and stability across all hardware configurations, including systems with Intel iGPUs or no dedicated GPU. Processing times listed below reflect CPU-only performance.

## Performance

| Size | Parameters | English-only | Multilingual | Required VRAM | Relative Speed |
|-------|-----------|--------------|--------------|---------------|----------------|
| tiny | 39 M | tiny.en | tiny | ~1 GB | ~10x |
| base | 74 M | base.en | base | ~1 GB | ~7x |
| small | 244 M | small.en | small | ~2 GB | ~4x |
| medium | 769 M | medium.en | medium | ~5 GB | ~2x |
| large | 1550 M | N/A | large | ~10 GB | 1x |
| turbo | 809 M | N/A | turbo | ~6 GB | ~8x |

**Model Selection Notes:**
- The **.en models** (English-only) perform better than multilingual models for English transcription
- The difference is most significant for `tiny.en` and `base.en`, less significant for `small.en` and `medium.en`
- The **turbo** model is an optimized version of large-v3 offering faster transcription with minimal accuracy degradation
- Processing times reflect CPU-only performance (slower than GPU benchmarks)

### Recommended Models

- **tiny.en** (~78MB) - Fastest, basic accuracy
- **base.en** (~148MB) - Fast, good accuracy
- **small.en** (~466MB) - Balanced, very good accuracy [recommended for most users]
- **medium.en** (~1.5GB) - Slower, excellent accuracy
- **large** (~3GB) - Best accuracy, multilingual support
- **turbo** (~1.6GB) - Fast + excellent accuracy (optimized large-v3)

## System Requirements

- **Linux OS** with PipeWire or PulseAudio
- **Window Manager** (Niri, Hyprland, i3, Sway, etc.) or Desktop Environment (KDE, GNOME)
- **Dependencies:**
  - `bash` - Shell interpreter
  - `cmake` + build tools - For building whisper.cpp
  - `ffmpeg` - Audio processing
  - `alsa-utils` - Provides `arecord` for audio recording
  - `wtype` - Auto-typing at cursor (Wayland)
  - `libnotify` - Desktop notifications
- **~500MB disk space** - For whisper.cpp and small.en model

## Limitations

- **English-only:** Transcription is hardcoded for English language
- **Wayland-focused:** Uses `wtype` for auto-typing (Wayland). For X11, replace with `xdotool`
- **CPU-only:** No GPU acceleration (by design for stability)

## Installation

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Configuration

See [KEYBINDINGS.md](KEYBINDINGS.md) for keybinding configuration.

## TUI Companion App (Optional)

An optional TUI companion app is available for model management and performance tracking. See [TUI.md](TUI.md) for details.

**Features:**
- View and download Whisper models
- Switch between installed models
- View transcription statistics and CPU usage
- System information display

**Installation:**
```bash
pip install rich psutil
cp whisper-tui.py ~/.local/bin/whisper-tui
chmod +x ~/.local/bin/whisper-tui
```

Run with: `whisper-tui`

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

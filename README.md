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

| Model | Parameters | Size | Speed | Accuracy |
|-------|-----------|------|-------|----------|
| tiny.en | 39M | 78MB | ~10x | Basic |
| base.en | 74M | 148MB | ~7x | Good |
| small.en | 244M | 466MB | ~4x | Very Good |
| medium.en | 769M | 1.5GB | ~2x | Excellent |
| large | 1550M | 3GB | 1x | Best (multilingual) |
| turbo | 809M | 1.6GB | ~8x | Excellent (optimized) |

**Note:** The .en models are English-only and perform better than multilingual models for English. The turbo model is an optimized version of large-v3 with faster speed and minimal accuracy degradation.

### Model Comparison

- **tiny.en** - Fastest, basic accuracy (~78MB)
- **base.en** - Fast, good accuracy (~148MB)
- **small.en** - Balanced, very good accuracy (~466MB) [recommended]
- **medium.en** - Slower, excellent accuracy (~1.5GB)
- **large** - Slowest, best accuracy, multilingual (~3GB)
- **turbo** - Fast (like base), excellent accuracy (~1.6GB)

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

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

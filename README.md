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

| Model | Size | Processing Time | Accuracy |
|-------|------|-----------------|----------|
| tiny.en | 78MB | ~1s | Basic |
| base.en | 148MB | ~1-2s | Good |
| small.en | 466MB | ~2-3s | Very Good |
| medium.en | 1.5GB | ~5-10s | Excellent |

## System Requirements

- Linux with PipeWire/PulseAudio
- Bash shell
- wtype (for auto-typing)
- libnotify (for notifications)
- cmake and build tools

## Installation

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Configuration

See [KEYBINDINGS.md](KEYBINDINGS.md) for keybinding configuration.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

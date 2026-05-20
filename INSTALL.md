# Installation & Setup

## Dependencies

**Required packages for all distros:**
- `cmake` + build tools - Build whisper.cpp
- `ffmpeg` - Audio processing
- `alsa-utils` - Audio recording via arecord
- `wtype` - Auto-typing (Wayland)
- `libnotify` - Desktop notifications

### Arch Linux / Arch-based distributions

```bash
sudo pacman -S cmake base-devel ffmpeg alsa-utils wtype libnotify
```

### Debian / Ubuntu

```bash
sudo apt install cmake build-essential ffmpeg alsa-utils wtype libnotify-bin
```

### Fedora

```bash
sudo dnf install cmake gcc-c++ ffmpeg alsa-utils wtype libnotify
```

## Building whisper.cpp

```bash
# Clone whisper.cpp
cd ~
git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp

# Create build directory
mkdir -p build && cd build

# Configure build (CPU-only, no Vulkan)
cmake -DWHISPER_VULKAN=OFF ..

# Build
make -j$(nproc)
```

## Download Model

```bash
cd ~/whisper.cpp
./models/download-ggml-model.sh small.en
```

### Available Models

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

**Recommendation:** Use English-only models (.en) for English transcription. The `turbo` model offers the best speed/accuracy tradeoff if you have ~1.6GB to spare.

## Install Script

```bash
# Copy script to bin directory
cp whisper-stt.sh ~/.local/bin/

# Make executable
chmod +x ~/.local/bin/whisper-stt.sh
```

## File Locations

After installation, your files should be at:

```
~/.local/bin/whisper-stt.sh          # Main script
~/whisper.cpp/                       # Source code
~/whisper.cpp/models/ggml-*.bin      # Models
~/whisper.cpp/build/bin/whisper-cli  # Binary
```

## Model Selection

Edit `~/.local/bin/whisper-stt.sh` to change the model:

```bash
# Better accuracy (466MB) - Default
MODEL="$HOME/whisper.cpp/models/ggml-small.en.bin"

# Faster, less accurate (148MB)
# MODEL="$HOME/whisper.cpp/models/ggml-base.en.bin"
```

## Testing

Test the script manually:

```bash
~/.local/bin/whisper-stt.sh
```

You should see a notification indicating recording has started. Run it again to stop and transcribe.

## Troubleshooting

### Script doesn't run
- Ensure it's executable: `chmod +x ~/.local/bin/whisper-stt.sh`
- Check the script path is correct

### No audio recorded
- Verify microphone is working: `pactl list sources`
- Check arecord can access your mic: `arecord -f S16_LE -r 16000 -c 1 -D pipewire test.wav`

### Transcription fails
- Ensure whisper.cpp was built successfully
- Check the model file exists: `ls ~/whisper.cpp/models/`
- Test whisper-cli directly: `~/whisper.cpp/build/bin/whisper-cli -m ~/whisper.cpp/models/ggml-small.en.bin -f test.wav`

### Text doesn't appear at cursor
- Ensure wtype is installed: `which wtype`
- Test wtype: `echo "test" | wtype -`

### Notifications don't appear
- Ensure libnotify is installed
- Check notify-send works: `notify-send "Test" "Notification"`

## TUI Companion App (Optional)

An optional TUI companion app is available for easier model management and performance tracking.

### Install Dependencies

```bash
# Required
pip install rich

# Optional (for CPU statistics)
pip install psutil
```

### Install TUI App

```bash
# Copy to bin directory
cp whisper-tui.py ~/.local/bin/whisper-tui

# Make executable
chmod +x ~/.local/bin/whisper-tui
```

### Run TUI App

```bash
whisper-tui
```

See [TUI.md](TUI.md) for full documentation.

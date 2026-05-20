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

| Model | Parameters | Size | Speed | Description |
|-------|-----------|------|-------|-------------|
| **English-only models** |
| tiny.en | 39M | 78MB | ~10x | Fastest, basic accuracy |
| base.en | 74M | 148MB | ~7x | Fast, good accuracy |
| small.en | 244M | 466MB | ~4x | Balanced, very good accuracy (recommended) |
| medium.en | 769M | 1.5GB | ~2x | Slower, excellent accuracy |
| **Multilingual models** |
| tiny | 39M | 78MB | ~10x | Fastest, supports all languages |
| base | 74M | 148MB | ~7x | Fast, supports all languages |
| small | 244M | 466MB | ~4x | Balanced, supports all languages |
| medium | 769M | 1.5GB | ~2x | Slower, supports all languages |
| large | 1550M | 3GB | 1x | Best accuracy, multilingual |
| **Optimized model** |
| turbo | 809M | 1.6GB | ~8x | Fast + excellent accuracy (optimized large-v3) |

**Recommendation:** Use English-only models (.en) for English transcription - they perform better than multilingual models. The `turbo` model offers the best speed/accuracy tradeoff if you have ~1.6GB to spare.

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

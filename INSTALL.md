# Installation & Setup

## Dependencies

### Arch Linux / Arch-based distributions

```bash
sudo pacman -S cmake base-devel ffmpeg wtype libnotify
```

### Debian / Ubuntu

```bash
sudo apt install cmake build-essential ffmpeg wtype libnotify-bin
```

### Fedora

```bash
sudo dnf install cmake gcc-c++ ffmpeg wtype libnotify
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

Available models:
- `tiny.en` (78MB) - Fastest, basic accuracy
- `base.en` (148MB) - Fast, good accuracy
- `small.en` (466MB) - Balanced, very good accuracy (recommended)
- `medium.en` (1.5GB) - Slower, excellent accuracy

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

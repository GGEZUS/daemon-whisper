# TUI Companion App

The **TUI Companion App** is an optional tool for managing Whisper models and viewing performance statistics. It is **NOT required** for the core functionality to work.

## Features

- **Model Management**
  - View all available Whisper models with specifications
  - Download models directly from the interface
  - Switch between installed models
  - Track currently active model

- **Performance Tracking**
  - View last transcription details (timestamp, text, duration)
  - Processing time statistics
  - CPU usage information

- **System Information**
  - CPU usage and frequency
  - Memory availability
  - Required tools verification

## Installation

### Dependencies

```bash
# Python TUI library
pip install rich

# Optional: for CPU statistics
pip install psutil
```

### Setup

```bash
# Copy to your bin directory
cp whisper-tui.py ~/.local/bin/whisper-tui

# Make executable
chmod +x ~/.local/bin/whisper-tui
```

## Usage

Run the TUI app:

```bash
whisper-tui
```

### Menu Options

1. **View all models** - Display table of all available models with specifications
2. **Download a model** - Download a model using whisper.cpp's download script
3. **Switch model** - Change the active model in whisper-stt.sh
4. **View system info** - Display CPU, memory, and tools status
5. **Refresh status** - Reload current status from system
6. **Exit** - Quit the TUI app

## Performance Logging

The main script (`whisper-stt.sh`) automatically logs transcription data to `/tmp/whisper_stt_log.json` including:

- Timestamp of transcription
- Model used
- Processing time
- CPU usage during transcription
- Transcribed text

The TUI app reads this log file to display the last transcription information.

## Model Specifications

| Size | Parameters | English-only | Multilingual | VRAM | Speed |
|-------|-----------|--------------|--------------|------|-------|
| tiny | 39 M | tiny.en | tiny | ~1 GB | ~10x |
| base | 74 M | base.en | base | ~1 GB | ~7x |
| small | 244 M | small.en | small | ~2 GB | ~4x |
| medium | 769 M | medium.en | medium | ~5 GB | ~2x |
| large | 1550 M | N/A | large | ~10 GB | 1x |
| turbo | 809 M | N/A | turbo | ~6 GB | ~8x |

## Troubleshooting

### TUI won't start
- Ensure Python 3 is installed: `python3 --version`
- Install required dependencies: `pip install rich psutil`

### Can't download models
- Ensure whisper.cpp is installed at `~/whisper.cpp`
- Check internet connection
- Verify the download script exists: `ls ~/whisper.cpp/models/download-ggml-model.sh`

### No transcription logs
- Check if log file exists: `ls /tmp/whisper_stt_log.json`
- Ensure you've run the main script at least once
- Check file permissions

### Model switch not working
- Ensure whisper-stt.sh exists at `~/.local/bin/whisper-stt.sh`
- Check file is writable
- Reload any running instances after switching

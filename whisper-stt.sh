#!/bin/bash

# Whisper Speech-to-Text Toggle Script
# Local speech-to-text transcription using whisper.cpp
# Press key once to start recording, press again to stop and transcribe

# Configuration
MODEL="$HOME/whisper.cpp/models/ggml-small.en.bin"
# MODEL="$HOME/whisper.cpp/models/ggml-base.en.bin"  # Faster, less accurate (148MB)
WHISPER="$HOME/whisper.cpp/build/bin/whisper-cli"
AUDIO_FILE="/tmp/whisper_recording.wav"
PID_FILE="/tmp/whisper_stt.pid"

# Check if already recording
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        # Stop recording and transcribe
        kill "$PID"
        rm "$PID_FILE"
        notify-send -i microphone "Speech to Text" "⏳ Processing..."

        # Wait a moment for recording to finish
        sleep 0.5

        # Transcribe with whisper.cpp
        if [ -f "$AUDIO_FILE" ]; then
            TEXT=$($WHISPER -m "$MODEL" -f "$AUDIO_FILE" -nt -l en 2>&1 | grep -v "^whisper_" | grep -v "^main:" | grep -v "^system_info:" | grep -v "^ggml_" | sed 's/^\s*//' | sed 's/\s*$//' | tr -s ' ' | grep -v "^[[:space:]]*$" | head -1)

            if [ -n "$TEXT" ]; then
                # Type the text using wtype
                echo "$TEXT" | wtype -
                notify-send -i checkmark "Speech to Text" "✅ Done: $TEXT"
            else
                notify-send -i error "Speech to Text" "❌ No speech detected"
            fi

            # Clean up
            rm "$AUDIO_FILE"
        fi
    else
        # PID file exists but process is dead
        rm "$PID_FILE"
    fi
else
    # Start recording
    notify-send -i microphone "Speech to Text" "🎙️ Recording... Press Mod+V to stop"

    # Use arecord for proper WAV format
    arecord -f S16_LE -r 16000 -c 1 -D pipewire "$AUDIO_FILE" &

    # Save PID
    echo $! > "$PID_FILE"
fi

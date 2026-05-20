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
START_TIME_FILE="/tmp/whisper_stt_start_time"
LOG_FILE="/tmp/whisper_stt_log.json"

# Function to get current CPU usage
get_cpu_usage() {
    # Get CPU stats before and after
    local cpu_before=($(grep '^cpu ' /proc/stat))
    sleep 0.1
    local cpu_after=($(grep '^cpu ' /proc/stat))

    # Calculate difference
    local idle_diff=$((cpu_after[4] - cpu_before[4]))
    local total_diff=0
    for i in 1 2 3 4; do
        total_diff=$((total_diff + cpu_after[i] - cpu_before[i]))
    done

    if [ $total_diff -gt 0 ]; then
        echo "100" | awk "{printf \"%.1f\", (100 - ($idle_diff * 100 / $total_diff))}"
    else
        echo "0.0"
    fi
}

# Function to log transcription
log_transcription() {
    local text="$1"
    local processing_time="$2"
    local cpu_usage="$3"
    local model_name=$(basename "$MODEL" .bin)

    # Create log entry
    local log_entry=$(cat <<EOF
{
  "timestamp": "$(date -Iseconds)",
  "model": "$model_name",
  "processing_time": $processing_time,
  "cpu_usage": $cpu_usage,
  "text": "$text"
}
EOF
)

    # Create log file if it doesn't exist
    if [ ! -f "$LOG_FILE" ]; then
        echo "[]" > "$LOG_FILE"
    fi

    # Append log entry (using temporary file for safety)
    local temp_file="/tmp/whisper_stt_log_temp.json"
    if command -v jq &> /dev/null; then
        jq ". += [$log_entry]" "$LOG_FILE" > "$temp_file" && mv "$temp_file" "$LOG_FILE"
    else
        # Fallback without jq (simple append, not proper JSON array)
        echo "$log_entry" >> "$LOG_FILE"
    fi
}

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

        # Calculate audio duration
        local start_time=0
        if [ -f "$START_TIME_FILE" ]; then
            start_time=$(cat "$START_TIME_FILE")
            rm "$START_TIME_FILE"
        fi
        local end_time=$(date +%s)
        local audio_duration=$((end_time - start_time))

        # Transcribe with whisper.cpp
        if [ -f "$AUDIO_FILE" ]; then
            # Get CPU before transcription
            local cpu_before=$(get_cpu_usage)

            # Start transcription timer
            local transcribe_start=$(date +%s.%N)

            TEXT=$($WHISPER -m "$MODEL" -f "$AUDIO_FILE" -nt -l en 2>&1 | grep -v "^whisper_" | grep -v "^main:" | grep -v "^system_info:" | grep -v "^ggml_" | sed 's/^\s*//' | sed 's/\s*$//' | tr -s ' ' | grep -v "^[[:space:]]*$" | head -1)

            # End transcription timer
            local transcribe_end=$(date +%s.%N)
            local processing_time=$(echo "$transcribe_end - $transcribe_start" | bc)

            # Get CPU after transcription
            local cpu_after=$(get_cpu_usage)

            if [ -n "$TEXT" ]; then
                # Type the text using wtype
                echo "$TEXT" | wtype -
                notify-send -i checkmark "Speech to Text" "✅ Done: $TEXT"

                # Log transcription (optional - only if LOG_FILE is writable)
                log_transcription "$TEXT" "$processing_time" "$cpu_after" 2>/dev/null
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

    # Record start time
    date +%s > "$START_TIME_FILE"

    # Use arecord for proper WAV format
    arecord -f S16_LE -r 16000 -c 1 -D pipewire "$AUDIO_FILE" &

    # Save PID
    echo $! > "$PID_FILE"
fi

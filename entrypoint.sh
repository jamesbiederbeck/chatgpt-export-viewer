#!/bin/bash
set -euo pipefail

CHATS_DIR="/app/chats"

do_init() {
    local zip_file
    zip_file=$(find "$CHATS_DIR" -maxdepth 1 -name "*.zip" | head -1)

    if [ -z "$zip_file" ]; then
        echo "ERROR: No zip file found in $CHATS_DIR" >&2
        return 1
    fi

    echo "Unpacking $zip_file..."
    unzip -o "$zip_file" -d "$CHATS_DIR" || { echo "ERROR: Failed to unzip $zip_file" >&2; return 1; }

    echo "Merging conversation shards..."
    jq -s 'add' "$CHATS_DIR"/conversations-*.json > /app/conversations.json \
        || { echo "ERROR: jq merge failed" >&2; return 1; }

    echo "Splitting chats..."
    python /app/split_chats.py \
        || { echo "ERROR: split_chats.py failed" >&2; return 1; }

    touch "$CHATS_DIR/.initcomplete"
    echo "Init complete."
}

if [ -f "$CHATS_DIR/.initcomplete" ]; then
    echo "Already initialized, starting server..."
else
    zip_count=$(find "$CHATS_DIR" -maxdepth 1 -name "*.zip" | wc -l)
    other_count=$(find "$CHATS_DIR" -maxdepth 1 -mindepth 1 ! -name "*.zip" ! -name ".initcomplete" | wc -l)

    if [ "$zip_count" -eq 1 ] && [ "$other_count" -eq 0 ]; then
        echo "Fresh data dir detected, running init..."
        if ! do_init; then
            echo "ERROR: Init failed." >&2
            exit 1
        fi
    elif [ "$other_count" -gt 0 ]; then
        echo "WARNING: Partial state detected (no .initcomplete). Retrying init..." >&2
        if ! do_init; then
            echo "ERROR: Init retry failed. Manual cleanup of $CHATS_DIR may be required." >&2
            exit 1
        fi
    else
        echo "ERROR: $CHATS_DIR contains no zip file and is not initialized." >&2
        echo "       Place a ChatGPT export zip in $CHATS_DIR and restart." >&2
        exit 1
    fi
fi

exec python /app/server.py

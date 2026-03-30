# ChatGPT Export Viewer

![ChatGPT Export Viewer Preview](app-preview.png)

A web application for viewing ChatGPT chat history exported from ChatGPT. Provides a convenient interface for browsing and searching through your exported chat conversations.

## Features

- Browse and search all your chats
- Images, audio, and transcriptions rendered inline
- Deep-linkable URLs per chat (`/chat/<id>`)
- Dark theme support

## Quick start (Docker)

1. Clone the repository:
```bash
git clone https://github.com/sugrarin/chatgpt-export-viewer.git
cd chatgpt-export-viewer
```

2. Export your ChatGPT data: **Settings → Data Controls → Export data**, then place the downloaded `.zip` in a `data/` directory:
```bash
mkdir data
cp ~/Downloads/chatgpt-export-*.zip data/
```

3. Start the container:
```bash
docker compose up
```

On first start, the container automatically unpacks the zip, merges conversation shards, and splits chats. A `.initcomplete` sentinel is written so subsequent restarts skip init.

4. Open `http://localhost:8000`

## Manual setup (no Docker)

1. Clone the repo (same as above).

2. Export your ChatGPT data and copy `conversations.json` to the project root.

3. Split conversations into individual files:
```bash
python split_chats.py
```

4. Start the server:
```bash
python server.py
```

5. Open `http://localhost:8000`

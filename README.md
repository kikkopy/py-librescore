# py-librescore

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library and CLI tool for downloading sheet music from MuseScore.

> **Note**: This project is inspired by [LibreScore/dl-librescore](https://github.com/LibreScore/dl-librescore/) and developed by [kikkopy](https://github.com/kikkopy).

## Features

- 📄 Download scores as PDF
- 🎵 Export as MIDI
- 🔊 Export as MP3 audio
- 🖼️ Generate PDF from score images
- 🚀 Parallel downloading
- 📊 Progress tracking
- 🔍 Metadata extraction

## Installation

### From PyPI
```bash
pip install py-librescore
```

### From source
```bash
git clone https://github.com/kikkopy/py-librescore
cd py-librescore
pip install .
```

## Quick Start

### Command Line Interface

```bash
# Download a score as PDF
py-librescore "https://musescore.com/user/123/scores/456" pdf

# Download multiple formats
py-librescore "https://musescore.com/user/123/scores/456" pdf midi mp3

# Specify output directory
py-librescore "URL" pdf -o ~/Downloads

# Enable verbose output and custom workers
py-librescore "URL" pdf midi -v -w 10
```

### Python API

```python
from py_librescore import MuseScore, FileType
from pathlib import Path

# Initialize client
ms = MuseScore()

# Get score metadata
score = ms.get_score("https://musescore.com/user/123/scores/456")

print(f"Title: {score.title}")
print(f"ID: {score.id}")
print(f"Pages: {score.page_count}")

# Download PDF with progress
def progress_callback(current, total):
    print(f"Progress: {current}/{total}")

pdf_file = score.download(FileType.PDF, progress_callback=progress_callback)

# Save to file
score.save(FileType.PDF, Path("./scores"))

# Download all formats
files = score.download_all([FileType.PDF, FileType.MIDI, FileType.MP3])
```

## Supported Formats

| Format | Description | File Extension |
|--------|-------------|----------------|
| PDF | Portable Document Format | `.pdf` |
| MIDI | Musical Instrument Digital Interface | `.mid` |
| MP3 | Audio format | `.mp3` |

## Documentation

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md).

## Legal Notice

This tool is for personal and educational use only. Please respect:
- MuseScore's Terms of Service
- Copyright laws
- Composers' and arrangers' rights

Only download scores that you have legal access to.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by [LibreScore/dl-librescore](https://github.com/LibreScore/dl-librescore/)
- Built with Python and love for music

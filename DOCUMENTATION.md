
# py-librescore Documentation

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Command Line Usage](#command-line-usage)
4. [Python API](#python-api)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)
7. [API Reference](#api-reference)

## Overview

py-librescore is a Python library that provides programmatic access to download sheet music from MuseScore. It supports multiple file formats and offers both CLI and Python API interfaces.

### How It Works

The library works by:
1. Fetching score metadata from MuseScore URLs
2. Authenticating with MuseScore's API
3. Downloading score data in various formats
4. Converting images to PDF when necessary

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Basic Installation

```bash
pip install py-librescore
```

### Development Installation

```bash
git clone https://github.com/kikkopy/py-librescore
cd py-librescore
pip install -e .
```

### Dependencies

- `requests`: HTTP requests
- `reportlab`: PDF generation
- `Pillow`: Image processing

## Command Line Usage

### Basic Syntax

```bash
py-librescore [OPTIONS] URL [FORMATS...]
```

### Examples

**Download a single format:**
```bash
py-librescore "https://musescore.com/user/123/scores/456" pdf
```

**Download multiple formats:**
```bash
py-librescore "https://musescore.com/user/123/scores/456" pdf midi mp3
```

**Custom output directory:**
```bash
py-librescore "URL" pdf -o ~/Documents/scores
```

**Verbose output with progress:**
```bash
py-librescore "URL" pdf -v -w 8
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output DIR` | Output directory | Current directory |
| `-v, --verbose` | Enable verbose output | False |
| `-w, --workers NUM` | Number of parallel workers | 5 |
| `--version` | Show version and exit | - |

## Python API

### Core Classes

#### MuseScore

Main entry point for the library.

```python
from py_librescore import MuseScore

# Initialize with default settings
ms = MuseScore()

# Initialize with custom workers
ms = MuseScore(max_workers=10)
```

#### Score

Represents a MuseScore score with metadata and download capabilities.

```python
# Get a score
score = ms.get_score("https://musescore.com/user/123/scores/456")

# Access metadata
print(score.id)        # Score ID
print(score.title)     # Score title  
print(score.page_count) # Number of pages
print(score.is_official) # Whether it's an official score
```

#### FileType

Enumeration of supported file formats.

```python
from py_librescore import FileType

FileType.PDF    # PDF format
FileType.MIDI   # MIDI format
FileType.MP3    # MP3 format
```

### Basic Usage

#### Downloading Single Files

```python
# Download PDF
pdf_file = score.download(FileType.PDF)

# Download with progress callback
def progress(current, total):
    print(f"Downloaded {current}/{total} pages")

pdf_file = score.download(FileType.PDF, progress_callback=progress)
```

#### Downloading Multiple Files

```python
# Download all supported formats
files = score.download_all()

# Download specific formats
files = score.download_all([FileType.PDF, FileType.MIDI])
```

#### Saving Files

```python
from pathlib import Path

# Save a single file
score.save(FileType.PDF, Path("./output"))

# Save all downloaded files
for file_type in score._files:
    score.save(file_type, Path("./output"))
```

### Advanced Usage

#### Custom Progress Callbacks

```python
def detailed_progress(current, total):
    percent = (current / total) * 100
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '─' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {percent:.1f}% ({current}/{total})', end='')

score.download(FileType.PDF, progress_callback=detailed_progress)
```

#### Error Handling

```python
from py_librescore.exceptions import (
    ScoreNotFoundException,
    AuthenticationException,
    DownloadException
)

try:
    score = ms.get_score("https://musescore.com/invalid-url")
    pdf_file = score.download(FileType.PDF)
except ScoreNotFoundException as e:
    print(f"Score not found: {e}")
except AuthenticationException as e:
    print(f"Authentication failed: {e}")
except DownloadException as e:
    print(f"Download failed: {e}")
```

#### File Information

```python
pdf_file = score.download(FileType.PDF)

print(f"File type: {pdf_file.file_type}")
print(f"Filename: {pdf_file.filename}")
print(f"Size: {pdf_file.size} bytes")
print(f"SHA256: {pdf_file.sha256}")
print(f"MD5: {pdf_file.md5}")
```

## Advanced Usage

### Custom Session Configuration

```python
import requests
from py_librescore import MuseScore

# Create custom session
session = requests.Session()
session.headers.update({
    'User-Agent': 'My Custom User Agent/1.0',
    'Accept-Language': 'fr-FR;q=0.9'
})

# Use custom session (advanced - internal API)
ms = MuseScore(max_workers=5)
ms._downloader.session = session
```

### Batch Processing

```python
from pathlib import Path
from py_librescore import MuseScore

def download_batch(urls, output_dir):
    ms = MuseScore()
    output_path = Path(output_dir)
    
    for url in urls:
        try:
            print(f"Processing: {url}")
            score = ms.get_score(url)
            score.download_all()
            
            for file_type in score._files:
                score.save(file_type, output_path / str(score.id))
                
            print(f"Completed: {score.title}")
            
        except Exception as e:
            print(f"Failed {url}: {e}")

# Usage
urls = [
    "https://musescore.com/user/123/scores/456",
    "https://musescore.com/user/123/scores/789",
]
download_batch(urls, "./batch_downloads")
```

## Troubleshooting

### Common Issues

**Score Not Found**
- Verify the URL is correct and accessible
- Check if the score requires login or subscription
- Ensure the score is public

**Authentication Errors**
- MuseScore may have updated their API
- Try again later as this may be temporary

**Download Failures**
- Check your internet connection
- Verify there's enough disk space
- Try with fewer workers (`-w 2`)

**PDF Generation Issues**
- Ensure Pillow and reportlab are properly installed
- Try with verbose mode for more information

### Debug Mode

Enable verbose output to see detailed information:

```bash
py-librescore "URL" pdf -v
```

Or in Python:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Reference

### MuseScore Class

**`__init__(max_workers: int = 5)`**
- `max_workers`: Number of parallel workers for PDF generation

**`get_score(url: str) -> Score`**
- `url`: MuseScore URL
- Returns: Score object

### Score Class

**Properties:**
- `id`: Score ID
- `title`: Score title
- `page_count`: Number of pages
- `is_official`: Whether it's an official score

**Methods:**

**`download(file_type: FileType, progress_callback: Optional[Callable] = None) -> ScoreFile`**
- Download a specific file format

**`download_all(file_types: Optional[List[FileType]] = None, progress_callback: Optional[Callable] = None) -> Dict[FileType, ScoreFile]`**
- Download multiple file formats

**`save(file_type: FileType, output_dir: Path) -> Path`**
- Save downloaded file to disk

### ScoreFile Class

Represents a downloaded file with metadata.

**Properties:**
- `file_type`: FileType enum
- `url`: Download URL
- `filename`: Suggested filename
- `data`: File content as bytes
- `size`: File size in bytes
- `sha256`: SHA256 hash
- `md5`: MD5 hash

**Methods:**

**`set_data(data: bytes)`**
- Set file data and calculate hashes

**`save(path: Path)`**
- Save file to specific path

## Legal and Ethical Considerations

- Only download scores you have legal access to
- Respect MuseScore's Terms of Service
- Support composers by purchasing official scores when possible
- This tool is for educational and personal use

## Support

For issues and questions:
1. Check this documentation
2. Search existing GitHub issues
3. Create a new issue with detailed information

## Changelog

### Version 1.0.0
- Initial release
- Support for PDF, MIDI, MP3 formats
- CLI and Python API
- Parallel downloading

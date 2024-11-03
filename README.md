# Movie chapters
A simple Python script to add chapters to movies based on timestamps read from text file

## Requirements
- Tested under Ubuntu 24.04
- Python 3 intepreter
- FFMPEG command line (can be installed with `sudo apt install ffmpeg`)

## Installation
Just copy the script into a folder abd run it from terminal (tested on Linux Mint based on Ubuntu 22.04)

(*optional: create a Python Virtual Environment to run the script inside it*)

## Usage
`python3 add_chapters.py <input> <chapters> <output>`

- `input`: Input video files in any format accepted by FFMPEG
- `chapters`: Text file with each line containing the timestamp `hh:mm:ss` format) and the chapter title, like the following example:
```
00:00:00 Introduction
00:23:20 Start
00:40:30 First Performance
00:40:56 Break
01:04:44 Second Performance
01:24:45 Crowd Shots
01:27:45 Credits
```
- `output`: Output video file to be created with embedded chapters

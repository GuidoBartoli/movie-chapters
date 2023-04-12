import argparse as ap
import os
import re
import subprocess as sp
import sys

if __name__ == "__main__":
    parser = ap.ArgumentParser("Read chapters from file and embed them into MPEG video.")
    parser.add_argument("input", help="input video")
    parser.add_argument("chapters", help="chapter data")
    parser.add_argument("output", help="output video")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit("# Input video not found!")
    print(f"> Input video: \"{os.path.basename(args.input)}\"")
    print("- Extracting original metadata...")
    data_file = "metadata.txt"
    if os.path.exists(data_file):
        os.remove(data_file)
    if sp.call(f'ffmpeg -i "{args.input}" -f ffmetadata {data_file} > /dev/null 2>&1', shell=True) != 0:
        sys.exit("# FFMPEG not installed!")
    if not os.path.exists(data_file):
        sys.exit("# Unable to extract metadata!")

    if not os.path.exists(args.chapters):
        sys.exit("# Chapter file not found!")
    chapters = []
    regex = re.compile(r"^(\d{2}):(\d{2}):(\d{2})\s+(.+)$")
    with open(args.chapters, "r") as file:
        for line in file:
            match = regex.match(line)
            if match is not None:
                h, m, s = (int(match.group(i)) for i in range(1, 4))
                if m > 59 or s > 59:
                    continue
                title = match.group(4)
                minutes = m + (h * 60)
                seconds = s + (minutes * 60)
                timestamp = seconds * 1000
                chapters += [{"title": title, "start": timestamp}]
    if not chapters:
        sys.exit("# No chapters found!")
    print(f"- {len(chapters)} chapters found in \"{os.path.basename(args.chapters)}\":")
    for i, c in enumerate(chapters):
        print(f"  [{i+1:0>2}] {c['title']} [start:{c['start']}]")

    print("- Computing chapter timestamps...")
    text = ""
    for i in range(len(chapters)):
        if i < len(chapters) - 1:
            end = chapters[i + 1]["start"] - 1
        else:
            duration = float(
                os.popen(
                    f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{args.input}"'
                ).read()[:-1]
            )
            end = int(duration * 1000)
        text += f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={chapters[i]['start']}\nEND={end}\ntitle={chapters[i]['title']}\n"
    with open(data_file, "a") as file:
        file.write(text)

    print("- Writing updated metadata...")
    if os.path.exists(args.output):
        os.remove(args.output)
    if (
        sp.call(
            f'ffmpeg -i "{args.input}" -i {data_file} -map_metadata 1 -codec copy "{args.output}" > /dev/null 2>&1',
            shell=True,
        )
        != 0
    ):
        sys.exit("# Unable to update metadata!")
    os.remove(data_file)
    print(f"> Output video: \"{os.path.basename(args.output)}\"")

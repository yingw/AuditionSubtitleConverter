"""
srt 字幕文件转成 Audition marker 的 csv 格式，另一个网上的版本 https://github.com/Terisback/subkers 有点bug
"""

import pysrt
import csv
from datetime import datetime
from pysrt.srttime import SubRipTime
from pysrt.srtitem import SubRipItem
import os
import sys
import argparse

def check_file_exists(targetfile):
    """检查文件是否存在，并询问是否覆盖"""
    if os.path.exists(targetfile):
        print(f"File '{targetfile}' exists.")
        if input("Overwrite? (y/n): ").lower() != "y":
            print("Operation canceled.")
            sys.exit(1)


def convert_srt_to_marker(filename):
    """将SRT字幕文件转换为Audition marker的CSV格式"""
    if not filename.lower().endswith(".srt"):
        print("Error: Only support *.srt file. Please choose another file.")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    try:
        subs = pysrt.open(filename)
    except pysrt.Error.InvalidSubtitleError as e:
        print(f"Error: Invalid subtitle file '{filename}': {e}")
        sys.exit(1)

    targetfile = os.path.splitext(filename)[0] + ".csv"
    check_file_exists(targetfile)

    field_names = ["Name", "Start", "Duration", "Time Format", "Type", "Description"]

    with open(targetfile, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(field_names)
        writer.writerow([])
        for s in subs:
            if isinstance(s, SubRipItem):
                print(s)
                name = s.text.replace("\n", " ")
                duration = subtime_to_string(s.end - s.start)
                start_time = subtime_to_string(s.start)
                writer.writerow([name, start_time, duration, "decimal", "Cue", ""])
    print("Coversion completed.")


def subtime_to_string(subtime: SubRipTime):
    """将SubRipTime对象转换为时间字符串"""
    try:
        time_obj = datetime.strptime(str(subtime), "%H:%M:%S,%f")
    except ValueError as e:
        print(f"Error: Unable to parse time string '{subtime}': {e}")
        return ""
    hours = time_obj.hour
    minutes = time_obj.minute
    seconds = time_obj.second
    milliseconds = time_obj.microsecond // 1000
    return (
        f"{minutes}:{seconds}.{milliseconds}"
        if hours == 0
        else f"{hours}:{minutes}:{seconds}.{milliseconds}"
    )

def main():
    parser = argparse.ArgumentParser(description=f"Convert SRT subtitle file to Adobe Audition marker CSV file.")
    parser.add_argument("filename", nargs="?", help="Input SRT subtitle file")
    args = parser.parse_args()

    if not args.filename:
        parser.print_help(sys.stderr)
        sys.exit(1)
    convert_srt_to_marker(args.filename)

if __name__ == "__main__":
    main()
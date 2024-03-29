# Audition Subtitle Converter

This Python script converts SRT subtitle files to Adobe Audition marker CSV files. The original version found on [GitHub](https://github.com/Terisback/subkers) had some bugs, so this script aims to provide a more reliable solution.

Audition markers file is a csv which looks like:

```txt
Name	Start	Duration	Time Format	Type	Description

Some Text	2:1.540	0:6.110	decimal	Cue	
Some Text2	2:7.690	0:4.340	decimal	Cue	
```

The values in the 'Start' and 'Duration' fields, '2:1.540' and '0:6.110' respectively, are not in standard format as expected (in SRT format: '00:02:01,540' --> '00:02:07,650'). This discrepancy needs to be addressed.

Another online version <https://github.com/Terisback/subkers>

## Requirements

- Python 3.x
- pysrt library

You can install the required library using pip:

```bash
pip install pysrt
```

## Usage

Run the script with the following command:

```py
python srt_to_marker.py <filename.srt>
```

Replace `<filename>` with the path to your SRT subtitle file.

TODO:
[ ] Convert csv to srt reversed.

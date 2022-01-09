import sys
import re

pattern = re.compile("([0-9]+):([0-9]+):([0-9]+),([0-9]+) --> ([0-9]+):([0-9]+):([0-9]+),([0-9]+)")


def parse_time(h_str, min_str, s_str, ms_str):
    return int(h_str) * 60 * 60 + int(min_str) * 60 + int(s_str) + int(ms_str) / 1000


def write_time(time) -> str:
    h = int(time // (60 * 60))
    time -= h * 60 * 60
    min = int(time // 60)
    time -= min * 60
    s = int(time)
    time -= s
    ms = int(1000 * time)
    return f"{h:02}:{min:02}:{s:02},{ms:03}"


if __name__ == '__main__':
    USAGE = """Offset the times and change playback rate in .srt subtitles files. The converted file is saved
        as <original-filename-without-extension>-NEW.srt.

        Usage: python subtitles.py <filename.srt> <offset_in_seconds> <old_fps> <new_fps>
        Example: python subtitles.py path/to/subtitles.srt 0 25 24
        """

    try:
        in_filename = sys.argv[1]
        offset = int(sys.argv[2])
        fps_multiplier = int(sys.argv[4]) / int(sys.argv[3])  # new / old fps
    except Exception as e:
        print(USAGE, file=sys.stderr)
        exit(1)

    out_filename = in_filename[:-4] + "-NEW.srt"
    with open(in_filename, 'r') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        line = line.strip()
        match = pattern.match(line)
        if match is None:
            new_lines.append(line + "\n")
        else:
            groups = match.groups()
            start_time = parse_time(groups[0], groups[1], groups[2], groups[3])
            stop_time = parse_time(groups[4], groups[5], groups[6], groups[7])

            start_time *= fps_multiplier
            start_time += offset
            stop_time *= fps_multiplier
            stop_time += offset

            new_lines.append(f"{write_time(start_time)} --> {write_time(stop_time)}\n")

    with open(out_filename, 'w') as f:
        f.writelines(new_lines)
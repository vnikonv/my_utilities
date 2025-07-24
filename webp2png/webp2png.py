#! python
"""
# This is a utility for ffmpeg to convert all .webp files in a specified directory
# (and optionally its subdirectories) to .png format. No paralelization is used.
"""

import subprocess
from pathlib import Path
import argparse

def webp2png(in_folder: str, out_folder: str, pattern: str) -> None:
    in_path = Path(in_folder)
    out_path = Path(out_folder)
    webp_files = list(in_path.glob(pattern))
    num_files = len(webp_files)
    count = 0

    if webp_files:
        out_path.mkdir(parents=True, exist_ok=False)
        for webp_f in webp_files:
            png_f = out_path / (webp_f.stem + '.png')
            subprocess.run(f'cwebp -mt -q 100 -lossless -quiet "{webp_f}" -o "{png_f}"', shell=True, check=True)
            count += 1
            print(f'Converted {count}/{num_files} files.')
        print('Conversion complete.')
    else:
        print('No .webp files found.')

def main():
    parser = argparse.ArgumentParser(description="Convert all webp files from in_folder to png and store in out_folder.")
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory where webp files are.'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Search webp files in subdirectories'
    )
    parser.add_argument(
        '--output', '-o',
        dest='out_folder',
        nargs='?',
        default='./output',
        help='Directory to where png files are saved.'
    )

    args = parser.parse_args()
    in_folder = Path(args.directory).resolve()
    out_folder = Path(args.out_folder).resolve()
    pattern = '**/*.webp' if args.recursive else '*.webp'
    webp2png(in_folder, out_folder, pattern)

if __name__ == '__main__':
    main()

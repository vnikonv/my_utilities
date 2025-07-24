#! python
"""
# This is a utility for ffmpeg to convert all .jpeg/.jpg files in a specified directory
# (and optionally its subdirectories) to .png format. It supports multithreading and
# can delete original jpeg/jpg files after conversion.
"""

import time
import sys
import subprocess
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_image(jpeg_f: Path, png_f: Path, yes: str) -> tuple[Path, bool]:
    try:
        subprocess.run(
            f'ffmpeg {yes} -hide_banner -loglevel panic -i "{jpeg_f}" "{png_f}"',
            shell=True,
            check=True
        )
        return jpeg_f, True
    except subprocess.CalledProcessError:
        return jpeg_f, False

def jpeg2png(in_folder: str, out_folder: str, recursive: bool, leave: bool, delete: bool, yes: str, workers: int) -> None:
    in_path = Path(in_folder)
    out_path = Path(out_folder)
    pattern = ['**/*.jpg','**/*.jpeg'] if recursive else ['*.jpg','*.jpeg']
    jpeg_files = list(in_path.glob(pattern[0])) + list(in_path.glob(pattern[1]))
    num_files = len(jpeg_files)

    if not jpeg_files:
        print('No .jpeg/.jpg files found.')
        return

    if not out_path.exists():
        out_path.mkdir(parents=True, exist_ok=False)

    print(f'Found {num_files} image(s). Starting conversion...')

    success_count = 0
    fail_count = 0
    futures = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for jpeg_f in jpeg_files:
            save_path = jpeg_f.parent if leave else out_path
            png_f = save_path / (jpeg_f.stem + '.png')
            futures.append(executor.submit(convert_image, jpeg_f, png_f, yes))

        count = 0
        for future in as_completed(futures):
            jpeg_f, success = future.result()
            count += 1
            status = 'Y' if success else 'N'
            print(f'[{status}] Converted {count}/{num_files}: {jpeg_f.name}')
            if success:
                success_count += 1
            else:
                fail_count += 1

    print(f'Conversion complete: {success_count} successful, {fail_count} failed.')

    if delete:
        for jpeg_f in jpeg_files:
            try:
                jpeg_f.unlink()
            except Exception as e:
                print(f'Failed to delete {jpeg_f}: {e}')
        print('Deleted all jpeg/jpg files.')
    else:
        print('Original files kept.')

def main():
    parser = argparse.ArgumentParser(description="Convert all jpeg/jpg files from in_folder to png and store in out_folder.")
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory where jpeg/jpg files are.'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Search jpeg/jpg files in subdirectories.'
    )
    parser.add_argument(
        '--leave', '-l',
        action='store_true',
        help='png files will be saved to the directories where jpg files are stored.'
    )
    parser.add_argument(
        '--output', '-o',
        default='.',
        help='Directory to where png files are saved.'
    )
    parser.add_argument(
        '--deljpg', '-d',
        action='store_true',
        help='Delete jpeg/jpg files after conversion.'
    )
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Answer yes to all.'
    )
    parser.add_argument(
        '--workers', '-w',
        action='store',
        default=1,
        help='Multithreading. Set the number of threads.'
    )
    
    args = parser.parse_args()
    in_folder = Path(args.directory).resolve()
    out_folder = Path(args.output).resolve()
    recursive = args.recursive
    leave = args.leave
    delete = True if args.deljpg else False
    yes = '-y' if args.yes else ''
    workers = int(args.workers)
    jpeg2png(in_folder, out_folder, recursive, leave, delete, yes, workers)

try:
    if __name__ == '__main__':
        start_time = time.time()
        main()
        end_time = time.time()
        elapsed = end_time - start_time
        print(f'Total execution time: {elapsed:.2f} seconds.')
except KeyboardInterrupt:
    print('\nInterrupted by user.')
finally:
    sys.exit(0)

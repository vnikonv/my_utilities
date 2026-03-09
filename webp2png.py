#! python

import time
import sys
import subprocess
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_image(webp_f: Path, png_f: Path, yes: str) -> tuple[Path, bool]:
    try:
        subprocess.run(
            f'ffmpeg {yes} -hide_banner -loglevel panic -i "{webp_f}" "{png_f}"',
            shell=True,
            check=True
        )
        return webp_f, True
    except subprocess.CalledProcessError:
        return webp_f, False

def webp2png(in_folder: str, out_folder: str, recursive: bool, leave: bool, delete: bool, yes: str, workers: int) -> None:
    in_path = Path(in_folder)
    out_path = Path(out_folder)
    pattern = ['**/*.webp'] if recursive else ['*.webp']
    webp_files = list(in_path.glob(pattern[0])) + list(in_path.glob(pattern[1]))
    num_files = len(webp_files)

    if not webp_files:
        print('No .webp files found.')
        return

    if not out_path.exists():
        out_path.mkdir(parents=True, exist_ok=False)

    print(f'Found {num_files} image(s). Starting conversion...')

    success_count = 0
    fail_count = 0
    futures = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for webp_f in webp_files:
            save_path = webp_f.parent if leave else out_path
            png_f = save_path / (webp_f.stem + '.png')
            futures.append(executor.submit(convert_image, webp_f, png_f, yes))

        count = 0
        for future in as_completed(futures):
            webp_f, success = future.result()
            count += 1
            status = 'Y' if success else 'N'
            print(f'[{status}] Converted {count}/{num_files}: {webp_f.name}')
            if success:
                success_count += 1
            else:
                fail_count += 1

    print(f'Conversion complete: {success_count} successful, {fail_count} failed.')

    if delete:
        for webp_f in webp_files:
            try:
                webp_f.unlink()
            except Exception as e:
                print(f'Failed to delete {webp_f}: {e}')
        print('Deleted all webp files.')
    else:
        print('Original files kept.')

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
        help='Search webp files in subdirectories.'
    )
    parser.add_argument(
        '--leave', '-l',
        action='store_true',
        help='png files will be saved to the directories where webp files are stored.'
    )
    parser.add_argument(
        '--output', '-o',
        default='.',
        help='Directory to where png files are saved.'
    )
    parser.add_argument(
        '--deljpg', '-d',
        action='store_true',
        help='Delete webp files after conversion. DO NOT USE IF ffmpeg is NOT INSTALLED'
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
    webp2png(in_folder, out_folder, recursive, leave, delete, yes, workers)

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

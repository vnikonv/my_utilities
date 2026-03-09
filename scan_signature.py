#! python
"""
# This script scans for .bin files in a specified directory (and optionally its subdirectories)
# and checks their signatures to identify the type of media file they may represent.
# It uses common media file signatures to determine the type.
"""

import argparse
from pathlib import Path

# Common media file signatures
SIGNATURES = {
    b"\x00\x00\x00\x20ftyp": "MP4",
    b"\x1A\x45\xDF\xA3": "MKV/WebM",
    b"RIFF": "AVI/WAV",
    b"OggS": "OGG",
    b"ID3": "MP3",
    b"\xFF\xFB": "MP3 (MPEG-1 Layer 3)",
    b"\x00\x00\x01\xBA": "MPEG-PS",
    b"\x00\x00\x01\xB3": "MPEG-1 Video"
}


def check_signature(filepath):
    with open(filepath, "rb") as f:
        header = f.read(16)
        for sig, name in SIGNATURES.items():
            if header.startswith(sig):
                return name
    return None


# Scan all .bin files in current directory
def main():
    parser = argparse.ArgumentParser(description="Check .bin files signature.")
    parser.add_argument(
        'directory',
        nargs='?', # Either takes 1 argument or 0. If 0, takes the default value
        default='.',
        help='Directory to search in (default: current directory)'
        )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true', # This argument will be of type boolean
        help='Search subdirectories recursively'
    )
    
    args = parser.parse_args()
    dir_path = Path(args.directory).resolve() # Sets the directory path from parser
    
    pattern = '**/*.bin' if args.recursive else '*.bin'
    bin_files = list(dir_path.glob(pattern))

    if not bin_files:
        print("No .bin files found")
        return
    else:
        for filepath in bin_files:
            kind = check_signature(filepath)
            if kind:
                print(f"{filepath}: Possible {kind} file")
            else:
                print(f"{filepath}: Unknown format")


if __name__ == '__main__':
    main()

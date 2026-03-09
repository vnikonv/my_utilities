import argparse
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import EasyMP3
import sys

def main():
    parser = argparse.ArgumentParser(description="Edit MP3 metadata and cover image.")
    parser.add_argument('--file', '-f', required=True, help='Path to the MP3 file.')
    parser.add_argument('--title', help='New title.')
    parser.add_argument('--artist', help='New artist.')
    parser.add_argument('--album', help='New album.')
    parser.add_argument('--cover', help='Path to new cover image (JPEG).')

    args = parser.parse_args()

    try:
        audio = EasyMP3(args.file)
    except Exception as e:
        print(f"Failed to load MP3 file: {e}")
        sys.exit(1)

    # Edit metadata if provided
    if args.title:
        audio["title"] = args.title
    if args.artist:
        audio["artist"] = args.artist
    if args.album:
        audio["album"] = args.album

    audio.save()

    # Add cover image if provided
    if args.cover:
        try:
            with open(args.cover, "rb") as img:
                id3 = ID3(args.file)
                id3.add(APIC(
                    encoding=3,          # UTF-8
                    mime="image/jpeg",   # Image type
                    type=3,              # Front cover
                    desc="Cover",
                    data=img.read()
                ))
                id3.save()
        except Exception as e:
            print(f"Failed to add cover image: {e}")
            sys.exit(1)

    print("Metadata updated successfully.")

if __name__ == "__main__":
    main()

import sys
import argparse
from pathlib import Path
from typing import List
from . import MuseScore, FileType, __version__
from .exceptions import LibreScoreException

def main():
    parser = argparse.ArgumentParser(
        prog='py-librescore',
        description='Download sheet music from MuseScore',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('url', help='MuseScore URL')
    parser.add_argument('formats', nargs='*', 
                        choices=['pdf', 'midi', 'mp3'],
                        default=['pdf'],
                        help='File formats to download')
    parser.add_argument('-o', '--output', default='.',
                        help='Output directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('-w', '--workers', type=int, default=5,
                        help='Number of parallel workers for PDF generation')
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    try:
        ms = MuseScore(max_workers=args.workers)
        
        if args.verbose:
            print(f"Fetching score from: {args.url}")
        
        score = ms.get_score(args.url)
        
        print(f"ID: {score.id}")
        print(f"Title: {score.title}")
        print(f"Pages: {score.page_count}")
        
        if score.is_official:
            print("Warning: Official score - may require subscription")
        
        output_dir = Path(args.output)
        
        file_type_map = {
            'pdf': FileType.PDF,
            'midi': FileType.MIDI,
            'mp3': FileType.MP3
        }
        
        for fmt in args.formats:
            file_type = file_type_map[fmt]
            
            if args.verbose:
                print(f"\nDownloading {fmt.upper()}...")
            
            def progress(current, total):
                if args.verbose:
                    percent = int((current / total) * 100)
                    print(f"Progress: {percent}% ({current}/{total})", end='\r')
            
            score_file = score.download(file_type, progress_callback=progress if args.verbose else None)
            
            filepath = score.save(file_type, output_dir)
            
            if args.verbose:
                print(f"\nSaved: {filepath}")
                print(f"Size: {score_file.size} bytes")
                print(f"SHA256: {score_file.sha256}")
            else:
                print(f"Saved: {filepath}")
        
        print("\nDone!")
        return 0
        
    except LibreScoreException as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
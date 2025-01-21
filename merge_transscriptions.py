import os
import re
from datetime import datetime, timedelta

def time_to_seconds(time_str):
    """Convert timestamp like '00:00:00' to seconds"""
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def seconds_to_time(seconds):
    """Convert seconds to timestamp format '00:00:00'"""
    return str(timedelta(seconds=seconds)).zfill(8)

def adjust_timestamps(content, base_seconds):
    """Adjust timestamps in content by adding base_seconds"""
    # Pattern to match timestamp format [HH:MM:SS-HH:MM:SS]
    pattern = r'\[(\d{2}:\d{2}:\d{2})-(\d{2}:\d{2}:\d{2})\]'
    
    def replace_timestamp(match):
        start_time = time_to_seconds(match.group(1))
        end_time = time_to_seconds(match.group(2))
        
        # Add base_seconds to both timestamps
        new_start = seconds_to_time(start_time + base_seconds)
        new_end = seconds_to_time(end_time + base_seconds)
        
        return f'[{new_start}-{new_end}]'
    
    return re.sub(pattern, replace_timestamp, content)

def combine_diarization_outputs():
    current_dir = os.path.dirname(os.path.abspath(__file__)) or '.'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(current_dir, f"merged_transcription_{timestamp}.md")
    segment_pattern = r"segment_(\d{3})_transcription\.txt$"
    
    try:
        transcription_files = []
        for file in os.listdir(current_dir):
            if match := re.match(segment_pattern, file):
                segment_num = int(match.group(1))
                transcription_files.append((segment_num, file))
        
        if not transcription_files:
            print("No transcription files found in current directory")
            print("Looking for files matching pattern: segment_XXX_transcription.txt")
            return
            
        transcription_files.sort()
        print(f"Found {len(transcription_files)} transcription files to process")
        
    except Exception as e:
        print(f"Error scanning directory: {e}")
        return
    
    try:
        with open(output_file, "w", encoding="utf-8") as outfile:
            base_seconds = 0
            for segment_num, file in transcription_files:
                print(f"Processing segment {segment_num}: {file}")
                
                try:
                    with open(os.path.join(current_dir, file), "r", encoding="utf-8") as infile:
                        content = infile.read().strip()
                        
                        # Adjust timestamps if not the first segment
                        if segment_num > 0:
                            content = adjust_timestamps(content, base_seconds)
                        
                        outfile.write(content)
                        outfile.write("\n\n")  # Add spacing between segments
                        
                        # Find the last timestamp to set base for next segment
                        last_timestamp = re.findall(r'\[\d{2}:\d{2}:\d{2}-(\d{2}:\d{2}:\d{2})\]', content)
                        if last_timestamp:
                            base_seconds = time_to_seconds(last_timestamp[-1])
                        
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    continue
        
        print(f"\nSuccessfully created merged transcription: {os.path.basename(output_file)}")
        
    except Exception as e:
        print(f"Error writing output file: {e}")
        return

if __name__ == "__main__":
    print("Starting transcription merger...")
    combine_diarization_outputs()
    print("Process completed.")
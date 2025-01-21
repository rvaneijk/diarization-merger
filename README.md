# Audio Transcription Merger

Merges multiple Google AI Studio diarization transcripts into a single file with continuous timestamps.

## Prerequisites

- Python 3.x
- ffmpeg
- Google AI Studio access

## Usage

1. Split your audio into 20-minute segments:
```bash
ffmpeg -i "your_audio.mp3" -f segment -segment_time 1200 -c copy "segment_%03d.mp3"
```

2. For each segment:
   - Upload to Google AI Studio
   - Use prompt: "Generate audio diarization, including transcriptions and speaker information for each transcription, for this interview. Organize the transcription by the time they happened."
   - Save output as `segment_XXX_transcription.txt`

3. Place `merge_transscriptions.py` in same directory as transcription files

4. Run:
```bash
python3 merge_transscriptions.py
```

The script will create `merged_transcription_YYYYMMDD_HHMMSS.md` with continuous timestamps.

## Next Steps

Feed the merged file to Gemini 1.5 Pro with:
```
Summarize the following discussion, providing a detailed summary of each speaker's individual arguments. Organize the summary by sections, mirroring the structure of the original discussion. Within each section, summarize each speaker's contribution using the following format: "[Speaker Name]: [comprehensive summary of their main arguments, focusing on their core positions and the reasoning behind them]. [Supporting details, including specific examples, analogies, or data they used]. [Note any counterarguments or caveats they mentioned]."
```
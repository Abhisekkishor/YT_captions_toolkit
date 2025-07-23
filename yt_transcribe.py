from youtube_transcript_api import YouTubeTranscriptApi
import sys
import os

vid = sys.argv[1]

try:
    parts = YouTubeTranscriptApi.get_transcript(vid)
    full_text = " ".join([p['text'] for p in parts])
    print("Transcript from API:")
    print(full_text)

except Exception as e:
    print(f"\nTranscript from API not available. Reason: {str(e)}\n")

    import yt_dlp
    import whisper

    def download_audio(video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{video_id}.mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as download_err:
            print(f"❌ Failed to download audio. Reason: {download_err}")
            sys.exit(1)

    def transcribe_with_whisper(video_id):
        audio_file = f"{video_id}.mp3"
        if not os.path.exists(audio_file):
            print(f"❌ Audio file '{audio_file}' not found.")
            sys.exit(1)

        try:
            model = whisper.load_model("base")
            result = model.transcribe(audio_file)
            print("Transcript from Whisper:")
            print(result['text'])
        except Exception as whisper_err:
            print(f"❌ Whisper transcription failed. Reason: {whisper_err}")
            sys.exit(1)

    # Start backup transcription path
    download_audio(vid)
    transcribe_with_whisper(vid)

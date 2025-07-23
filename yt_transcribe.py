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

    import whisper
    import yt_dlp

    def download_audio(video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        filename = f"{video_id}.m4a"
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': filename,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }

        print("📥 Downloading audio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if not os.path.exists(filename):
            raise FileNotFoundError(f"❌ Audio file '{filename}' not found.")
        return filename

    def transcribe_with_whisper(audio_file):
        print("🧠 Transcribing with Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        print("Transcript from Whisper:")
        print(result['text'])

    audio_path = download_audio(vid)
    transcribe_with_whisper(audio_path)

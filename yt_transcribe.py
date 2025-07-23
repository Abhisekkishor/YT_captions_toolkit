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

    def transcribe_with_whisper(audio_path, video_id):
        print("🧠 Transcribing with Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcript_text = result['text']
        
        # Print in console
        print("Transcript from Whisper:")
        print(transcript_text)

        # Save to file
        txt_filename = f"{video_id}_transcript.txt"
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        
        print(f"\n✅ Transcript saved to: {txt_filename}")

    audio_file = download_audio(vid)
    transcribe_with_whisper(audio_file, vid)

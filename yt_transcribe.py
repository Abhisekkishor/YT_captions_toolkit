from youtube_transcript_api import YouTubeTranscriptApi
import sys

vid = sys.argv[1]

try:
    parts = YouTubeTranscriptApi.get_transcript(vid)
    full_text = " ".join([p['text'] for p in parts])
    print("Transcript from API:")
    print(full_text)

except Exception as e:
    print(f"Transcript from API not available. Reason: {str(e)}")

    import whisper
    import yt_dlp

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

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def transcribe_with_whisper(video_id):
        model = whisper.load_model("base")
        result = model.transcribe(f"{video_id}.mp3")
        print("Transcript from Whisper:")
        print(result['text'])

    download_audio(vid)
    transcribe_with_whisper(vid)

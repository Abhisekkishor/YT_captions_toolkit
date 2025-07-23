from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import sys, json
vid = sys.argv[1] if len(sys.argv) > 1 else "b_MGyd8TKdQ"
try:
    parts = YouTubeTranscriptApi.get_transcript(vid)
    full_text = " ".join(p['text'] for p in parts)
except NoTranscriptFound:
    print("No captions – Whisper will kick in on Colab.")
    sys.exit(0)
parser = PlaintextParser.from_string(full_text, Tokenizer("english"))
summary = TextRankSummarizer()(parser.document, 5)   # 5 sentences
print(json.dumps({"video": vid, "summary": " ".join(str(s) for s in summary)}, indent=2))

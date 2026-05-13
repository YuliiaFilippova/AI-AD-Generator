import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str):
    try:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
    except:
        return None
    return None


def get_video_metadata(url: str):
    """Get title and description from YouTube"""
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title", "")
        description = info.get("description", "")

        return title, description

    except Exception as e:
        print(f"[metadata] Failed to fetch title/description: {e}")
        return "", ""


def get_transcript(video_id: str):
    """Get transcript text from YouTube"""
    if not video_id:
        return ""

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t["text"] for t in transcript])
        return text

    except Exception as e:
        print(f"[metadata] Transcript not available: {e}")
        return ""


def clean_text(text: str):
    return text.replace("\n", " ").strip()


def get_youtube_data(url: str):
    """Main function to extract all metadata safely"""

    try:
        title, description = get_video_metadata(url)
        video_id = extract_video_id(url)
        transcript = get_transcript(video_id)

        return {
            "title": clean_text(title),
            "description": clean_text(description),
            "transcript": clean_text(transcript)
        }

    except Exception as e:
        print(f"[metadata] Failed to extract metadata: {e}")
        return {
            "title": "",
            "description": "",
            "transcript": ""
        }


def build_semantic_context(title, description, transcript, llm_call):
    """
    Create short semantic context using LLM.
    llm_call = your ollama function
    """

    if not title and not description and not transcript:
        return ""

    text = f"""
Title: {title}

Description: {description}

Transcript:
{transcript[:3000]}
"""

    prompt = """
Summarize the key context of this video.

Focus on:
- who is involved
- important conditions (e.g. blind, injured, emotional)
- setting (e.g. circus, outdoors, indoors)
- overall situation

Rules:
- Keep it very short (2–3 sentences)
- Do NOT include dialogue
- Do NOT repeat phrases
"""

    try:
        response = llm_call(prompt)
        return response.strip()

    except Exception as e:
        print(f"[metadata] Failed to build semantic context: {e}")
        return ""
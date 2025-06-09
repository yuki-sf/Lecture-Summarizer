import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " "], chunk_size=2000, chunk_overlap=100 #Adjust chunk size for better summarization
)

video_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " "], chunk_size=1000, chunk_overlap=50 # Larger chunks for video transcripts
)


def huggingface_summarize(text: str) -> str:
    print("[HF] Summarizing chunk of text...")
    payload = {"inputs": text,
               "parameters": {
                    "min_length": 100,   # Adjust for ~200 word summaries
                    "max_length": 300,
                    "do_sample": False
                }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"[HF] Error {response.status_code}: {response.text}")
        return f"Error: Hugging Face API failed with status code {response.status_code}"
    
    summary = response.json()
    if isinstance(summary, list) and "summary_text" in summary[0]:
        return summary[0]["summary_text"]
    return "Error: Unexpected API response format."

def huggingface_video_summarize(text: str) -> str:
    print("[HF Video] Summarizing video chunk...")
    payload = {"inputs": text,
               "parameters": {
                    "min_length": 20,   # Adjust for ~100 word summaries
                    "max_length": 50,
                    "do_sample": False
                }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"[HF Video] Error {response.status_code}: {response.text}")
        return f"Error: Hugging Face API failed with status code {response.status_code}"
    
    summary = response.json()
    if isinstance(summary, list) and "summary_text" in summary[0]:
        return summary[0]["summary_text"]
    return "Error: Unexpected API response format."

def summarize_text_chunks(chunks):
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"[Summarizer] Summarizing chunk {i + 1} of {len(chunks)}...")
        summary = huggingface_summarize(chunk.page_content)
        summaries.append(summary)
    return "\n\n".join(summaries)

def summarize_video_chunks(chunks):
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"[Video Summarizer] Summarizing video chunk {i + 1} of {len(chunks)}...")
        summary = huggingface_video_summarize(chunk.page_content)
        summaries.append(summary)
    return "\n\n".join(summaries)

def summarize_article(url: str) -> str:
    print(f"[Article] Fetching article from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching article: {str(e)}"
    
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = soup.find_all('p')
    text = "\n".join(p.get_text() for p in paragraphs if p.get_text().strip())
    
    if not text or len(text) < 100:
        return "Could not extract enough content to summarize."

    print("[Article] Splitting article into chunks...")
    docs = text_splitter.create_documents([text])
    return summarize_text_chunks(docs)

def summarize_youtube_video(url: str) -> str:
    print(f"[YouTube] Loading YouTube video transcript for {url}...")
    try:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
        documents = loader.load()
        if not documents:
            return "Failed to extract transcript for summarization."
        
        print("[YouTube] Splitting transcript into chunks...")
        docs = video_splitter.create_documents([doc.page_content for doc in documents])
    except Exception as e:
        return f"Error loading YouTube video: {str(e)}"
    
    print(f"[YouTube] Loaded and split into {len(docs)} chunk(s).")
    return summarize_video_chunks(docs)

class summary_agent():
    def summarize(self, input_text: str) -> str:
        print("[Agent] Received input to summarize.")
        if "youtube.com" in input_text or "youtu.be" in input_text:
            return summarize_youtube_video(input_text)
        elif input_text.startswith("http"):
            return summarize_article(input_text)
        else:
            print("[Agent] Treating input as raw text.")
            docs = text_splitter.create_documents([input_text])
            return summarize_text_chunks(docs)

if __name__ == "__main__":
    print("Enter a YouTube link, article URL, or raw text:")
    query = input()
    agent = summary_agent()
    print("\n[Summary Output]\n")
    print(agent.summarize(query))

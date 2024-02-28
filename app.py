import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a youtube video summarizer. You will be taking the transcript text and summzarizing the entire video and providing the important things in bullet points within 250 words. Here comes the transcript text good luck:  """

def extractTranscriptionFromVideo(videoUrl: str):
    with st.spinner("Fetching transcript...."):
        try:
        
            videoId=videoUrl.split("=")[1]
            transcriptText=YouTubeTranscriptApi.get_transcript(video_id=videoId)

            transcript=""
            for i in transcriptText:
                transcript += " " + i["text"]
                    
            return transcript

        except:
            st.error("Sorry for the inconvenience but transcription for this video is not available yet.")

def generateSummary(transcriptText, prompt: str):
    with st.spinner("Generating Summary...."):
        model=genai.GenerativeModel('gemini-pro')
        response=model.generate_content(prompt+transcriptText)
        return response.text

st.title("Youtube Video Summarizer By Mohammad Ali")
youtubeLink=st.text_input("Enter youtube video url: ")

if youtubeLink:
    videoId=youtubeLink.split("=")[1]
    st.image(f'http://img.youtube.com/vi/{videoId}/0.jpg', use_column_width=True)

if st.button("Summarize"):
    transcriptText=extractTranscriptionFromVideo(youtubeLink)

    if transcriptText:
        summary=generateSummary(transcriptText, prompt)
        st.markdown("## Summary: ")
        st.write(summary)
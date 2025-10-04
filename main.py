import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary 
import requests 
from dotenv import load_dotenv
import os
import pygame
import pyaudio

load_dotenv()
ai_api = os.getenv("GROQ_API_KEY")
newapi = os.getenv("NEWS_API_KEY")


r = sr.Recognizer()


def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    pygame.mixer.init()

    # Load your MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3
    pygame.mixer.music.play()

    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def ask_groq(prompt):
    """
    Ye function user ka input Groq API ko bhejta hai
    aur AI ka response return karta hai.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {ai_api}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        print("Error:", response.status_code, response.text)
        return "Sorry, I couldn't connect to the AI service."
    
def processComand(c):
    if "open google" in c.lower() :
        webbrowser.open("http://google.com")
    elif "open facebook" in c.lower() :
        webbrowser.open("http://facebook.com")
    elif "open youtube" in c.lower() :
        webbrowser.open("http://youtube.com")
    elif c.lower().startswith("play"):
        parts = c.lower().split(" ")
        if len(parts) > 1 :
            song = parts[1]
            if song in musicLibrary.music:
                link = musicLibrary.music[song]
                webbrowser.open(link)
        else :
            speak("sorry music not avalible in music library")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newapi}")
        if r.status_code == 200 :
            data = r.json()
            articles = data.get("articles", [])

            for article in articles :
                speak(article["title"])
        else :
            speak("sorry i could not fetch the news")
    else :
        output = ask_groq(c)
        speak(output)
       

    

if __name__ == "__main__":
    speak("Installizing Jarvis..")


    
    # Obtain audio from microphone
    while True:
        print("Recognizing..")
       
        try:
            with sr.Microphone() as source:
                print("Listening..")
            # Adjust for ambient noise for better accuracy
                r.adjust_for_ambient_noise(source)
            # Listen for audio input
                audio = r.listen(source, timeout= 4, phrase_time_limit= 5 )
            # Use Google Web Speech API to recognize the speech
            word = r.recognize_google(audio)
            # Listen for the wake word Jarvis
            if ("jarvis" in word.lower()):
                speak("How can I help you sir!")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis activated...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processComand(command)

        except Exception as e:
            print(f"Error! {e}")


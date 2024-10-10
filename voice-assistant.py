import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyjokes
import random
import requests

# Initialize the voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Setting female voice

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    greetings = ["Good Morning!", "Good Afternoon!", "Good Evening!"]
    if 0 <= hour < 12:
        speak(greetings[0])
    elif 12 <= hour < 18:
        speak(greetings[1])
    else:
        speak(greetings[2])

    introductions = [
        "Hi Yadav, I am GPT5.0, your assistant. How can I assist you today?",
        "Hello Yadav! I'm GPT5.0. What would you like me to help with?",
        "Hi Yadav! GPT5.0 here. Ready to assist. How can I help?"
    ]
    speak(random.choice(introductions))
    showCommands()  # Display commands in the terminal

def showCommands():
    """List the available commands for the user."""
    commands = [
        "Open YouTube or Google.",
        "Tell you the current time.",
        "Tell a joke.",
        "open Gmail",
        "Fetch the latest news.",
        "open whatsapp ,telegram or spotify",
    ]
    print("Here are some things I can do:")
    for command in commands:
        print(f"- {command}")  # Print commands to the terminal

def takeCommand():
    """Takes microphone input from the user and returns the string output."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        speak("Say that again please...")
        return "None"
    return query

def openApplication(app_name):
    """Open specified application based on the user command."""
    # Define URLs for web-based applications
    applications = {
        "spotify": "https://open.spotify.com/",
        "whatsapp": "https://web.whatsapp.com/",
        "telegram": "https://web.telegram.org/a/",
        "file explorer": "This PC",
        "gmail": "https://mail.google.com/mail/u/0/#inbox",  # Keep email as is
    }

    app_url = applications.get(app_name.lower())
    if app_url:
        webbrowser.open(app_url)  # Open the application in a web browser
        speak(f"Opening {app_name} for you.")
    else:
        speak("Sorry, I couldn't find that application.")

def getWeather(city):
    """Fetch the weather report for the specified city."""
    api_key = "your_openweather_api_key"  # Replace with your OpenWeatherMap API Key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        main = weather_data['main']
        temperature = main['temp']
        weather_desc = weather_data['weather'][0]['description']
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}.")
    else:
        speak("I couldn't find the weather for that city. Please check the city name and try again.")

def getCity():
    """Ensure the assistant captures the city name."""
    while True:
        speak("Could you please tell me the city name for the weather?")
        city = takeCommand().lower()

        if city != "none" and city != "":
            return city
        else:
            speak("I didn't catch that. Could you please repeat the city name?")

def getNews():
    """Fetch the top news headlines."""
    api_key = 'your_newsapi_key'  # Replace with your NewsAPI Key
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()

    if news_data["status"] == "ok":
        speak("Here are the top news headlines.")
        for i, article in enumerate(news_data['articles'][:5]):
            speak(f"Headline {i + 1}: {article['title']}")
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")

if __name__ == '__main__':
    wishMe()

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            speak("Opening YouTube now.")

        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("Opening Google for you.")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\YourUsername\\Music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            speak("Playing your music now.")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}. Would you like to know anything else?")

        elif 'open email' in query:
            openApplication("email")  # Open the email application

        elif 'joke' in query:
            speak(pyjokes.get_joke())
            speak("Hope that made you smile! Want to hear another one?")

        elif 'news' in query:
            getNews()

        elif 'open whatsapp' in query:
            app_names = ['whatsapp']  # Add more application names here
            for app in app_names:
                if app in query:
                    openApplication(app)
                    break

        elif 'open telegram' in query:
            app_names = ['telegram']  # Add more application names here
            for app in app_names:
                if app in query:
                    openApplication(app)
                    break

        elif 'open spotify' in query:
            app_names = ['spotify']  # Add more application names here
            for app in app_names:
                if app in query:
                    openApplication(app)
                    break

        elif 'open gmail' in query:
            app_names = ['gmail']  # Add more application names here
            for app in app_names:
                if app in query:
                    openApplication(app)
                    break

        elif 'then' in query:
            speak("Thank you for your time.")
            break

        else:
            speak("Sorry, I can't assist with that. Would you like to try asking something else?")

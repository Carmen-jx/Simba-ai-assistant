from _datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# speech engine initialization

engine = pyttsx3.init()
voices = engine.getProperty('voices')
i = 0
# for v in voices:
#    i +=1
#    print(v, i)
engine.setProperty('voice', voices[90].id)
activateWord = 'simba'

#configure wolfram alpha
app_id = 'UXRVW7-R3P3A66PV7'

def speak(text, rate=180):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()



def parse_command():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        listener.energy_threshold = 300
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_GB')
        print('The input speech was: {query')
    except Exception as exception:
        print('I did not catch that')
        speak('I did not catch that')

        print(exception)
        return 'None'

    return query

def search_wiki(query= ' '):
    results= wikipedia.search(query)
    if not results:
        print('no wikipedia results')
        return'No results'
    try:
        wikiPage = wikipedia.page(results[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

if __name__ == '__main__':
    speak('hi what can I help you with')

    while True:
        # Parse
        query = parse_command().lower().split()

        if query[0] == activateWord:
            query.pop(0)

            if query[0] == 'say':
                if 'hello' in query:
                    speak('wazzup')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                print(query)
                try:
                    url= 'http://' +query
                    webbrowser.get('chrome').open_new(url)
                    print("Browser opened successfully.")  # Debugging
                except Exception as e:
                    print("Error opening browser:", e)  # Debugging

            if query[0] == 'wiki':
                query = ' '.join((query[1:]))
                speak('searching for ' + query + 'from wikipedia database')

                try:
                    speak(search_wiki(query))
                except Exception as e:
                    speak(query + 'cannot be found, try again')




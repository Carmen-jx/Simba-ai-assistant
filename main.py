from _datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import requests
import random

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
wolf_client = wolframalpha.Client('UXRVW7-R3P3A66PV7')


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
        print('The input speech was:', query)
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

def wolf_type(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframalpa(query = ' '):
    response = wolf_client.query(query)

    if response['@success'] == 'false':
        return 'Could not compute'
    else:
        result = ''
        #question
        pod0 = response['pod'][0]

        pod1 = response['pod'][1]

        if ('result' in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            result = wolf_type(pod1['subpod'])

            return result.split('(')[0]
        else:
            question = wolf_type(pod0['subpod'])

            return result.split('(')[0]
            speak('computation failed. searching wikipedia database')
            return search_wiki(question)



def fetch_poem():
    # configure poem API request
    response = requests.get("https://www.beanpoems.com/api/poems")
    print(response.json())

    if response.status_code == 200:
        return response.json()
    else:
        print("failed to fetch poem:", response.status_code)
        return None





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
                    url = 'http://' + query
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

            if query[0] == 'compute':
                query = ' '.join((query[1:]))
                speak('computing')
                try:
                    result = search_wolframalpa(query)
                    speak(result)
                except Exception as e:
                    speak('unable to compute')
                    print(e)

            if query[0] == "poem":
                try:
                    poems_list = fetch_poem()

                    poem = poems_list[random.randint(0,5)]

                    if poem:
                        title = poem.get('title')
                        description = poem.get('description')
                        body = poem.get('body')

                        speak('Title: ' + title, 150)
                        speak(description, 150)
                        speak(body, 150)
                    else:
                        speak('Cannot find a poem')
                except Exception as e:
                    speak('unable to read a poem')
                    print(e)







import os
import random
import speech_recognition
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager  

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

# создание команд, где ключ - функция, а значение - набор вызываемых команд
commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую', 'хай'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'play_music': ['включить музыку', 'включи музыку', 'музыка'],
        'shutdown': ['включить компьютер', 'выключи компьютер'],
        'gogle_open': ['открой ссылку', 'включить гугл', 'гугл']
    }
}

# функция распознавания команд
def listen_command():
    try:
        # Вынесем распознавание команды
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        return query
    except speech_recognition.UnknownValueError:
        return 'Упс... Не понял, что ты сказал(а) :/'


def greeting():
    return 'Привет!'

# функция для записи в список дел с помощью голосовой программы
def create_task():
    print('Что добавим в список дел?')
    
    query = listen_command()

    with open('todo-list.txt', 'a', encoding="utf-8") as file:
        file.write(f'❗️ {query}\n')
        
    return f'Задача {query} добавлена в todo-list!'

# функция включения рандомной музыки  
def play_music():
    #files = os.listdir('music')
    #random_file = f'music/{random.choice(files)}'
    path = "music"
    all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]
    random_file = random.choice(all_mp3)
    os.system(f'start {random_file}')
    return f'Наслаждаемся {random_file.split("/")[-1]} 🔊🔊🔊'

# функция выключения компьютера
def shutdown():
    print('Вы хотите выключить компьютер? (да/нет)')

    query = listen_command()
    if query == 'нет':
        exit()
    else:
        os.system("shutdown /s /t 1")

# функция открытия ссылки в Google
def gogle_open():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
   "profile.default_content_setting_values.media_stream_mic": 1,
   "profile.default_content_setting_values.geolocation": 2,
   "profile.default_content_setting_values.notifications": 2
    }) 
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://www.google.com/search?q=%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8&oq=%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8&aqs=chrome..69i57j0i402l2j0i10i131i433i512l3j69i61l2.6800j1j7&sourceid=chrome&ie=UTF-8")
    time.sleep(30)
    
def main():
    query = listen_command()
    
    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())
            
if __name__ == "__main__":
    main()            

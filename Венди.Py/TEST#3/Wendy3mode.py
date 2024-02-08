#библиотеки
import speech_recognition as sr
from fuzzywuzzy import fuzz
import datetime
import time
import os
from os import system, path
import sys
from random import *
import string as st
import webbrowser
import pyautogui as pg
import pyshorteners
import datefinder
import winsound
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import configparser

#тело Венди
class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    #Настройки и словари не точечных команд
    def __init__(self):
        self.r = sr.Recognizer()
        self.text = ''

        self.cmds = {
            ('Венди привет', 'Венди ты тут', 'привет'): self.hello,
            ('Венди пока', 'Венди выключись', 'Венди закройся', 'пока', 'закройся', 'выключись'): self.enough,
            ('Венди выключи компьютер', 'Венди завершаем работу', 'Венди ширма'): self.close,
            ('Венди перезагрузка', 'Венди перезагрузи компьютер', 'Венди антракт'): self.restart_pc,
            ('Венди открой калькулятор', 'Венди калькулятор'): self.calc,
            ('Венди открой браузер', 'Венди браузер', 'Венди открой интернет', 'Венди открой интернет'): self.open_web,
            ('Венди открой YouTube', 'Венди YouTube', 'открой youtube', 'венди youtube'): self.YouTube,
            ('Венди следующее видео', 'следующее видео', 'Венди дальше', 'дальше'): self.YouTube_dop,
            ('Венди вк', 'Венди вконтакте', 'Венди vk', 'Венди открой вк', 'Венди открой вконтакте', 'Венди открой vk'): self.VK,
            ('Венди открой телеграм', 'Венди телеграм', 'Венди открой telegram', 'Венди открой telegram'): self.Teleg,
            ('Венди открой почту', 'Венди почта', 'Венди открой mail', 'Венди mail'): self.mail,
            ('Венди включи музыку', 'Венди поставь что-нибудь'): self.music,
            ('Венди укороти ссылку', 'Венди сделай ссылку короче', 'Венди короткая ссылка'): self.ShortLink,
            ('Венди создай логин и пароль', 'Венди создать логин и пароль', 'Венди придумай логин и пароль'): self.USPASS,
            ('Венди что ты можешь'): self.Power,
        }

        self.ndels = ['скажи', 'расскажи', 'покажи', 'произнеси', 'пожалуйста', 'ладно']

        self.commands = [
            'Венди привет', 'Венди ты тут', 'привет',
            'Венди пока', 'Венди выключись', 'Венди закройся', 'пока', 'закройся', 'выключись'
            'Венди выключи компьютер', 'Венди завершаем работу', 'Венди ширма',
            'Венди перезагрузка', 'Венди перезагрузи компьютер', 'Венди антракт',
            'Венди открой калькулятор', 'Венди калькулятор',
            'Венди открой браузер', 'Венди браузер', 'Венди открой интернет', 'Венди открой интернет'
            'Венди открой YouTube', 'Венди YouTube', 'открой youtube', 'венди youtube'
            'Венди следующее видео', 'следующее видео', 'Венди дальше', 'дальше'
            'Венди вк', 'Венди вконтакте', 'Венди vk', 'Венди открой вк', 'Венди открой вконтакте', 'Венди открой vk',
            'Венди открой телеграм', 'Венди телеграм', 'Венди открой telegram', 'Венди открой telegram',
            'Венди открой почту', 'Венди почта', 'Венди открой mail', 'Венди mail',
            'Венди включи музыку', 'Венди поставь что-нибудь',
            'Венди укороти ссылку', 'Венди сделай ссылку короче', 'Венди короткая ссылка',
            'Венди создай логин и пароль', 'Венди создать логин и пароль', 'Венди придумай логин и пароль',
            'Венди что ты можешь'
        ]

        self.num_task = 0
        self.j = 0
        self.ans = ''

    #чистелка слов
    def cleaner(self, text):
        self.text = text

        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

        self.ans = self.text

        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k > 90) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    #команды точечных запросов и нечеткое распознование #windy #в индии
    def recognizer(self):
        self.text = self.cleaner(self.listen())
        print(self.text)

        if self.text.startswith(('венди найди в интернете', 'венди ищи', 'венди кто такой', 'венди что такое', 'венди кто такая', 'венди когда',\
        'венди найди кто такой', 'венди найди что такое', 'венди найди кто такая', 'венди найди когда', 'венди как работает',\
        'найди в интернете', 'найди кто такой', 'найди что такое', 'найди кто такая', 'найди когда', 'найди как работает')):
            self.web_search(self.text)

        elif self.text.startswith(('венди найди на ютубе', 'венди найди на ютуби', 'венди найди на youtube', 'венди открой на youtube', 'венди открой на ютубе', 'венди открой на ютуби'\
        'найди на ютубе', 'найди на ютуби', 'найди на youtube', 'открой на youtube', 'открой на ютубе', 'открой на ютуби', 'венди найди на ютубе кто такой')):
            self.YouTube_search(self.text)

        elif self.text.startswith(('венди переведи на английский', 'венди перевести на английский', 'венди перевести на английский', 'переведи на английский', 'перевести на английский',\
        'перевести на английский')):
            self.translateRU(self.text)

        elif self.text.startswith(('венди переведи на русский', 'венди перевести на русский', 'венди перевести на русский', 'переведи на русский', 'перевести на русский',\
        'перевести на русский')):
            self.translateEN(self.text)

        elif self.text.startswith(('венди создай папку', 'венди создать папку', 'венди создай папку с именем', 'венди создать папку с именем', 'создай папку', 'создать папку',\
        'создай папку с именем', 'создать папку с именем')):
            self.Folder(self.text)

        elif self.text.startswith(('венди поставь будильник', 'венди поставить будильник', 'венди заведи будильник', 'поставь будильник', 'поставить будильник', 'заведи будильник')):
            self.alarm_clock(self.text)

        elif self.text.startswith(('венди громкость на максимум', 'венди максимум', 'венди музыку на максимум', 'в индии громкость на максимум', 'в индии максимум',\
        'в индии музыку на максимум', 'громкость на максимум', 'максимум', 'музыку на максимум', 'венди громкость на 100', 'венди 100', 'венди музыку на 100',\
        'в индии громкость на 100', 'в индии 100', 'в индии музыку на 100', 'громкость на 100', 'музыку на 100',)):
            self.VUP(self.text)

        elif self.text.startswith(('венди громкость на середину', 'венди громкость на мидл', 'венди середина', 'венди мидл', 'венди музыку на середину', 'венди музыку на мидл',\
        'в индии громкость на середину', 'в индии громкость на мидл', 'в индии середина', 'в индии мидл', 'в индии музыку на середину', 'в индии музыку на мидл',\
        'громкость на середину', 'громкость на мидл', 'середина', 'мидл', 'музыку на середину', 'музыку на мидл', 'громкость на 50', 'венди громкость на 50',  'в индии громкость на 50')):
            self.VMIDLE(self.text)

        elif self.text.startswith(('венди громкость на минимум', 'венди минимум', 'венди музыку на минимум', 'венди минимал', 'венди музыку на минимал',\
        'в индии громкость на минимум', 'в индии минимум', 'в индии музыку на минимум', 'в индии минимал', 'в индии музыку на минимал',\
        'громкость на минимум', 'минимум', 'музыку на минимум', 'минимал', 'музыку на минимал', 'венди выключи звук', 'выключи звук', 'в индии выключи звук')):
            self.VDOWN(self.text)

        elif self.text.startswith(('венди громкость на 75', 'венди музыку на 75', 'в индии громкость на 75', 'в индии музыку на 75', 'громкость на 75', 'музыку на 75')):
            self.V75(self.text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 90:
                    self.cmds[tasks]()
                    return

    #Приветствие
    def HI(self):
        Executive_voice = randint(0, 1)
        if Executive_voice == 0:
            winsound.PlaySound('Приветначиннаюработу.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Запускаюскриптыиготоваработать.WAV', winsound.SND_LOOP)

    def Power(self):
        winsound.PlaySound('2_5237814936477909508.WAV', winsound.SND_LOOP)
        winsound.PlaySound('2_5237814936477909506.WAV', winsound.SND_LOOP)

    def USPASS(self):
        username = ''.join(choice(st.ascii_letters) for _ in range(10))
        password = ''.join(choice(st.ascii_letters + st.digits) for _ in range(12))
        Executive_voice = randint(1, 4)
        if Executive_voice == 1:
            winsound.PlaySound('генерирую.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        print("Логин:", username + '@gmail.com')
        print("Логин:", username + '@mail.ru')
        print("Пароль:", password)
        print()

    def hello(self):
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('Приветчеммогупомочь.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Ятут.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Здравствуйте.WAV', winsound.SND_LOOP)

    def enough(self):
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('Покапока.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Радабылапомочь.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Досвидания.WAV', winsound.SND_LOOP)
        system('cls')
        sys.exit(0)

    def close(self):
        Executive_voice = randint(0, 1)
        if Executive_voice == 0:
            winsound.PlaySound('Выуверены.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Выточноэтогохотите.WAV', winsound.SND_LOOP)
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'да') > 70) or (fuzz.ratio(text, "подтверждаю") > 70):
            Executive_voice = randint(1, 5)
            if Executive_voice == 1:
                winsound.PlaySound('Действиеподтверждено.WAV', winsound.SND_LOOP)
            elif Executive_voice == 2:
                winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
            elif Executive_voice == 3:
                winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
            elif Executive_voice == 4:
                winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Хорошо.WAV', winsound.SND_LOOP)
            time.sleep(1)
            Executive_voice = randint(0, 1)
            if Executive_voice == 1:
                winsound.PlaySound('Доскорыхвстреч.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Хорошовампровестивремя.WAV', winsound.SND_LOOP)
            system('shutdown /s /f /t 10')
            self.quite()
        elif (fuzz.ratio(text, 'отмена') > 70) or (fuzz.ratio(text, 'нет') > 70):
            Executive_voice = randint(0, 1)
            if Executive_voice == 0:
                winsound.PlaySound('Действиенеподтверждено.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Запросневыполнен.WAV', winsound.SND_LOOP)
        else:
            Executive_voice = randint(0, 1)
            if Executive_voice == 0:
                winsound.PlaySound('Действиенеподтверждено.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Запросневыполнен.WAV', winsound.SND_LOOP)

    def restart_pc(self):
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('Выуверены.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Выуверенычтохотитеперезагрузитькомпьютер.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Выточноэтогохотите.WAV', winsound.SND_LOOP)
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'да') > 70) or (fuzz.ratio(text, "подтверждаю") > 70):
            Executive_voice = randint(1, 6)
            if Executive_voice == 1:
                winsound.PlaySound('Действиеподтверждено.WAV', winsound.SND_LOOP)
            elif Executive_voice == 2:
                winsound.PlaySound('Хорошо.WAV', winsound.SND_LOOP)
            elif Executive_voice == 3:
                winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
            elif Executive_voice == 4:
                winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
            elif Executive_voice == 5:
                winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Хорошовампровестивремя.WAV', winsound.SND_LOOP)
            system('shutdown /r /f /t 10 /c "Перезагрузка будет выполнена через 10 секунд"')
            self.quite()
        elif (fuzz.ratio(text, 'отмена') > 70) or (fuzz.ratio(text, 'нет') > 70):
            Executive_voice = randint(0, 1)
            if Executive_voice == 0:
                winsound.PlaySound('Действиенеподтверждено.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Запросневыполнен.WAV', winsound.SND_LOOP)
        else:
            Executive_voice = randint(0, 1)
            if Executive_voice == 0:
                winsound.PlaySound('Действиенеподтверждено.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Запросневыполнен.WAV', winsound.SND_LOOP)

    def calc(self):
        Executive_voice = randint(1, 6)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Открываюкалькулятор.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
                winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        elif Executive_voice == 5:
            winsound.PlaySound('сейчасоткрою.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Калькулятороткрыт.WAV', winsound.SND_LOOP)
        system('calc')

    def open_web(self):
        webbrowser.open(Assistant.settings['SETTINGS']['web'])
        Executive_voice = randint(1, 9)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Открываюинтернет.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('Открываюбраузер.WAV', winsound.SND_LOOP)
        elif Executive_voice == 5:
            winsound.PlaySound('Браузероткрыт.WAV', winsound.SND_LOOP)
        elif Executive_voice == 6:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        elif Executive_voice == 7:
            winsound.PlaySound('сейчасоткрою.WAV', winsound.SND_LOOP)
        elif Executive_voice == 8:
            winsound.PlaySound('открываюдоступкинформации.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Интернетоткрыт.WAV', winsound.SND_LOOP)

    def YouTube(self):
        webbrowser.open('https://www.youtube.com/')
        time.sleep(2)
        pg.hotkey('winleft', 'up')
        Executive_voice = randint(1, 6)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('ютуботкрыт.WAV', winsound.SND_LOOP)
        elif Executive_voice == 5:
            winsound.PlaySound('сейчасоткрою.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('открываюютуб.WAV', winsound.SND_LOOP)
        time.sleep(2)
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('желаетеоткрытьпервоевидео.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('яоткроюпервоевидеодлявасиливысами.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('запуститпервоевидео.WAV', winsound.SND_LOOP)
        self.text = self.listen()
        print(self.text)
        if (fuzz.ratio(self.text, 'давай') > 70) or (fuzz.ratio(self.text, 'да') > 70) or (fuzz.ratio(self.text, "открой") > 70)\
        or (fuzz.ratio(self.text, "открывай") > 70) or (fuzz.ratio(self.text, "да давай") > 70):
            Executive_voice = randint(1, 4)
            if Executive_voice == 1:
                winsound.PlaySound('запускаю.WAV', winsound.SND_LOOP)
            elif Executive_voice == 2:
                winsound.PlaySound('приятногопросмотра.WAV', winsound.SND_LOOP)
            elif Executive_voice == 3:
                winsound.PlaySound('запускаювидео.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('открываювидео.WAV', winsound.SND_LOOP)
            pg.leftClick(438, 310)
        elif fuzz.ratio(self.text, 'нет') > 70 or (fuzz.ratio(self.text, 'не надо') > 70)\
        or (fuzz.ratio(self.text, 'нет не надо') > 70) or (fuzz.ratio(self.text, 'я сам') > 70):
            Executive_voice = randint(1, 4)
            if Executive_voice == 1:
                winsound.PlaySound('надеюсьвынайдетечтоискали.WAV', winsound.SND_LOOP)
            elif Executive_voice == 2:
                winsound.PlaySound('приятногопросмотра.WAV', winsound.SND_LOOP)
            elif Executive_voice == 3:
                winsound.PlaySound('удачнопровестивремя.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Хорошовампровестивремя.WAV', winsound.SND_LOOP)

    def YouTube_dop(self):
        Executive_voice = randint(1, 4)
        if Executive_voice == 1:
            winsound.PlaySound('запускаю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('приятногопросмотра.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        pg.leftClick(1325, 269)

    def VK(self):
        webbrowser.open('https://vk.com/feed')
        Executive_voice = randint(1, 5)
        if Executive_voice == 1:
            winsound.PlaySound('открываювконтакте.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('вконтактеоткрыт.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('вкоткрыт.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('сейчасоткрою.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('открываювк.WAV', winsound.SND_LOOP)

    def Teleg(self):
        webbrowser.open('https://web.telegram.org/k/')
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('телеграмоткрыт.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('открываютнлнграм.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('сейчасоткрою.WAV', winsound.SND_LOOP)


    def mail(self):
        webbrowser.open('https://mail.google.com/')
        Executive_voice = randint(1, 6)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('открываюпочту.WAV', winsound.SND_LOOP)
        elif Executive_voice == 5:
            winsound.PlaySound('сейчасоткрою.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('почтаоткрыта.WAV', winsound.SND_LOOP)

    def music(self):
        mus = randint(1, 3)
        if mus == 1:
            webbrowser.open(Assistant.settings['SETTINGS']['PLIST'])
        if mus == 2:
            webbrowser.open(Assistant.settings['SETTINGS']['Phonk'])
        else:
            webbrowser.open(Assistant.settings['SETTINGS']['MUSVIBE'])
        pg.hotkey('winleft', 'up')
        time.sleep(3)
        Executive_voice = randint(1, 5)
        if Executive_voice == 1:
            winsound.PlaySound('поймайтевайбсмузыкой.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('приятного прослушивания.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('ставлюплейлист.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('включаюмузыку.WAV', winsound.SND_LOOP)
        time.sleep(6)
        pg.leftClick(850, 672)
        pg.leftClick(850, 601)

    def web_search(self, search):
        words = ['венди найди в интернете', 'венди ищи', 'венди кто такой', 'венди что такое', 'венди кто такая', 'венди когда',\
        'венди найди кто такой', 'венди найди что такое', 'венди найди кто такая', 'венди найди когда', 'венди как работает',\
        'найди в интернете', 'найди кто такой', 'найди что такое', 'найди кто такая', 'найди когда', 'найди как работает',]
        remove = ['пожалуйста', 'ладно', 'давай', 'сейчас']
        for i in words:
            search = search.replace(i, '')
            for j in remove:
                search = search.replace(j, '')
                search = search.strip()
        Executive_voice = randint(1, 8)
        if Executive_voice == 1:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('обращаюськумнойпаутине.WAV', winsound.SND_LOOP)
        elif Executive_voice == 5:
            winsound.PlaySound('спрашиваювинтернете.WAV', winsound.SND_LOOP)
        elif Executive_voice == 6:
            winsound.PlaySound('сейчаснайду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 7:
            winsound.PlaySound('открываюдоступкинформации.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('ищувашзапросвинтернете.WAV', winsound.SND_LOOP)
        webbrowser.open(f'https://duckduckgo.com/?q={search}&t=ffab&atb=v399-2&ia=web')
        time.sleep(2)
        pg.hotkey('winleft', 'up')

    def YouTube_search(self, search):
        wordsY = ['венди найди на ютубе', 'венди найди на ютуби', 'венди найди на youtube', 'венди открой на youtube', 'венди открой на ютубе', 'венди открой на ютуби'\
        'найди на ютубе', 'найди на ютуби', 'найди на youtube', 'открой на youtube', 'открой на ютубе', 'открой на ютуби', 'венди найди на ютубе кто такой']
        removeY = ['пожалуйста', 'ладно', 'давай', 'сейчас']
        for i in wordsY:
            search = search.replace(i, '')
            for j in removeY:
                search = search.replace(j, '')
                search = search.strip()
        Executive_voice = randint(1, 7)
        if Executive_voice == 1:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('пытаюсьнайтивашзапроснаютубе.WAV', winsound.SND_LOOP)
        elif Executive_voice == 5:
            winsound.PlaySound('ищувашзапроснаютубе.WAV', winsound.SND_LOOP)
        elif Executive_voice == 6:
            winsound.PlaySound('сейчаснайду.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('открываюдоступкинформации.WAV', winsound.SND_LOOP)
        webbrowser.open(f'https://www.youtube.com/results?search_query={search}')
        time.sleep(2)
        pg.hotkey('winleft', 'up')
        time.sleep(5)
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('желаетеоткрытьпервоевидео.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('яоткроюпервоевидеодлявасиливысами.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('запуститпервоевидео.WAV', winsound.SND_LOOP)
        self.text = self.listen()
        print(self.text)
        if (fuzz.ratio(self.text, 'давай') > 70) or (fuzz.ratio(self.text, 'да') > 70) or (fuzz.ratio(self.text, "открой") > 70) or (fuzz.ratio(self.text, "открывай") > 70)\
        or (fuzz.ratio(self.text, "запусти") > 70) or (fuzz.ratio(self.text, "запускай") > 70):
            Executive_voice = randint(1, 4)
            if Executive_voice == 1:
                winsound.PlaySound('запускаю.WAV', winsound.SND_LOOP)
            elif Executive_voice == 2:
                winsound.PlaySound('приятногопросмотра.WAV', winsound.SND_LOOP)
            elif Executive_voice == 3:
                winsound.PlaySound('запускаювидео.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('открываювидео.WAV', winsound.SND_LOOP)
            pg.leftClick(578, 298)
            pg.leftClick(552, 540)
        elif fuzz.ratio(self.text, 'нет') > 70 or (fuzz.ratio(self.text, 'не надо') > 70):
            Executive_voice = randint(1, 4)
            if Executive_voice == 1:
                winsound.PlaySound('надеюсьвынайдетечтоискали.WAV', winsound.SND_LOOP)
            elif Executive_voice == 2:
                winsound.PlaySound('приятногопросмотра.WAV', winsound.SND_LOOP)
            elif Executive_voice == 3:
                winsound.PlaySound('удачнопровестивремя.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('Хорошовампровестивремя.WAV', winsound.SND_LOOP)

    def translateRU(self, task):
        Executive_voice = randint(1, 5)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('пробуюперевести.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('сейчаспереведу.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('перевожу.WAV', winsound.SND_LOOP)

        variants = ['венди переведи на английский', 'венди перевести на английский', 'венди перевести на английский', 'переведи на английский', 'перевести на английский',\
        'перевести на английский']

        for i in variants:
            print(i)
            task = task.replace(i, '').replace('  ', ' ')
        print(task)
        webbrowser.open(f'https://www.deepl.com/ru/translator#ru/en/{task}')

    def translateEN(self, task):
        Executive_voice = randint(1, 5)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('перевожу.WAV', winsound.SND_LOOP)
        elif Executive_voice == 3:
            winsound.PlaySound('сейчаспереведу.WAV', winsound.SND_LOOP)
        elif Executive_voice == 4:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('пробуюперевести.WAV', winsound.SND_LOOP)

        varia = ['венди переведи на русский', 'венди перевести на русский', 'венди перевести на русский', 'переведи на русский', 'перевести на русский',\
        'перевести на русский']

        for i in varia:
            print(i)
            task = task.replace(i, '').replace('  ', ' ')
        print(task)
        webbrowser.open(f'https://www.deepl.com/en/translator#en/ru/{task}')

    def Folder(self, task):
        dels = ['венди создай папку', 'венди создать папку', 'венди создай папку с именем', 'венди создать папку с именем', 'создай папку', 'создать папку',\
        'создай папку с именем', 'создать папку с именем']
        for i in dels:
            task = task.replace(i, '').replace('  ', ' ').strip()

            if not path.exists(task):
                os.chdir(Assistant.settings['SETTINGS']['Desktop'])
                os.mkdir(f'{task}')
                Executive_voice = randint(1, 6)
                if Executive_voice == 1:
                    winsound.PlaySound('генерирую.WAV', winsound.SND_LOOP)
                elif Executive_voice == 2:
                    winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
                elif Executive_voice == 3:
                    winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
                elif Executive_voice == 4:
                    winsound.PlaySound('создаюпапку.WAV', winsound.SND_LOOP)
                elif Executive_voice == 5:
                    winsound.PlaySound('папкасоздается.WAV', winsound.SND_LOOP)
                else:
                    winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)
                Assistant.last_dir = task

    def ShortLink(self):
        winsound.PlaySound('введитессылку.WAV', winsound.SND_LOOP)
        link = input('Введите ссылку: ')
        if link == '':
            Executive_voice = randint(1, 2)
            if Executive_voice == 1:
                winsound.PlaySound('строкадляссылкипуста.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('выничегоневвели.WAV', winsound.SND_LOOP)
        else:
            Executive_voice = randint(1, 3)
            if Executive_voice == 1:
                winsound.PlaySound('вашассылкаготова.WAV', winsound.SND_LOOP)
            elif Executive_voice == 2:
                winsound.PlaySound('генерирую.WAV', winsound.SND_LOOP)
            else:
                winsound.PlaySound('ссылкаукорочена.WAV', winsound.SND_LOOP)
            print(pyshorteners.Shortener().tinyurl.short(link))

    def alarm_clock(self, text):
        time = datefinder.find_dates(text)
        date_and_time = ''
        for date_and_time in time:
            print(date_and_time)
        date_time = str(date_and_time)
        only_time = date_time[11:]
        print(only_time)
        winsound.PlaySound('будильникустановлен.WAV', winsound.SND_LOOP)
        hour_time = int(only_time[:-6])
        min_time = int(only_time[3:-3])

        count = 0

        while True:
            if hour_time == datetime.datetime.now().hour:
                if min_time <= datetime.datetime.now().minute:
                    if count < 3:
                        print('Будильник сработал!')
                        winsound.PlaySound('Будильник.wav', winsound.SND_LOOP)
                        count += 1
                    else:
                        break
                else:
                    self.recognizer()
            else:
                self.recognizer()

    def VUP(self, text):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(-0.0, None)
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)

    def VDOWN(self, text):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(-30.0, None)
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)

    def VMIDLE(self, text):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(-9.9, None)
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)

    def V75(self, text):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(-4.2, None)
        Executive_voice = randint(1, 3)
        if Executive_voice == 1:
            winsound.PlaySound('Выполняю.WAV', winsound.SND_LOOP)
        elif Executive_voice == 2:
            winsound.PlaySound('Секунду.WAV', winsound.SND_LOOP)
        else:
            winsound.PlaySound('одинмомент.WAV', winsound.SND_LOOP)

    #слушает
    def listen(self):
        self.text = ''

        with sr.Microphone() as source:
            print(f"Я вас слушаю...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, phrase_time_limit=300, timeout=20)
            try:
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
            return self.text

#Отдельный запуск функций
Assistant().HI()

#бесконечный цикл
while True:
    try:
        Assistant().recognizer()
    except Exception as ex:
        print(ex)
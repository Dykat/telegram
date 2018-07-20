import requests
# Парсинг а примере сайта https://baraholka.onliner.by/viewforum.php?f=214
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import json
import telebot
import constants
from time import sleep


def get_html(urls):
    r = requests.get(urls)
    return r.text

def get_all_links(html):
    # блок который парсим
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('table', class_='ba-tbl-list__table')
    divs = soup.find_all('h2',class_='wraptxt')
    links = []
    # теги, потом изменю или добавлю дополнения
    for div in divs:
        a = div.find('a').get('href')
        b = div.find('a').text.strip()        
        link = 'https://baraholka.onliner.by' + a.strip('.')  +'\n ' # +'    ' + b  +'\n   '# '    ' + c + str(d) +'\n   '        
        links.append(link)                
    return links

def mains():
    start = datetime.now()  # время
    urls = 'https://baraholka.onliner.by/viewforum.php?f=214'
    all_links = get_all_links(get_html(urls)) 
    result_list = []
    for i in all_links:
        result_list.append (i)
    return result_list[5]
    
URL = 'https://api.telegram.org/bot' + '607161646:AAEL58emfphC434NbsZyoY861IUjxob8kqg' + '/'

global last_update_id
last_update_id = 0


def get_updates():
    # получим пакеты обновлений о тех сообщениях которые пишем боту
    url = URL + str('getupdates')  # Содержание переменной URL+метод getupdates
    r = requests.get(url)  # переменная в которой будет сохраняться ответ сервера
    return r.json()  # будет нам возвращать


def get_message():
    data = get_updates()  # вызовим ф-цию get_updates
    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:# если последнее объявление такое же как и предыдущее то ничего не выводит
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']

        message = {'chat_id': chat_id,
                   'text': message_text}
        return message
    return None


def send_message(chat_id, text='подождите секунду'):
    url = URL + str('sendmessage?chat_id={}&text={}').format(chat_id,
                                                             text)  # Содержание переменной URL+метод sendmessage
    requests.get(url)


def main():

    d = get_updates()
    with open('updates.json',
              'w') as file:  # запуск контекстного менеджера with и открытие файла для записи который назвали updates.json, открытие его для записи в которой флаг w и запись его в переменную file
        json.dump(d, file, indent=2,
                  ensure_ascii=False)  # обращаюсь к модулю json у его есть метод dump(означает запись в файл)туда мы записываем содиржимое переменной d в файловый обьект file. затем делаем отступы, и по скольку там были кирилические символы выключаем этот флаг

    while True:
        answer = get_message()
        if answer != None: #сли объявление не такое же как предыдущее то отправляет в телеграм
            chat_id = answer['chat_id']
            text = answer['text']  
            send_message(chat_id, mains())  # вместо mains переменная которая сохраняет результаты парсинга
        
        if answer == None:
            continue
        sleep(2)



        
if __name__ == '__main__':  # создаем точку входа
    main()  # с этого будет запускаться


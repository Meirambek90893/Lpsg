from email.message import Message
from operator import index
import sqlite3 
import logging
from turtle import update
from urllib import request
from aiogram import Bot,Dispatcher,executor,types
from config import Token
from random import*
import requests
from bs4 import BeautifulSoup as b



logging.basicConfig(level=logging.INFO)

bot = Bot(token=Token)

dp = Dispatcher(bot)

status = 0

def notebook(text):
    prise_list = []

    ber = f"https://kz.e-katalog.com/ek-list.php?search_={text}+&katalog_from_search_=298"
    

    r = requests.get(ber)
    sed = b(r.text,"html.parser")
    des = sed.find_all("td",class_="model-conf-title")
    
    
    if des != True:
        for i in des:

            ced = i.find("a")
            teg = ced.get("href")
                    
            limp = "https://kz.e-katalog.com/"+teg
            
            r1 = requests.get(limp)
            soy = b(r1.text, "html.parser")
                    
            name = soy.find("h1",class_="t2 no-mobile")
            name = name.text
                    

            clas1 = soy.find('div',class_="img200 h")
            amg = clas1.findChildren('img')[0]
            amg1 = "https://kz.e-katalog.com/"+amg['src']
            prise_list.insert(0,[limp,name,amg1])
            if des.index(i)== 9:
                break
        return prise_list
    else:
        return prise_list
def phone(text):
    price_list = []
    ase = "https://kz.e-katalog.com/ek-list.php?search_="+text
    r = requests.get(ase)
    xro = b(r.text,"html.parser")
    ten = xro.find_all('a',class_='model-short-title no-u')
    
   
    if ten != True:
        for i in ten:
            teg = i.get('href')
            limp = "https://kz.e-katalog.com/"+teg
            r = requests.get(limp)
            
            soup = b(r.text, "html.parser")
            name = soup.find("div", class_ = "fix-menu-name ib")
            price = name.find("a").text  # забирает цену телефона
            name.find("a").extract() # убирает тэг ребенка короткий путь
            name = name.text
                

            clas1 = soup.find('div',class_="img200 h")
            amg = clas1.findChildren('img')[0]
            amg1 = "https://kz.e-katalog.com/"+amg['src']
            price_list.insert(0,[limp,name,amg1])
                
            if ten.index(i)== 9:
                break
        return price_list
    else:
        return price_list
@dp.message_handler(commands=['start'])
async def flit(message:types.Message):



     
    await bot.send_message(message.chat.id,'Привет')

@dp.message_handler(commands=['price'])
async def flit(message:types.Message):
    menu1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ityms1 = types.KeyboardButton = "Нотбуки"
    ityms2 = types.KeyboardButton = "Телефоны"
    menu1.add(ityms1,ityms2)

    await bot.send_message(message.chat.id,"Выберите технику",reply_markup=menu1)

@dp.message_handler(content_types=['text'])   
async def go(message):

    global status
    
    if message.text == "Нотбуки":
        status = 1
        await bot.send_message(message.chat.id,"Название товара" )
        
    elif message.text == "Телефоны":
        status = 2
        await bot.send_message(message.chat.id,"Название товара")
       
    elif status == 1:
        one2 = notebook(message.text)
        if len(one2) != 0:
            for i in one2 :
                await bot.send_photo(message.chat.id,i[0],caption = f"<a href='{i[0]}'>{i[1]} </a>",parse_mode="HTML" )
        else:
            await bot.send_message(message.chat.id,"проверить данные Ноутбука")
     
    elif status == 2:
        one1 = phone(message.text)
        
        if len(one1)  != 0:
            for i in one1:
                await bot.send_photo(message.chat.id,i[0],caption = f"<a href='{i[0]}'>{i[1]} </a>",parse_mode="HTML")
        else:
            await bot.send_message(message.chat.id,"проверить данные Телефона")
    elif status == 0:
        await bot.send_message(message.chat.id,"выбери название техники")
    
    
if __name__ == '__main__': 
   executor.start_polling(dp) 
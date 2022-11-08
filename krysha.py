import requests
from bs4 import BeautifulSoup as b
import logging
from aiogram import Bot,Dispatcher,executor,types
from config import Token
from random import*

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Token)

dp = Dispatcher(bot)


def h4():
    
    URL = "https://krisha.kz/prodazha/kvartiry/"
    r = requests.get(URL)
    soup = b(r.text, "html.parser")
    tem = soup.find_all("a", class_= "a-card__title tm-click-checked-hot-adv")
    # tem2 = soup.find_all('a',class_="a-card__title")
    
    link_list = []
    img_list = []
    name_list = []
    price_list = []
    for i in tem:
        sub = i.get('href') # филт на ссылки
        der = 'https://krisha.kz/'+sub
        link_list.append(der)
        r = requests.get(der)
        soup = b(r.text, "html.parser")
        try:
            img = soup.find("div", class_= "gallery__small-item active")
            filtr = img.get("data-photo-url")
            img_list.append(filtr)
        except:
             img_list.append("пусто")
        name = soup.find("div",class_="offer__advert-title")
        fnm = name.findChildren("h1")
        
        for dew in fnm:
            perebor = dew.text
            rep = perebor.replace(" ","")
            cet = rep.replace("\n","")
            name_list.append(cet)
        red = requests.get(der)
        ded = b(red.text,'html.parser')
        sdf = ded.find_all('div',class_="offer__price")    
        for feq in sdf:
            zel = feq.text
            
            cet = zel.replace("\n","")
            price_list.append(cet)


    
    return link_list,img_list,name_list,price_list
        
@dp.message_handler(commands=['Info'])
async def flit(message:types.Message):
    all_info = h4()
    link_list = all_info[0]
    img_list = all_info[1]
    name_list = all_info[2]
    price_list = all_info[3]
 
    await bot.send_photo(message.chat.id,img_list[0],caption=f"<a href='{link_list[0]}'>{name_list[0]+price_list[0]} </a>",parse_mode="HTML")


if __name__ == '__main__': 
   executor.start_polling(dp) 







import telebot
from telebot import types
import config
import pandas as pd
import requests

dataframe = pd.read_csv("./data/atlas_raw_rb.csv")
cityframe = pd.read_csv("./data/day_light_data.csv")
bot = telebot.TeleBot(config.token)

# Старт бота
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
user = bot.get_me()
btn1 = types.KeyboardButton("/start")


is_on_chatbot = 0
is_on_library = 0
is_plant_selected = 0
is_on_city = 0
is_city_selected = 0

class PlantData:
    def __init__(self,plant_data):
        self.plant_data = plant_data
        self.name = self.plant_data["Название"]
        self.descr = self.plant_data["Описание"]
        self.atlas = self.plant_data['Атлас']
        self.other = self.plant_data['Другие виды']
        self.areal = self.plant_data['Ареал']
        self.resour = self.plant_data['Ресурсы']
        self.vozdel = self.plant_data['Возделывание']
        self.chem = self.plant_data['Химический состав']
        self.raw = self.plant_data['Сырьё']
        self.pharm = self.plant_data['Фармакологические свойства']
        self.redbook = self.plant_data['Краснокнижные регионы']

class DayLightData:
    def __init__(self, day_light_data):
        self.day_light_data = day_light_data
        self.city = self.day_light_data["Город"]
        self.region = self.day_light_data["Регион"]
        self.district = self.day_light_data['Федеральный округ']
        self.dlwin = int(self.day_light_data['Средний световой день (зима)'])
        self.dcwin = int(self.day_light_data['Количество световых дней (зима)'])
        self.dlspr = int(self.day_light_data['Средний световой день (весна)'])
        self.dcspr = int(self.day_light_data['Количество световых дней (весна)'])
        self.dlsum = int(self.day_light_data['Средний световой день (лето)'])
        self.dcsum = int(self.day_light_data['Количество световых дней (лето)'])
        self.dlaut = int(self.day_light_data['Средний световой день (осень)'])
        self.dcaut = int(self.day_light_data['Количество световых дней (осень)'])
        self.dall = int(self.day_light_data["Количество световых дней в году"])

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать работу")
    btn2 = types.KeyboardButton("❓ Информация")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот поддержки принятия решений при выборе лекарственных культур".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(f"[LOG] {message.from_user.username}: {message.text}")

    if message.text =="Вернуться в главное меню":
        global is_plant_selected
        is_plant_selected=0
        global is_on_library
        is_on_library = 0
        global is_on_city
        is_on_city = 0
        global is_city_selected
        is_city_selected = 0
        global is_on_chatbot
        is_on_chatbot = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Начать работу")
        btn2 = types.KeyboardButton("❓ Информация")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}! Я бот поддержки принятия решений при выборе лекарственных культур".format(message.from_user), reply_markup=markup)
    elif message.text == "/help":
         bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text =="❓ Информация":
        bot.send_message(message.from_user.id, u"Мы представляем систему поддержки принятия решений для фермерских хозяйств, связанных с выращиванием лекарственных растений. Наша система даёт возможность получать интересующую информацию о культурах, используемых в производстве фармацевтических препаратов и получать рекомендации по их посеву. Она также позволяет фермеру выбрать культуры пригодные для выращивания в определённом регионе, не тратя время на анализ различных источников.")
    elif message.text =="Начать работу":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        gen_model = types.KeyboardButton("Чатбот")
        library = types.KeyboardButton("Справочник")
        city_info = types.KeyboardButton("Информация по населённому пункту")
        return_to_start = types.KeyboardButton("Вернуться в главное меню")
        markup.add(gen_model,library, city_info, return_to_start)
        bot.send_message(message.chat.id, text="Выбери нужный пункт, чтобы продолжить", reply_markup=markup)

    elif message.text =="Чатбот":
        is_on_chatbot = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        return_to_start = types.KeyboardButton("Вернуться в главное меню")
        markup.add(return_to_start)
        info = "👋 Привет, я чат-бот помощник! Я могу проконсультировать тебя по вопросам, связанными с растениями. \n\n🗒 Напиши вопрос о растении, которое тебя интересует, а я постараюсь ответить.\n❗️ Учти, что мой ответ может занять от ДВУХ до НЕСКОЛЬКИХ МИНУТ.\n\n Примеры запросов:\n - Какой ареал у алоэ древовидного?\n - Какой химический состав у лёна посевого?\n - Как применяют в медицине василек благословенный?"
        bot.send_message(message.chat.id, text=info, reply_markup=markup)
        

    elif message.text == "Информация по населённому пункту":
        is_on_city = 1
        is_city_selected = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        return_to_start = types.KeyboardButton("Вернуться в главное меню")
        markup.add(return_to_start)
        bot.send_message(message.chat.id, text="Введите название вашего населённого пункта", reply_markup=markup)

    elif message.text =="Справочник" or message.text=="Вернуться в справочник":
        is_plant_selected = 0
        is_on_library = 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        return_to_start = types.KeyboardButton("Вернуться в главное меню")
        markup.add(return_to_start)
        bot.send_message(message.chat.id, text="Введите название растения", reply_markup=markup)

    else:
        # Чатбот
        if is_on_chatbot == 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            return_to_start = types.KeyboardButton("Вернуться в главное меню")
            markup.add(return_to_start)
            data = {'text': message.text}
            response = requests.post(config.flask_url, data=data)
            # Retrieve the response data
            response_data = response.json()
            # Print the response
            bot.send_message(message.chat.id, text=response_data['response'], reply_markup=markup)
        # Город
        if is_on_city==1:
            entered_name = message.text.lower()
            city_names = cityframe["Город"]
            similar_cities = []
            is_city_selected = 0
            for index, name in enumerate(city_names):

                if entered_name == name.lower():
                    global dld
                    dld = DayLightData(cityframe.loc[index])

                    is_city_selected = 1
                if index == len(city_names):
                    is_city_selected = 0

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            return_to_start = types.KeyboardButton("Вернуться в главное меню")
            markup.add(return_to_start)
            if  is_city_selected == 1:
                bot.send_message(message.chat.id, text=f"Выбран населённый пункт: {dld.city}")
                bot.send_message(message.chat.id, text=f"Регион: {dld.region}")
                bot.send_message(message.chat.id, text=f"Федеральный округ: {dld.district}")
                bot.send_message(message.chat.id, text=f"Средний световой день (зима), часы: {dld.dlwin}")
                bot.send_message(message.chat.id, text=f"Количество световых дней (зима): {dld.dcwin}")
                bot.send_message(message.chat.id, text=f"Средний световой день (весна), часы: {dld.dlspr}")
                bot.send_message(message.chat.id, text=f"Количество световых дней (весна): {dld.dcspr}")
                bot.send_message(message.chat.id, text=f"Средний световой день (лето), часы: {dld.dlsum}")
                bot.send_message(message.chat.id, text=f"Количество световых дней (лето): {dld.dcsum}")
                bot.send_message(message.chat.id, text=f"Средний световой день (осень), часы: {dld.dlaut}")
                bot.send_message(message.chat.id, text=f"Количество световых дней (осень): {dld.dcaut}")
                bot.send_message(message.chat.id, text=f"Количество световых дней в году: {dld.dall}")
                bot.send_message(message.chat.id, text="Введите название вашего населённого пункта", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text=f"Населённый пункт не найден, попробуйте изменить запрос",reply_markup=markup)
        # Cправочник
        if is_on_library == 1:
            if is_plant_selected!=1:
                entered_name = message.text.lower()
                names = dataframe["Название"]
                for index, name in enumerate(names):
                    if entered_name in name:
                        global plant_data
                        plant_data = PlantData(dataframe.loc[index])

                        is_plant_selected = 1

                if is_plant_selected==1:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    descr = types.KeyboardButton("Описание")
                    another_tps = types.KeyboardButton("Другие виды")
                    areal = types.KeyboardButton("Ареал")
                    atlas = types.KeyboardButton("Атлас")
                    res = types.KeyboardButton("Ресурсы")
                    voz = types.KeyboardButton("Возделывание")
                    chem = types.KeyboardButton("Химический состав")
                    raw = types.KeyboardButton("Сырьё")
                    pharm = types.KeyboardButton("Фармакологические свойства")
                    redbook = types.KeyboardButton("Краснокнижные регионы")
                    library = types.KeyboardButton("Вернуться в справочник")
                    print(is_on_library, is_plant_selected)
                    return_to_start = types.KeyboardButton("Вернуться в главное меню")
                    markup.add(descr, another_tps, areal,atlas,res,voz,chem,raw,pharm,redbook, library,return_to_start)
                    bot.send_message(message.chat.id, text=f"Выбрано растение: {plant_data.name}")
                    bot.send_message(message.chat.id, text="Выберите нужный пункт", reply_markup=markup)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    library = types.KeyboardButton("Вернуться в справочник")
                    return_to_start = types.KeyboardButton("Вернуться в главное меню")
                    is_on_library = 0
                    markup.add(library, return_to_start)
                    bot.send_message(message.chat.id, text="Растение не найдено, выберите один из пунктов", reply_markup=markup)
        try:
            if message.text == "Описание" and is_plant_selected==1:

                    if len(plant_data.descr) > 4095:
                        for x in range(0, len(plant_data.descr), 4095):
                            bot.send_message(message.chat.id, text=plant_data.descr[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.descr)
            if message.text == "Атлас" and is_plant_selected==1:

                    if len(plant_data.atlas) > 4095:
                        for x in range(0, len(plant_data.atlas), 4095):
                            bot.send_message(message.chat.id, text=plant_data.atlas[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.atlas)
            if message.text == "Другие виды" and is_plant_selected==1:

                    if len(plant_data.other) > 4095:
                        for x in range(0, len(plant_data.other), 4095):
                            bot.send_message(message.chat.id, text=plant_data.other[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.other)
            if message.text == "Ареал" and is_plant_selected==1:

                    if len(plant_data.areal) > 4095:
                        for x in range(0, len(plant_data.areal), 4095):
                            bot.send_message(message.chat.id, text=plant_data.areal[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.areal)
            if message.text == "Ресурсы" and is_plant_selected==1:

                    if len(plant_data.resour) > 4095:
                        for x in range(0, len(plant_data.resour), 4095):
                            bot.send_message(message.chat.id, text=plant_data.resour[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.resour)
            if message.text == "Возделывание" and is_plant_selected==1:

                    if len(plant_data.vozdel) > 4095:
                        for x in range(0, len(plant_data.vozdel), 4095):
                            bot.send_message(message.chat.id, text=plant_data.vozdel[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.vozdel)
            if message.text == "Химический состав" and is_plant_selected==1:

                    if len(plant_data.chem) > 4095:
                        for x in range(0, len(plant_data.chem), 4095):
                            bot.send_message(message.chat.id, text=plant_data.chem[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.chem)
            if message.text == "Сырьё" and is_plant_selected==1:

                    if len(plant_data.raw) > 4095:
                        for x in range(0, len(plant_data.raw), 4095):
                            bot.send_message(message.chat.id, text=plant_data.raw[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.raw)
            if message.text == "Фармакологические свойства" and is_plant_selected==1:

                    if len(plant_data.pharm) > 4095:
                        for x in range(0, len(plant_data.pharm), 4095):
                            bot.send_message(message.chat.id, text=plant_data.pharm[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.pharm)
            if message.text == "Краснокнижные регионы" and is_plant_selected==1:

                    if len(plant_data.redbook) > 4095:
                        for x in range(0, len(plant_data.redbook), 4095):
                            bot.send_message(message.chat.id, text=plant_data.redbook[x:x + 4095])
                    else:
                        bot.send_message(message.chat.id, text=plant_data.redbook)
        except:
            bot.send_message(message.chat.id, text="Информация отсутствует. Измените запрос.")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "1":
            pass

bot.polling(none_stop=True, interval=0)
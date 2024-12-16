"""
Модуль в котором содержаться потоки Qt
"""
import datetime
import time
import requests

from PySide6 import QtCore



class WeatherHandler(QtCore.QThread):
    wheatherHandlerSignal = QtCore.Signal(str)  # Пропишите сигналы, которые считаете нужными

    def __init__(self, city: str, parent=None):
        super().__init__(parent)
        self.__city = city
        self.__delay = 10
        self.__status = None
        self.delay1 = 1

    def set_city(self, city: str) -> None:
        self.__city = city

    def get_weather(self):
        open_weather_token = "1044ae1ab27265501dac183236ffd563"

        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={self.__city}&appid={open_weather_token}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            mes_repl = (f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
                        f"Погода в населенном пункте: {city}\nТемпература: {cur_weather}C° {wd}\n"
                        f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                        f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                        )
        except:
            mes_repl = "Проверьте название города"
        return mes_repl

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.delay1 = delay

    def run(self) -> None:
        while True:
            self.wheatherHandlerSignal.emit(self.get_weather())
            time.sleep(self.delay1)

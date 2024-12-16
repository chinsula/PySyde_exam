"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads
Создавать форму можно как в ручную, так и с помощью программы Designer
Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""
from PySide6 import QtWidgets
from a_threads import WeatherHandler


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.__initSignals()

    def initUi(self):
        """
        Инициализация Ui
        :return: None
        """
        self.inputSity = QtWidgets.QLineEdit()
        self.inputSity.setPlaceholderText("Введите название населенного пункта")
        # self.inputDelay = QtWidgets.QLineEdit()
        # self.inputDelay.setPlaceholderText("Введите время задержки")
        self.outputWheather = QtWidgets.QTextEdit()
        self.outputWheather.setEnabled(False)
        self.pushButtonHandle = QtWidgets.QPushButton("Старт")
        self.pushButtonHandle.setCheckable(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.inputSity)
        # layout.addWidget(self.inputDelay)
        layout.addWidget(self.outputWheather)
        layout.addWidget(self.pushButtonHandle)
        self.setLayout(layout)
        self.setMinimumSize(300, 140)
        self.message = self.inputSity.text()

    def __initSignals(self):
        self.pushButtonHandle.clicked.connect(self.on_started)

    def on_started(self, status):
        self.pushButtonHandle.setText("Стоп" if status else "Старт")
        self.weatherHandler = WeatherHandler("" if not self.inputSity.text() else self.inputSity.text())
        self.weatherHandler.start()
        self.weatherHandler.sleep(self.weatherHandler.delay1)
        # self.weatherHandler.wheatherHandlerSignal.connect(lambda data: print(f"Статус код: {data}"))
        self.weatherHandler.wheatherHandlerSignal.connect(self.apiUpdate)

    def apiUpdate(self, data):
        if self.pushButtonHandle.isChecked():
            self.inputSity.setEnabled(False)
            self.outputWheather.setText(f"{data}")

        elif not self.pushButtonHandle.isChecked():
            self.inputSity.setEnabled(True)





if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window()
    window.show()
    app.exec()



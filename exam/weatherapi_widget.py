"""
Виджет погоды. Обращаемся по названию к населенному пункту, русский язык либо транслит.
Получаем сводку погоды.
"""

from PySide6 import QtWidgets
from threads import WeatherHandler


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
        self.setWindowTitle("Погода в любой точке мира")
        self.inputСity = QtWidgets.QLineEdit()
        self.inputСity.setPlaceholderText("Введите название населенного пункта")
        self.outputWheather = QtWidgets.QTextEdit()
        self.outputWheather.setEnabled(False)
        self.pushButtonHandle = QtWidgets.QPushButton("Старт")
        self.pushButtonHandle.setCheckable(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.inputСity)
        layout.addWidget(self.outputWheather)
        layout.addWidget(self.pushButtonHandle)
        self.setLayout(layout)
        self.setMinimumSize(350, 140)
        self.message = self.inputСity.text()

    def __initSignals(self):
        self.pushButtonHandle.clicked.connect(self.on_started)

    def on_started(self, status: bool):
        """
        Метод для запуска и остановки потока
        :param status: статус запуска потока
        :return: возвращаем состояние, при котором нет активных потоков (при неактивном статусе (False)
        принудительно закрываем поток для исключения состояния гонки)
        """

        self.inputСity.setEnabled(not status)
        self.pushButtonHandle.setText("Стоп" if status else "Старт")
        if not status:
            self.weatherHandler.terminate()
            self.weatherHandler.wait(0.5)
            return
        self.weatherHandler = WeatherHandler("" if not self.inputСity.text() else self.inputСity.text())
        self.weatherHandler.start()
        self.weatherHandler.wheatherHandlerSignal.connect(self.apiUpdate)

    def apiUpdate(self, data):
        self.outputWheather.setText(f"{data}")


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window()
    window.show()
    app.exec()

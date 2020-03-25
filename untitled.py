class MainWindowSlots(Ui_Form):
	
	# Определяем пользовательский слот
	def set_time(self):
		pass
		return None


class MainWindow(MainWindowSlots):

	self.cpBtn.clicked.connect(self.browse_folder)

	def browse_folder(self):
		self.listWidget.clear()
		directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")

	# При инициализации класса нам необходимо выпонить некоторые операции
	def __init__(self, form):
		# Сконфигурировать интерфейс методом из базового класса Ui_Form
		self.setupUi(form)
		# Подключить созданные нами слоты к виджетам
		self.connect_slots()

	# Подключаем слоты к виджетам
	def connect_slots(self):
		#self.pushButton.clicked.connect(self.set_time)
		return None


if __name__ == '__main__':
	# Создаём экземпляр приложения
	app = QApplication(sys.argv)
	# Создаём базовое окно, в котором будет отображаться наш UI
	window = QWidget()
	# Создаём экземпляр нашего UI
	ui = MainWindow(window)
	# Отображаем окно
	window.show()
	# Обрабатываем нажатие на кнопку окна "Закрыть"
	sys.exit(app.exec_())
#-*-coding:utf-8-*-
import os
import re
import sys
import base64
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
import nacl.encoding
import nacl.public

import des
from des import Ui_Form

class ExampleApp(QtWidgets.QMainWindow, des.Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)  #инициализация дизайна
		self.cpBtn.clicked.connect(self.browse_folder)
		self.pkBtn.clicked.connect(self.GEN_PUBLIC_KEY)
		self.sendBtn.clicked.connect(self.ENCODE_FILE)
		self.getBtn.clicked.connect(self.DECODE_FILE)
		self.dftBtn.clicked.connect(self.browse_folder)

	file = 0

	def browse_folder(self):
		global file
		file = QtWidgets.QFileDialog.getOpenFileName(self, "Choose File")[0]
		self.pathToFile.setText(file)

	public_key = 0

	def GEN_PUBLIC_KEY(self):
		global public_key
		public_key = nacl.public.PrivateKey.generate()
		print(public_key.public_key.encode(encoder=nacl.encoding.Base64Encoder).decode('utf-8'))
		self.pkgBox.setText(public_key.public_key.encode(encoder=nacl.encoding.Base64Encoder).decode('utf-8'))

	def ENCODE_FILE(self):
		get_public_key = nacl.public.PublicKey(self.pksBox.text().encode(), encoder=nacl.encoding.Base64Encoder)
		sealed_box = nacl.public.SealedBox(get_public_key)

		os.rename(file, "image.bin")
		in_file = open('image.bin', 'rb')
		data = in_file.read()
		in_file.close()
		os.rename("image.bin", file)
		
		new_data = base64.b64encode(bytes(data)).decode('utf-8')
		rev_data = ""
		for i in range(0, len(new_data)):
			rev_data += new_data[len(new_data)-1-i]

		#re.sub(r'', '', rev_data)
		#rev_data.translate('\/')
		#print(rev_data)
		EXT = file.split('.')
		#print(EXT[1])
		rev_data += EXT[1]
		#print(rev_data[len(rev_data)-3] +  rev_data[len(rev_data)-2] + rev_data[len(rev_data)-1])
		message = str.encode(rev_data)
		self.codeBox.appendPlainText(sealed_box.encrypt(message, encoder=nacl.encoding.Base64Encoder).decode('utf-8'))

	from_txt = False

	def DECODE_FILE(self):
		#global from_txt
		#check = from_txt
		#if (check == False):
			encrypted = self.cfBox.toPlainText().encode()
			print(self.pkgBox.text().encode())
			unseal_box = nacl.public.SealedBox(public_key)
			decode = unseal_box.decrypt(encrypted, encoder=nacl.encoding.Base64Encoder).decode('utf-8')
			#print(decode)
			#self.decodeBox.appendPlainText(unseal_box.decrypt(encrypted, encoder=nacl.encoding.Base64Encoder).decode('utf-8'))

			EXT = decode[len(decode)-3] +  decode[len(decode)-2] + decode[len(decode)-1]

			shutil.copy("bin/_iMain.bin", "dFiles")
			new_data = ""

			for i in range(0, len(decode)-3):
				new_data += decode[i]

			rev_data = ""

			for i in range(0, len(new_data)):
				rev_data += new_data[len(new_data)-1-i]

			new_data = base64.b64decode(rev_data)
			os.rename('dFiles/_iMain.bin', 'dFiles/image.txt')
			out_file = open('dFiles/image.txt', 'wb')
			out_file.write(new_data)
			out_file.close()
			os.rename('dFiles/image.txt', 'dFiles/image.'+ EXT)
		#else:
			#pass


def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = ExampleApp()  # Создаём объект класса ExampleApp
	window.show()  # Показываем окно
	app.exec_()  # запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  # то запускаем функцию main()



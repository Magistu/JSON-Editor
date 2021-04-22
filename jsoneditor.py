from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
import os
import json


class MainWindow(QMainWindow):
	def closeEvent(self, e):
		if not text.document().isModified():
			return
		answer = QMessageBox.question(
 			window, None,
 			"You have unsaved changes. Save before closing?",
 			QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
		)
		if answer & QMessageBox.Save:
			save()
		elif answer & QMessageBox.Cancel:
			e.ignore()

app = QApplication([])
app.setApplicationName("JSON Editor")
text = QPlainTextEdit()
window = MainWindow()
window.setCentralWidget(text)

file_path = None

menuFile = window.menuBar().addMenu("&File")
open_action = QAction("&Open")
def open_file():
	global file_path
	path = QFileDialog.getOpenFileName(window, "Open")[0]
	if path:
		text.setPlainText(open(path).read())
		file_path = path
open_action.triggered.connect(open_file)
open_action.setShortcut(QKeySequence.Open)
menuFile.addAction(open_action)

save_action = QAction("&Save")
def save():
	if file_path is None:
		save_as()
	else:
		with open(file_path, "w") as f:
			f.write(text.toPlainText())
		text.document().setModified(False)
save_action.triggered.connect(save)
save_action.setShortcut(QKeySequence.Save)
menuFile.addAction(save_action)

save_as_action = QAction("Save &As...")
def save_as():
	global file_path
	path = QFileDialog.getSaveFileName(window, "Save As")[0]
	if path:
		file_path = path
		save()
save_as_action.triggered.connect(save_as)
menuFile.addAction(save_as_action)

close = QAction("&Close")
close.triggered.connect(window.close)
menuFile.addAction(close)

menuEdit = window.menuBar().addMenu("&Edit")

extenxion = QAction('&File extenxion', menuEdit, checkable=True)
menuEdit.addAction(extenxion)

add_file_names_action = QAction("&Add File Names")
def add_file_names():
	selected = QFileDialog.getOpenFileNames(window, "Open")[0]
	if selected:
		text.insertPlainText('~~~')
		for num, item in enumerate(selected, start=0):
			if extenxion.isChecked():
				text.insertPlainText(os.path.basename(item))
			else:
				text.insertPlainText(os.path.basename(item).split(".")[0])
			if num != len(selected)-1:
				text.insertPlainText(' ')
		text.insertPlainText('~~~')
add_file_names_action.triggered.connect(add_file_names)
menuEdit.addAction(add_file_names_action)

add_file_names_arrays_action = QAction("&Add File Names Arrays")
def add_file_names_arrays():
	selected = QFileDialog.getExistingDirectory(window, "Open")
	if selected:
		selected=[selected+'/'+f for f in os.listdir(selected)]
		for num, item in enumerate(selected, start=0):
			if (os.path.isfile(item)):
				if extenxion.isChecked():
					selected[num] = [os.path.basename(item)]
				else:
					selected[num] = [os.path.basename(item).split(".")[0]]
			else:
				selected[num] = os.listdir(item)
		selected[0][0]='~~~'+selected[0][0]+'~~~'
		text.insertPlainText(str(selected).replace("'",'"'))
add_file_names_arrays_action.triggered.connect(add_file_names_arrays)
menuEdit.addAction(add_file_names_arrays_action)

convert_action = QAction("&Convert")
def convert():
	template = text.toPlainText()
	data = json.loads(template)
	N = len([*data][0].replace('~~~','').split(' '))
	tdata={}
	rdata={}
	replacements=[]
	keys2=[]
	for i in range(N):
		item=[*data][0]
		if isinstance(item, str):
			if item[0:3:1]==item[-1:-4:-1]=='~~~':
				item=item.replace('~~~','').split(' ')[i]
			key1=item
		for item in data.values():
			if isinstance(item, dict):
				values=list(item.values())
			for num, value in enumerate(values,start=0):
				if isinstance(value, str) and value[0:3:1]==value[-1:-4:-1]=='~~~':
					if N > len(value.replace('~~~','').split(' ')):
						text.setPlainText(template)
						break
					key2=[*item][num]
					val=value.replace('~~~','').split(' ')[i]
					keys2.append(key2)
					replacements.append(val)
				if isinstance(value, list) and isinstance(value[0], list):
					if isinstance(value[0][0], str) and value[0][0][0:3:1]==value[0][0][-1:-4:-1]=='~~~':
						value[0][0]=value[0][0].replace('~~~','')
						if N > len(value):
							text.setPlainText(template)
							break
						key2=[*item][num]
						val=value[i]
						keys2.append(key2)
						replacements.append(val)
		tdata[key1]=data[[*data][0]]
		for num, item in enumerate(replacements,start=0):
			tdata[key1][keys2[num]]=item
		data = json.loads(template)
		rdata.update(tdata)
		tdata={}
	with open('out.json','w') as file:
		json.dump(rdata,file,indent=2)
convert_action.triggered.connect(convert)
menuEdit.addAction(convert_action)

menuHelp = window.menuBar().addMenu("&Help")
about_action = QAction("&About")
menuHelp.addAction(about_action)
def show_about_dialog():
	text = "<center>" \
		   "<h1>JSON Editor</h1>" \
		   "&#8291;" \
		   "</center>" \
		   "<p>Version 1.0<br/>"
	QMessageBox.about(window, "About JSON Editor", text)
about_action.triggered.connect(show_about_dialog)

window.show()
app.exec_()
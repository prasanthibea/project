from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import sqlite3
from datetime import datetime,timedelta, date, time
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from LogInpage import logincheck
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime, QRegExp



class StatusComboBox(QComboBox):
	def __init__(self, parent):
		super().__init__(parent)

		self.setPlaceholderText("Choose the test Mode")
		self.addItems(['Good', 'Under Maintenance'])


#class ReadOnlyTableDelegate(QStyledItemDelegate):
#    def createTableEditor(self, parent, option, index):
#        print('createEditor event fired')
#        return 


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        #print('createEditor event fired')
        return 




class Application(QMainWindow):
	def __init__(self):
		super().__init__()


		self.chamberStatusMainWidget = QWidget()

		## Creating labels for the fields:
		self.chamberStatusLabel = QLabel("Chamber Status Editor:")
		self.chamberStatusLabel.setStyleSheet('''font-weight: bold;
									font:Times;
									text-decoration: underline;
									color: #3745C6;							
									font-size: 30px;
									''')


		# Creating layouts:
		self.chamberStatusEditorLayout = QVBoxLayout()
		

		#Create a table using QtestDetails For SlotBooking:
		self.numberOfRowsofChamberTable = 0
		self.chamberStatusTable = QTableWidget(self.numberOfRowsofChamberTable,3)
		self.chamberStatusTable.setHorizontalHeaderLabels(['Chamber Name','Status','Remarks'])
		self.chamberStatusTable.setStyleSheet("QHeaderView {font: Times; font-size: 10pt; font-weight: bold; }")
		self.chamberStatusTable.setColumnWidth(0,250)
		self.chamberStatusTable.setColumnWidth(1,250)
		self.chamberStatusTable.setColumnWidth(2,250)


		#delegate1 = ReadOnlyTableDelegate(self)
		#self.chamberStatusTable.setItemDelegateForColumn(0, delegate1)
		#self.chamberStatusTable.setItemDelegateForColumn(1, delegate1)
		#self.chamberStatusTable.setItemDelegateForColumn(2, delegate1)
	

		self.chamberStatusTable.setRowCount(39) 

		conn = sqlite3.connect('Test_Chamber.db')
		curs = conn.cursor()
	
		tests = curs.execute("SELECT * FROM All_Chambers").fetchall()
		conn.close() 


		for i in range(len(tests)):
			self.chamberStatusTable.setItem(i,0,QTableWidgetItem(tests[i][0]))


		for i in range(len(tests)):

			combo_Box = StatusComboBox(self)
			self.chamberStatusTable.setCellWidget(i, 1, combo_Box)


		#Adding the chamber Images: 
		#self.Label = QLabel()
		#self.chamberImage = QPixmap("BeALogo.png")
		#self.Label.setPixmap(self.chamberImage)
		#self.chamberStatusTable.setCellWidget(0, 2, self.Label)
		#self.chamberStatusTable.verticalHeader().setDefaultSectionSize(50)
		#self.chamberStatusTable.horizontalHeader().setDefaultSectionSize(200)


		


		delegate = ReadOnlyDelegate(self)
		self.chamberStatusTable.setItemDelegateForColumn(0, delegate)





		self.editTableBtn = QPushButton('Edit')
		self.editTableBtn.setFixedWidth(300)

		self.updateSaveBtn = QPushButton('Update')
		self.updateSaveBtn.setFixedWidth(300)

		self.setStyleSheet('''QPushButton {
									font-weight: bold;
									padding: 5px;
									border-color: #2196F3;
									background: #C83724;
									color: white;
									border-radius: 5;
									font-size: 13px;
									}
								
									QPushButton:hover {
									background: #2196F3;
									color: white;
									}''')


		self.editTableBtn.clicked.connect(self.chamber_status_db1)
		self.updateSaveBtn.clicked.connect(self.chamber_status_db)




		self.chambersTableLayout = QVBoxLayout()
		self.chambersTableLayout.addWidget(self.chamberStatusTable)
		self.chambersTableLayout.addWidget(self.editTableBtn, alignment= Qt.AlignLeft)
		self.chambersTableLayout.addWidget(self.updateSaveBtn, alignment= Qt.AlignRight)


		## Adding widgets to the layouts.
		self.chamberStatusEditorLayout.addWidget(self.chamberStatusLabel, alignment= Qt.AlignCenter)
		self.chamberStatusEditorLayout.addLayout(self.chambersTableLayout)


		self.chamberStatusMainWidget.setLayout(self.chamberStatusEditorLayout)
		self.setCentralWidget(self.chamberStatusMainWidget)
		self.showMaximized()


	def chamber_status_db1(self):
		print("You can edit Now")

	
	def chamber_status_db(self):
		
		conn = sqlite3.connect('Test_Chamber.db')
		cur = conn.cursor()
				
		#Creating SQLite3 Table for the Primary details:
		conn.execute('''CREATE TABLE IF NOT EXISTS Chamber_Status_Table
		('Chamber Name' TEXT,
		'Status' TEXT,  
		'Remarks' TEXT
		)''')


		for i in range(self.chamberStatusTable.rowCount()):

			if self.chamberStatusTable.item(i,0) != None:
				Chamber_Names = self.chamberStatusTable.item(i,0).text()
				print(Chamber_Names)
			else:
				Chamber_Names = ''


			if self.chamberStatusTable.item(i,1) != None:
				chamber_status = self.chamberStatusTable.item(i,1).text()
				print(chamber_status)
			else:
				chamber_status = ''



			if self.chamberStatusTable.item(i,2) != None:
				Remarks_Bar = self.chamberStatusTable.item(i,2).text()
				print(Remarks_Bar)
			else:
				Remarks_Bar = ''

		
		#Inserting the values to the table:
		conn.execute("INSERT INTO Chamber_Status_Table VALUES (?,?,?)",(Chamber_Names,chamber_status,Remarks_Bar))
		conn.commit()
		conn.close()

















if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Application()
	ex.show()
	sys.exit(app.exec_())
# Importing necessary libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
from PyQt5.uic import loadUi
from PyQt5.QtSql import *
import sys


#class MainWindow(QMainWindow):
#	def __init__(self):
#		super().__init__()

def ChambersDataTableUi(self):

	#Create main widgets and window: 
	#self.mainWidget = QWidget()

	self.allChambersDetailsLabel = QLabel("List of Chambers:")
	self.allChambersDetailsLabel.setStyleSheet('''font-weight: bold;
								font:Times;
								text-decoration: underline;
								color: #cf014b;							
								font-size: 22px;
								''')

	self.allChambersDetailsLayout = QVBoxLayout()
	self.ChambersSearchbarLayout = QHBoxLayout()

	#self.shadowEffectsofChambersTable = QGraphicsDropShadowEffect(self)
	#self.shadowEffectsofChambersTable.setBlurRadius(10)
	#self.shadowEffectsofChambersTable.setXOffset(0)
	#self.shadowEffectsofChambersTable.setYOffset(0)
	
	
	#Create searchbar:
	self.chambersSearchbar = QLineEdit()
	self.chambersSearchbar.setPlaceholderText('Search:')
	self.chambersSearchbar.setClearButtonEnabled(True)
	self.chambersSearchbar.setFixedWidth(350)
	self.chambersSearchbar.setFixedHeight(30)

	self.refreshBtnOfchambers = QPushButton('Refresh')
	self.refreshBtnOfchambers.setFixedWidth(150)
	#self.refreshBtnOfchambers.setGraphicsEffect(self.shadowEffectsofChambersTable)
	self.refreshBtnOfchambers.clicked.connect(self.refreshBtnOfchambersTable)


	self.ChambersSearchbarLayout.addWidget(self.allChambersDetailsLabel, alignment = Qt.AlignLeft)
	self.ChambersSearchbarLayout.addWidget(self.chambersSearchbar, alignment = Qt.AlignLeft)
	self.ChambersSearchbarLayout.addWidget(self.refreshBtnOfchambers, alignment = Qt.AlignRight)
	self.allChambersDetailsLayout.addLayout(self.ChambersSearchbarLayout)
	self.spacer4 = QSpacerItem(300, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
	self.allChambersDetailsLayout.addItem(self.spacer4)
	
	#Create connection with sqlite3 database:
	conn = sqlite3.connect('test.db')
	cursor = conn.cursor()
	
	#Fetch the required columns from the tables using JOIN function.
	chambersListTable =('SELECT * FROM BEA_Chambers_Data');
	resultsOfchambersListTable = conn.execute(chambersListTable).fetchall()
	#print(resultsOfchambersListTable)

	#Create a table with the required header labels:
	self.modelOfchambersListTable = QStandardItemModel(len(resultsOfchambersListTable),5)
	self.modelOfchambersListTable.setHorizontalHeaderLabels(['Chamber/Equipment','ID','Make/Id/Type','Chamber Capacity','Range'])
	
	tablerow = 0
	for row in resultsOfchambersListTable:
		for j in range(5):
			self.modelOfchambersListTable.setItem(tablerow, j, QStandardItem(str(row[j])))
		tablerow +=1

	#Create sort and filter functions:
	Chambers_filter_proxy_model = QSortFilterProxyModel()
	Chambers_filter_proxy_model.setSourceModel(self.modelOfchambersListTable)
	Chambers_filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
	Chambers_filter_proxy_model.setFilterKeyColumn(-1)
	self.chambersSearchbar.textChanged.connect(Chambers_filter_proxy_model.setFilterRegExp)
	
	#Create a tableview widget:
	self.chambersListTable = QTableView()
	self.chambersListTable.setFont(QFont('Times', 10))
	self.chambersListTable.setStyleSheet("QHeaderView {font: Times; font-size: 10pt; font-weight: bold; }")
	self.chambersListTable.setSortingEnabled(True)
	self.chambersListTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
	self.chambersListTable.setAlternatingRowColors(True)
	self.chambersListTable.setModel(Chambers_filter_proxy_model)
	self.allChambersDetailsLayout.addWidget(self.chambersListTable)
	self.chambersListTable.verticalHeader().setDefaultSectionSize(30)
	self.chambersListTable.horizontalHeader().setDefaultSectionSize(200)
	
		
		
	
	#self.mainWidget.setLayout(self.allChambersDetailsLayout)
	#self.setCentralWidget(self.mainWidget)
	
	
	main = QWidget()
	main.setLayout(self.allChambersDetailsLayout)
	return main

	
	
	
def refreshBtnOfchambersTable(self):
	self.chambersListTable.setParent(None)


	conn = sqlite3.connect('test.db')
	cursor = conn.cursor()
	
	#Fetch the required columns from the tables using JOIN function.
	chambersListTable =('SELECT * FROM BEA_Chambers_Data');
	resultsOfchambersListTable = conn.execute(chambersListTable).fetchall()
	#print(resultsOfchambersListTable)

	#Create a table with the required header labels:
	self.modelOfchambersListTable = QStandardItemModel(len(resultsOfchambersListTable),5)
	self.modelOfchambersListTable.setHorizontalHeaderLabels(['Chamber/Equipment','ID','Make/Id/Type','Chamber Capacity','Range'])
	
	tablerow = 0
	for row in resultsOfchambersListTable:
		for j in range(5):
			self.modelOfchambersListTable.setItem(tablerow, j, QStandardItem(str(row[j])))
		tablerow +=1

	#Create sort and filter functions:
	Chambers_filter_proxy_model = QSortFilterProxyModel()
	Chambers_filter_proxy_model.setSourceModel(self.modelOfchambersListTable)
	Chambers_filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
	Chambers_filter_proxy_model.setFilterKeyColumn(-1)
	self.chambersSearchbar.textChanged.connect(Chambers_filter_proxy_model.setFilterRegExp)
	
	#Create a tableview widget:
	self.chambersListTable = QTableView()
	self.chambersListTable.setFont(QFont('Times', 10))
	self.chambersListTable.setStyleSheet("QHeaderView {font: Times; font-size: 10pt; font-weight: bold; }")
	self.chambersListTable.setSortingEnabled(True)
	self.chambersListTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
	self.chambersListTable.setAlternatingRowColors(True)
	self.chambersListTable.setModel(Chambers_filter_proxy_model)
	self.allChambersDetailsLayout.addWidget(self.chambersListTable)
	self.chambersListTable.verticalHeader().setDefaultSectionSize(30)
	self.chambersListTable.horizontalHeader().setDefaultSectionSize(200)
	


#if __name__ == '__main__':	
#	app = QApplication(sys.argv)
#	window = MainWindow()
#	window.show()
#	app.exec_()
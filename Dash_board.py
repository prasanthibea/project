# Importing necessary libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
from PyQt5.uic import loadUi
from PyQt5.QtSql import *
import sys
from datetime import datetime


#class MainWindow(QMainWindow):
#	def __init__(self):
#		super().__init__()

def dashBoardUi(self):

	#Create main widgets and window: 
	self.mainWidget = QWidget()
	self.slotBookingDashboardLayout = QVBoxLayout()
	self.slotBookingSearchbarLayout = QHBoxLayout()

	self.shadowEffect1 = QGraphicsDropShadowEffect(self)
	self.shadowEffect1.setBlurRadius(10)
	self.shadowEffect1.setXOffset(0)
	self.shadowEffect1.setYOffset(0)
	
	
	#Create searchbar:
	self.slotsBookedSearchbar = QLineEdit()
	self.slotsBookedSearchbar.setPlaceholderText('Search:')
	self.slotsBookedSearchbar.setClearButtonEnabled(True)
	self.slotsBookedSearchbar.setFixedWidth(350)
	self.slotsBookedSearchbar.setFixedHeight(30)

	self.refreshButtonOfSlots = QPushButton('Refresh')
	self.refreshButtonOfSlots.setFixedWidth(150)
	#self.refreshButtonOfSlots.setGraphicsEffect(self.shadowEffect1)
	self.refreshButtonOfSlots.clicked.connect(self.refreshOfBookingsDashoard)


	self.slotBookingSearchbarLayout.addWidget(self.slotsBookedSearchbar, alignment = Qt.AlignLeft)
	self.slotBookingSearchbarLayout.addWidget(self.refreshButtonOfSlots, alignment = Qt.AlignRight)
	self.slotBookingDashboardLayout.addLayout(self.slotBookingSearchbarLayout)
	self.spacerBar = QSpacerItem(300, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
	self.slotBookingDashboardLayout.addItem(self.spacerBar)

	
	#Create connection with sqlite3 database:
	conn = sqlite3.connect('test.db')
	cursor = conn.cursor()
	
	#Fetch the required columns from the tables using JOIN function.
	BookedSlotsDataTable =(''' SELECT SLOTS11.'Company Name',SLOTS11.'Customer Email',SLOTS11.'BookingID',
				SLOTS11_AD.'Test Name',SLOTS11_AD.'Test Start Date',SLOTS11_AD.'Test Duration',SLOTS11_AD.'Test End Date',SLOTS11_AD.'Allotted Chambers',
				SLOTS11_AD.'Remarks' FROM SLOTS11 Natural JOIN SLOTS11_AD''');
	resultsOfJCBookedSlots = conn.execute(BookedSlotsDataTable).fetchall()
	#print(resultsOfJCBookedSlots)

	#Create a table with the required header labels:
	self.modelOfSlotsDashBoard = QStandardItemModel(len(resultsOfJCBookedSlots),9)
	self.modelOfSlotsDashBoard.setHorizontalHeaderLabels(['Company Name','Customer Email','Booking ID','Test Name','Test Start Date','Test Duration(Hours)',
		'Test End Date','Allotted Chambers','Remarks'])
	
	tablerow = 0
	for row in resultsOfJCBookedSlots:
		for j in range(9):
			self.modelOfSlotsDashBoard.setItem(tablerow, j, QStandardItem(str(row[j])))
		tablerow +=1

	#Create sort and filter functions:
	filter_proxy_model = QSortFilterProxyModel()
	filter_proxy_model.setSourceModel(self.modelOfSlotsDashBoard)
	filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
	filter_proxy_model.setFilterKeyColumn(-1)
	self.slotsBookedSearchbar.textChanged.connect(filter_proxy_model.setFilterRegExp)
	
	#Create a tableview widget:
	self.BookedSlotsDBTable = QTableView()
	self.BookedSlotsDBTable.setFont(QFont('Times', 10))
	self.BookedSlotsDBTable.setStyleSheet("QHeaderView {font: Times; font-size: 10pt; font-weight: bold; }")
	self.BookedSlotsDBTable.setSortingEnabled(True)
	self.BookedSlotsDBTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
	self.BookedSlotsDBTable.setAlternatingRowColors(True)
	self.BookedSlotsDBTable.setModel(filter_proxy_model)
	self.slotBookingDashboardLayout.addWidget(self.BookedSlotsDBTable)
	self.BookedSlotsDBTable.horizontalHeader().setDefaultSectionSize(150)

	
	

	#self.mainWidget.setLayout(self.slotBookingDashboardLayout)
	#self.setCentralWidget(self.mainWidget)


	main = QWidget()
	main.setLayout(self.slotBookingDashboardLayout)
	return main

def refreshOfBookingsDashoard(self):
	self.BookedSlotsDBTable.setParent(None)


	#Create connection with sqlite3 database:
	conn = sqlite3.connect('test.db')
	cursor = conn.cursor()
	
	#Fetch the required columns from the tables using JOIN function.
	BookedSlotsDataTable =(''' SELECT SLOTS11.'Company Name',SLOTS11.'Customer Email',SLOTS11.'BookingID',
				SLOTS11_AD.'Test Name',SLOTS11_AD.'Test Start Date',SLOTS11_AD.'Test Duration',SLOTS11_AD.'Test End Date',SLOTS11_AD.'Allotted Chambers',
				SLOTS11_AD.'Remarks' FROM SLOTS11 Natural JOIN SLOTS11_AD''');
	resultsOfJCBookedSlots = conn.execute(BookedSlotsDataTable).fetchall()
	#print(resultsOfJCBookedSlots)

	#Create a table with the required header labels:
	self.modelOfSlotsDashBoard = QStandardItemModel(len(resultsOfJCBookedSlots),9)
	self.modelOfSlotsDashBoard.setHorizontalHeaderLabels(['Company Name','Customer Email','Booking ID','Test Name','Test Start Date','Test Duration(Hours)',
		'Test End Date','Allotted Chambers','Remarks'])
	tablerow = 0
	for row in resultsOfJCBookedSlots:
		for j in range(9):
			self.modelOfSlotsDashBoard.setItem(tablerow, j, QStandardItem(str(row[j])))
		tablerow +=1

	#Create sort and filter functions:
	filter_proxy_model = QSortFilterProxyModel()
	filter_proxy_model.setSourceModel(self.modelOfSlotsDashBoard)
	filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
	filter_proxy_model.setFilterKeyColumn(-1)
	self.slotsBookedSearchbar.textChanged.connect(filter_proxy_model.setFilterRegExp)
	
	#Create a tableview widget:
	self.BookedSlotsDBTable = QTableView()
	self.BookedSlotsDBTable.setFont(QFont('Times', 10))
	self.BookedSlotsDBTable.setStyleSheet("QHeaderView {font: Times; font-size: 10pt; font-weight: bold; }")
	self.BookedSlotsDBTable.setSortingEnabled(True)
	self.BookedSlotsDBTable.setModel(filter_proxy_model)
	self.slotBookingDashboardLayout.addWidget(self.BookedSlotsDBTable)
	self.BookedSlotsDBTable.setAlternatingRowColors(True)
	self.BookedSlotsDBTable.horizontalHeader().setDefaultSectionSize(150)
	


#if __name__ == '__main__':
#	app = QApplication(sys.argv)
#	window = MainWindow()
#	window.show()
#	app.exec_()







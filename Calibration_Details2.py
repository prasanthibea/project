from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import sys
import os
import sqlite3


class Application(QMainWindow):
	def __init__(self):
		super().__init__()
		#loadUi("Calibration_Table.ui",self)
		#self.CalibrationTableUI()

	#def CalibrationTableUI(self):
		#Create main widgets and window:
	
		self.mainWidget = QWidget()
		self.Calibrationtablelabel = QLabel("Calibration List:")
		self.Calibrationtablelabel.setStyleSheet('''font-weight: bold;
									font:Times;
									text-decoration: underline;
									color: #cf014b;							
									font-size: 22px;
									''')
		
		self.CalibrationDetailsLayout = QVBoxLayout()
		self.calibrationListSearchBarLayout = QHBoxLayout()
			
	
		self.calibrationListShadow = QGraphicsDropShadowEffect(self)
		self.calibrationListShadow.setBlurRadius(10)
		self.calibrationListShadow.setXOffset(0)
		self.calibrationListShadow.setYOffset(0)
	
	
	
		#Create searchbar:
	
		self.calibrationtSearchBar = QLineEdit()
		self.calibrationtSearchBar.setPlaceholderText('Search:')
		self.calibrationtSearchBar.setClearButtonEnabled(True)
		self.calibrationtSearchBar.setFixedWidth(350)
		self.calibrationtSearchBar.setFixedHeight(30)
		
		self.refreshBtnOfCDT = QPushButton('Refresh')
		self.refreshBtnOfCDT.setFixedWidth(150)
		#self.refreshBtnOfCDT.setGraphicsEffect(self.calibrationListShadow)
		self.refreshBtnOfCDT.clicked.connect(self.refreshOfCDT)
	
		
		self.calibrationListSearchBarLayout.addWidget(self.Calibrationtablelabel,alignment= Qt.AlignLeft)					
		self.calibrationListSearchBarLayout.addWidget(self.calibrationtSearchBar,alignment= Qt.AlignLeft)
		self.calibrationListSearchBarLayout.addWidget(self.refreshBtnOfCDT,alignment= Qt.AlignRight)
		self.CalibrationDetailsLayout.addLayout(self.calibrationListSearchBarLayout)
		self.spacer5 = QSpacerItem(300, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.CalibrationDetailsLayout.addItem(self.spacer5)
		
		#Create connection with sqlite3 database:
		conn = sqlite3.connect('test.db')
		cursor = conn.cursor()
		
		#Fetch the required columns from the tables using JOIN function.
		calibrationtDataTable =(''' SELECT * FROM Calibration_Table''');
		resultsOfCDT = conn.execute(calibrationtDataTable).fetchall()
		#print(resultsOfCDT)
		
		#Create a table with the required header labels:
		self.modelOfCalibrationTable = QStandardItemModel(len(resultsOfCDT),5)
		self.modelOfCalibrationTable.setHorizontalHeaderLabels(['Name of the equipment','Model/Type/Make/SL No','Calibration done date','Calibration due date','Calibrated By'])
	
		tablerow = 0
		for row in resultsOfCDT:
			for j in range(5):
				self.modelOfCalibrationTable.setItem(tablerow, j, QStandardItem(str(row[j])))
			tablerow +=1
		
		#Create sort and filter functions:
		filter_proxy_model = QSortFilterProxyModel()
		filter_proxy_model.setSourceModel(self.modelOfCalibrationTable)
		filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
		filter_proxy_model.setFilterKeyColumn(-1)
		self.calibrationtSearchBar.textChanged.connect(filter_proxy_model.setFilterRegExp)
		
		#Create a tableview widget:
		self.CalibrationListTable = QTableView()
		self.CalibrationListTable.setSortingEnabled(True)
		self.CalibrationListTable.setStyleSheet("QHeaderView {font: Times; font-size: 10pt; font-weight: bold; }")
		self.CalibrationListTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.CalibrationListTable.setAlternatingRowColors(True)
		self.CalibrationListTable.setFont(QFont('Times', 10))
		self.CalibrationListTable.setModel(filter_proxy_model)
		self.CalibrationDetailsLayout.addWidget(self.CalibrationListTable)
		self.CalibrationListTable.verticalHeader().setDefaultSectionSize(30)
		self.CalibrationListTable.horizontalHeader().setDefaultSectionSize(200)
		
		
		#self.mainWidgetOfcalibrationTable = QWidget()
		#self.mainWidgetOfcalibrationTable.setLayout(self.CalibrationDetailsLayout)
		#return self.mainWidgetOfcalibrationTable

		self.mainWidget.setLayout(self.CalibrationDetailsLayout)
		self.setCentralWidget(self.mainWidget)


	def refreshOfCDT(self):
		self.CalibrationListTable.setParent(None)
	
		#Create connection with sqlite3 database:
		conn = sqlite3.connect('test.db')
		cursor = conn.cursor()
		
		#Fetch the required columns from the tables using JOIN function.
		calibrationtDataTable =(''' SELECT * FROM Calibration_Table''');
		resultsOfCDT = conn.execute(calibrationtDataTable).fetchall()
		#print(resultsOfCDT)
		
		#Create a table with the required header labels:
		self.modelOfCalibrationTable = QStandardItemModel(len(resultsOfCDT),5)
		self.modelOfCalibrationTable.setHorizontalHeaderLabels(['Name of the equipment','Model/Type/Make/SL No','Calibration done date','Calibration due date','Calibrated By'])
		
		tablerow = 0
		for row in resultsOfCDT:
			for j in range(5):
				self.modelOfCalibrationTable.setItem(tablerow, j, QStandardItem(str(row[j])))
			tablerow +=1
		
		#Create sort and filter functions:
		filter_proxy_model = QSortFilterProxyModel()
		filter_proxy_model.setSourceModel(self.modelOfCalibrationTable)
		filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
		filter_proxy_model.setFilterKeyColumn(-1)
		self.calibrationtSearchBar.textChanged.connect(filter_proxy_model.setFilterRegExp)
		
		#Create a tableview widget:
		self.CalibrationListTable = QTableView()
		self.CalibrationListTable.setSortingEnabled(True)
		self.CalibrationListTable.setStyleSheet("QHeaderView {font: Times; font-size: 10pt; font-weight: bold; }")
		self.CalibrationListTable.setModel(filter_proxy_model)
		self.CalibrationDetailsLayout.addWidget(self.CalibrationListTable)
		self.CalibrationListTable.setAlternatingRowColors(True)
		self.CalibrationListTable.setFont(QFont('Times', 10))
		self.CalibrationListTable.verticalHeader().setDefaultSectionSize(30)
		self.CalibrationListTable.horizontalHeader().setDefaultSectionSize(200)




if __name__ == '__main__':
	app = QApplication(sys.argv) 
	ex = Application()
	ex.show()
	sys.exit(app.exec_())
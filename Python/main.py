# LG4X: lmfit gui for xps curve fitting, Copyright (C) 2020, Hideki NAKAJIMA, Synchrotron Light Research Institute, Thailand

from PyQt5 import QtWidgets,QtCore
import sys, os
import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from lmfit.models import GaussianModel, LorentzianModel, VoigtModel, PseudoVoigtModel, ThermalDistributionModel, PolynomialModel, StepModel
from lmfit.models import ExponentialGaussianModel, SkewedGaussianModel, SkewedVoigtModel, DoniachModel, BreitWignerModel, LognormalModel
import xpspy as xpy

#style.use('ggplot')
style.use('seaborn-pastel')

class PrettyWidget(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		#super(PrettyWidget, self).__init__()
		self.initUI()

	def initUI(self):
		self.version = 'LG4X: lmfit gui for xps curve fitting ver. 0.05'
		self.floating = '.2f'
		self.setGeometry(600,300, 1100, 700)
		self.center()
		self.setWindowTitle(self.version)     
		self.statusBar().showMessage('Copyright (C) 2020, Hideki NAKAJIMA, Synchrotron Light Research Institute, Nakhon Ratchasima, Thailand')
		
		# Grid Layout
		grid = QtWidgets.QGridLayout()
		grid.setRowMinimumHeight(0, 25)
		grid.setRowMinimumHeight(1, 25)
		grid.setRowMinimumHeight(2, 25)
		widget = QtWidgets.QWidget(self)
		self.setCentralWidget(widget)
		widget.setLayout(grid)
		
		# Home directory
		self.filePath = QtCore.QDir.homePath()
		#self.filePath = '/Users/hidekinakajima/Desktop/W@home/Python/'
		
		# Figure: Canvas and Toolbar
		#self.figure = plt.figure(figsize=(6.7,5))
		self.figure, (self.ar, self.ax) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [1,5], 'hspace': 0})
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.toolbar.setMaximumHeight(20)
		self.toolbar.setMinimumHeight(15)
		self.toolbar.setStyleSheet("QToolBar { border: 0px }")
		grid.addWidget(self.canvas, 4,0,1,3)
		grid.addWidget(self.toolbar, 3,0,1,3)
		
		# data template
		#self.df = pd.DataFrame()
		self.df = []
		self.result = pd.DataFrame()

		# lists of dropdown menus
		self.list_imp = ['Importing data', 'Import csv', 'Import txt', 'Open directory']
		self.list_file = ['File list']
		self.list_bg = ['Shirley BG', 'Tougaard BG', 'Polynomial BG', 'Fermi-Dirac BG', 'Arctan BG', 'Erf BG']
		self.list_preset = ['Fitting preset', 'New', 'Load', 'Save', 'C1s', 'C K edge']

		# DropDown file import
		self.comboBox_imp = QtWidgets.QComboBox(self)
		self.comboBox_imp.addItems(self.list_imp)
		grid.addWidget(self.comboBox_imp, 0, 0, 1, 1)
		self.comboBox_imp.currentIndexChanged.connect(self.imp)
		self.comboBox_imp.setCurrentIndex(0)
		
		# DropDown file list
		self.comboBox_file = QtWidgets.QComboBox(self)
		self.comboBox_file.addItems(self.list_file)
		grid.addWidget(self.comboBox_file, 1, 0, 1, 2)
		self.comboBox_file.currentIndexChanged.connect(self.plot)
		
		# DropDown BG list
		self.comboBox_bg = QtWidgets.QComboBox(self)
		self.comboBox_bg.addItems(self.list_bg)
		grid.addWidget(self.comboBox_bg, 0, 1, 1, 1)
		self.comboBox_bg.setCurrentIndex(0)

		# DropDown preset list
		self.comboBox_pres = QtWidgets.QComboBox(self)
		self.comboBox_pres.addItems(self.list_preset)
		grid.addWidget(self.comboBox_pres, 2, 0, 1, 2)
		self.comboBox_pres.currentIndexChanged.connect(self.preset)
		self.comboBox_pres.setCurrentIndex(0)
		
		# Fit Button
		btn_fit = QtWidgets.QPushButton('Fit', self)
		btn_fit.resize(btn_fit.sizeHint())    
		btn_fit.clicked.connect(self.fit)
		grid.addWidget(btn_fit, 1, 2, 1, 1)
		
		# Add Button
		btn_add = QtWidgets.QPushButton('add peak', self)
		btn_add.resize(btn_add.sizeHint())   
		btn_add.clicked.connect(self.add_col)
		grid.addWidget(btn_add, 3, 3, 1, 2)
		
		# Remove Button
		btn_rem = QtWidgets.QPushButton('rem peak', self)
		btn_rem.resize(btn_rem.sizeHint())   
		btn_rem.clicked.connect(self.rem_col)
		grid.addWidget(btn_rem, 3, 5, 1, 2)
		
		# Export results Button
		btn_exp = QtWidgets.QPushButton('Export', self)
		btn_exp.resize(btn_exp.sizeHint())   
		btn_exp.clicked.connect(self.exportResults)
		grid.addWidget(btn_exp, 2, 2, 1, 1)
		
		# Evaluate Button
		btn_eva = QtWidgets.QPushButton('Evaluate', self)
		btn_eva.resize(btn_eva.sizeHint())   
		btn_eva.clicked.connect(self.eva)
		grid.addWidget(btn_eva, 0, 2, 1, 1)
		
		# PolyBG Table
		list_bg_col = ['bg_c0', 'bg_c1', 'bg_c2', 'bg_c3', 'bg_c4']
		list_bg_row = ['Range', 'Shirley', 'Tougaard', 'Polynomial', 'FD (amp, ctr, kt)', 'arctan (amp, ctr, sig)', 'erf (amp, ctr, sig)']
		self.fitp0 = QtWidgets.QTableWidget(len(list_bg_row),len(list_bg_col)*2)
		list_bg_colh = ['', 'bg_c0', '', 'bg_c1', '', 'bg_c2', '', 'bg_c3', '', 'bg_c4']
		self.fitp0.setHorizontalHeaderLabels(list_bg_colh)
		self.fitp0.setVerticalHeaderLabels(list_bg_row)
	
		# set BG table checkbox
		for row in range(len(list_bg_row)):
			for col in range(len(list_bg_col)):
				item = QtWidgets.QTableWidgetItem()
				item.setFlags(QtCore.Qt.ItemIsUserCheckable |	QtCore.Qt.ItemIsEnabled)
				item.setCheckState(QtCore.Qt.Unchecked)
				if (row == 0 and col < 2) or (row > 2 and col < 4):
					self.fitp0.setItem(row, col*2, item)

		# set BG table default
		pre_bg = [[0,300,0,270,'','','','','',''],['cv',1e-06,'it',10,'','','','','',''],['B',2866,'C',1643,'C*',1.0,'D',1.0,'',''],[2,0,2,0,2,0,2,0,'','']]
		self.setPreset(0, pre_bg, [])

		self.fitp0.resizeColumnsToContents()
		self.fitp0.resizeRowsToContents()	
		grid.addWidget(self.fitp0, 0, 3, 3, 4)
		
		# set Fit Table
		list_col = ['peak_1']
		list_row = ['model', 'center', 'sigma', 'gamma', 'amp', 'frac', 'skew', 'q', 'amp_ref', 'ratio', 'ctr_ref', 'ctr_diff', 'ctr_min', 'ctr_max', 'sig_min', 'sig_max', 'gam_min', 'gam_max', 'amp_min', 'amp_max', 'frac_min', 'frac_max', 'skew_min', 'skew_max', 'q_min', 'q_max']
		self.fitp1 = QtWidgets.QTableWidget(len(list_row),len(list_col)*2)
		list_colh = ['', 'peak_1']
		self.fitp1.setHorizontalHeaderLabels(list_colh)
		self.fitp1.setVerticalHeaderLabels(list_row)
		
		#self.list_shape = ['g', 'l', 'v', 'p']
		self.list_shape = ['g: Gaussian', 'l: Lorentzian', 'v: Voigt', 'p: PseudoVoigt', 'e: ExponentialGaussian', 's: SkewedGaussian', 'a: SkewedVoigt', 'b: BreitWigner', 'n: Lognormal', 'd: Doniach']
		self.list_peak = ['', '1']
		
		# set DropDown peak model
		for col in range(len(list_col)):
			comboBox = QtWidgets.QComboBox()
			comboBox.addItems(self.list_shape)
			#comboBox.setMaximumWidth(55)
			self.fitp1.setCellWidget(0, 2*col+1, comboBox)

		# set DropDown amp_ref peak section
		for col in range(len(list_col)):
			comboBox = QtWidgets.QComboBox()
			comboBox.addItems(self.list_peak)
			comboBox.setMaximumWidth(55)
			self.fitp1.setCellWidget(8, 2*col+1, comboBox)

		# set DropDown ctr_ref peak selection
		for col in range(len(list_col)):
			comboBox = QtWidgets.QComboBox()
			comboBox.addItems(self.list_peak)
			comboBox.setMaximumWidth(55)
			self.fitp1.setCellWidget(10, 2*col+1, comboBox)

		# set checkbox in fit table
		for row in range(len(list_row)-1):
			for col in range(len(list_col)):
				item = QtWidgets.QTableWidgetItem()
				item.setFlags(QtCore.Qt.ItemIsUserCheckable |	QtCore.Qt.ItemIsEnabled)
				if row < 7:
					item.setCheckState(QtCore.Qt.Checked)
					self.fitp1.setItem(row+1, col*2, item)
				if row > 10:
					item.setCheckState(QtCore.Qt.Unchecked)
					self.fitp1.setItem(row+1, col*2, item)
	
		# load default preset
		#pre_pk = [[0,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0],[2,0]]
		pre_pk = [[0,0],[2,284.6],[2,0.85],[2,0.85],[0,20000],[2,0.5],[2,0],[2,0]]
		self.setPreset(0, [], pre_pk)

		self.fitp1.resizeColumnsToContents()
		self.fitp1.resizeRowsToContents()
		grid.addWidget(self.fitp1, 4, 3, 1, 4)
		
		self.show()
		
	
	def add_col(self):
		rowPosition = self.fitp1.rowCount()
		colPosition = self.fitp1.columnCount()
		self.fitp1.insertColumn(colPosition)
		self.fitp1.insertColumn(colPosition+1)
		
		# add DropDown peak model
		comboBox = QtWidgets.QComboBox()
		comboBox.addItems(self.list_shape)
		#comboBox.setMaximumWidth(55)
		self.fitp1.setCellWidget(0, colPosition+1, comboBox)
		
		# setup new peak parameters
		for row in range(rowPosition):
			if row == 0:
				add_fac = float(self.fitp1.item(row+2, colPosition-1).text()) * 1
			if row == 3:
				add_fac = -1 * float(self.fitp1.item(row+1, colPosition-1).text())/2
			if row != 0 and row != 3:
				add_fac = 0
			if self.fitp1.item(row+1, colPosition-1) != None and row != 7 and row != 9:
				if len(self.fitp1.item(row+1, colPosition-1).text()) > 0:
					item = QtWidgets.QTableWidgetItem(str(format(float(self.fitp1.item(row+1, colPosition-1).text()) + add_fac, self.floating)))
					self.fitp1.setItem(row+1, colPosition+1, item)
		
		# add DropDown peak selection for amp_ref and ctr_ref and keep values as it is
		self.list_peak.append(str(int(1+colPosition/2)))
		
		for col in range(int(colPosition/2)+1):
			if col < int(colPosition/2):
				index = self.fitp1.cellWidget(8, 2*col+1).currentIndex()
			comboBox= QtWidgets.QComboBox()
			comboBox.addItems(self.list_peak)
			comboBox.setMaximumWidth(55)
			self.fitp1.setCellWidget(8, 2*col+1, comboBox)
			if index > 0 and col < int(colPosition/2):
				comboBox.setCurrentIndex(index)

		for col in range(int(colPosition/2)+1):
			if col < int(colPosition/2):
				index = self.fitp1.cellWidget(10, 2*col+1).currentIndex()
			comboBox = QtWidgets.QComboBox()
			comboBox.addItems(self.list_peak)
			comboBox.setMaximumWidth(55)
			self.fitp1.setCellWidget(10, 2*col+1, comboBox)
			if index > 0 and col < int(colPosition/2):
				comboBox.setCurrentIndex(index)

		# add checkbox
		for row in range(rowPosition-1):
			item = QtWidgets.QTableWidgetItem()
			item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
			if row < 7:
				#item.setCheckState(QtCore.Qt.Checked)
				if self.fitp1.item(row+1, colPosition-2).checkState() == 2:
					item.setCheckState(QtCore.Qt.Checked)
				else:
					item.setCheckState(QtCore.Qt.Unchecked)
				self.fitp1.setItem(row+1, colPosition, item)
			if row > 10:
				#item.setCheckState(QtCore.Qt.Unchecked)
				if self.fitp1.item(row+1, colPosition-2).checkState() == 2:
					item.setCheckState(QtCore.Qt.Checked)
				else:
					item.setCheckState(QtCore.Qt.Unchecked)
				self.fitp1.setItem(row+1, colPosition, item)

		# add table header
		item = QtWidgets.QTableWidgetItem()
		self.fitp1.setHorizontalHeaderItem(colPosition, item)
		item = QtWidgets.QTableWidgetItem('peak_' + str(int(1+colPosition/2)))
		self.fitp1.setHorizontalHeaderItem(colPosition+1, item)
		self.fitp1.resizeColumnsToContents()
		#self.fitp1.setColumnWidth(1, 55)


	def rem_col(self):
		colPosition = self.fitp1.columnCount()
		if colPosition > 2:
			self.fitp1.removeColumn(colPosition-1)
			self.fitp1.removeColumn(colPosition-2)
			self.list_peak.remove(str(int(colPosition/2)))
			# remove peak in dropdown menu and keep values as it is
			for col in range(int(colPosition/2)):
				if col < int(colPosition/2)-1:
					index = self.fitp1.cellWidget(8, 2*col+1).currentIndex()
				comboBox	= QtWidgets.QComboBox()
				comboBox.addItems(self.list_peak)
				self.fitp1.setCellWidget(8, 2*col+1, comboBox)
				if index > 0:
					comboBox.setCurrentIndex(index)
	
			for col in range(int(colPosition/2)):
				if col < int(colPosition/2)-1:
					index = self.fitp1.cellWidget(10, 2*col+1).currentIndex()
				comboBox	= QtWidgets.QComboBox()
				comboBox.addItems(self.list_peak)
				self.fitp1.setCellWidget(10, 2*col+1, comboBox)
				if index > 0:
					comboBox.setCurrentIndex(index)


	def preset(self):
		index = self.comboBox_pres.currentIndex()
		rowPosition = self.fitp1.rowCount()
		colPosition = self.fitp1.columnCount()
		
		if index == 1:
			if colPosition > 2:
				for col in range(int(colPosition/2)-1):
					self.rem_col()
			# load default preset
			if self.comboBox_file.currentIndex() > 0:
				#self.df = np.loadtxt(str(self.comboBox_file.currentText()),	delimiter=',', skiprows=1)
				x0 = self.df[:,0]
				y0 = self.df[:,1]
				pre_pk = [[0,0],[0,x0[abs(y0 - y0.max()).argmin()]],[0,abs(x0[0]-x0[-1])/23.5],[2,0],[0,y0[abs(y0 - y0.max()).argmin()]*2.5*abs(x0[0]-x0[-1])/23.5],[2,0]]
			else:
				pre_pk = [[0,0],[0,1],[0,1],[2,0],[0,1],[2,0]]
			self.setPreset(0, [], pre_pk)
		if index == 2:
			self.loadPreset()
			#print(self.df[0], self.df[1], self.df[2])
			if len(str(self.pre[0])) != 0 and len(self.pre[1]) != 0 and len(self.pre[2]) != 0:
				self.setPreset(self.pre[0], self.pre[1], self.pre[2])
		if index == 3:
			self.savePreset()
			self.savePresetDia()
		if index == 4:
			# load C1s peak preset
			pre_bg = [[2,295,2,275,'','','','','',''],['cv',1e-06,'it',10,'','','','','',''],['B',2866,'C',1643,'C*',1.0,'D',1.0,'',''],[2,0,2,0,2,0,2,0,'','']]
			if self.comboBox_file.currentIndex() > 0:
				#self.df = np.loadtxt(str(self.comboBox_file.currentText()),	delimiter=',', skiprows=1)
				x0 = self.df[:,0]
				y0 = self.df[:,1]
				pre_pk = [[0,0,0,0,0,0,0,0],[2,284.6,2,286.5,2,288.0,2,291.0],[2,0.85,2,0.85,2,1.28,2,1.28],[2,0.85,2,0.85,2,1.28,2,1.28],[0,y0[abs(y0 - y0.max()).argmin()]*2.5*0.85,0,y0[abs(y0 - y0.max()).argmin()]*2.5*0.85*0.1,0,y0[abs(y0 - y0.max()).argmin()]*2.5*0.85*0.05,0,y0[abs(y0 - y0.max()).argmin()]*2.5*0.85*0.05],[2,0.5,2,0.5,2,0.5,2,0.5]]
			else:
				pre_pk = [[0,0,0,0,0,0,0,0],[2,284.6,2,286.5,2,288.0,2,291.0],[2,0.85,2,0.85,2,1.28,2,1.28],[2,0.85,2,0.85,2,1.28,2,1.28],[0,20000,0,2000,0,750,0,750],[2,0.5,2,0.5,2,0.5,2,0.5]]
			self.setPreset(0, pre_bg, pre_pk)
		if index == 5:
			# load C K edge preset
			pre_bg = [[2, 270.7, 2, 320.7, '', '', '', '', '', ''], ['cv', 1e-06, 'it', 10.0, '', '', '', '', '', ''], ['B', 2866.0, 'C', 1643.0, 'C*', 1.0, 'D', 1.0, '', ''], [2, 0.07, 2, 0.0, 2, 0.0, 2, 0.0, '', ''], [2, 12.05, 2, 43.36, 2, 0.05, 0, '', '', ''], [2, 0.27, 2, 291.82, 2, 0.72, 0, '', '', ''], [0, '', 0, '', 0, '', 0, '', '', '']]

			pre_pk = [['', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0], [0, 284.95, 0, 286.67, 0, 287.57, 0, 289.0, 0, 290.69, 0, 292.27, 2, 296.0, 2, 302.0, 2, 310.0], [0, 0.67, 0, 0.5, 0, 0.8, 0, 0.8, 0, 1.0, 0, 1.5, 0, 3.0, 0, 5.0, 0, 5.0], [2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0], [0, 0.51, 0, 0.1, 0, 0.32, 0, 0.37, 0, 0.28, 0, 0.29, 0, 0.59, 0, 1.21, 0, 0.2], [2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0, 2, 0.0], [2, '', 2, '', 2, '', 2, '', 2, '', 2, '', 2, '', 2, '', 2, ''], [2, '', 2, '', 2, '', 2, '', 2, '', 2, '', 2, '', 2, '', 2, ''], ['', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], ['', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], [0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, ''], [0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, ''], [2, 0.5, 2, 0.5, 2, 0.5, 2, 0.5, 2, 0.5, 2, 1.0, 2, 2.0, 2, 2.0, 2, 2.0], [2, 0.8, 2, 0.8, 2, 0.8, 2, 0.8, 2, 1.0, 2, 1.5, 2, 3.0, 2, 5.0, 2, 5.0], [0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, ''], [0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, '', 0, ''], [2, 0.1, 2, 0.1, 2, 0.1, 2, 0.1, 2, 0.0, 2, 0.1, 2, 0.1, 2, 0.1, 2, 0.0]]
			self.setPreset(4, pre_bg, pre_pk)

		self.comboBox_pres.setCurrentIndex(0)
		self.fitp1.resizeColumnsToContents()
		self.fitp1.resizeRowsToContents()

		
	def setPreset(self, index_bg, list_pre_bg, list_pre_pk):
		if len(str(index_bg)) > 0:
			if int(index_bg) < len(self.list_bg):
				self.comboBox_bg.setCurrentIndex(int(index_bg))

		# load preset for bg
		if len(list_pre_bg) != 0:
			for  row in range(len(list_pre_bg)):
				for col in range(len(list_pre_bg[0])):
					if (col % 2) != 0:
						item = QtWidgets.QTableWidgetItem(str(list_pre_bg[row][col]))
					else:
						if (row == 0 and col < 4) or row > 2:
							item = QtWidgets.QTableWidgetItem()
							if list_pre_bg[row][col] == 2:
								item.setCheckState(QtCore.Qt.Checked)
							else:
								item.setCheckState(QtCore.Qt.Unchecked)
						else:
							item = QtWidgets.QTableWidgetItem(str(list_pre_bg[row][col]))
						
					self.fitp0.setItem(row, col, item)

		# load preset for peaks
		# adjust npeak before load
		if len(list_pre_pk) != 0:
			colPosition = int(self.fitp1.columnCount()/2)
			#print(int(colPosition), int(len(list_pre_pk[0])/2), list_pre_pk[0])
			if colPosition > int(len(list_pre_pk[0])/2):
				for col in range(colPosition - int(len(list_pre_pk[0])/2)):
					self.rem_col()
			if colPosition < int(len(list_pre_pk[0])/2):
				for col in range(int(len(list_pre_pk[0])/2) - colPosition):
					self.add_col()

		for  row in range(len(list_pre_pk)):
			for col in range(len(list_pre_pk[0])):
				if (col % 2) != 0:
					if row == 0 or row == 8 or row == 10:
						comboBox	= QtWidgets.QComboBox()
						if row == 0:
							comboBox.addItems(self.list_shape)
						else:
							comboBox.addItems(self.list_peak)
						self.fitp1.setCellWidget(row, col, comboBox)
						comboBox.setCurrentIndex(list_pre_pk[row][col])
					else:
						if str(list_pre_pk[row][col]) == '':
							item = QtWidgets.QTableWidgetItem('')
						else:
							item = QtWidgets.QTableWidgetItem(str(format(list_pre_pk[row][col], self.floating)))
						self.fitp1.setItem(row, col, item)
				else:
					if row != 0 and row != 8 and row != 9 and row != 10 and row != 11:
						item = QtWidgets.QTableWidgetItem()
						if list_pre_pk[row][col] == 2:
							item.setCheckState(QtCore.Qt.Checked)
						else:
							item.setCheckState(QtCore.Qt.Unchecked)
						
						self.fitp1.setItem(row, col, item)


	def loadPreset(self):
		cfilePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open data file', self.filePath, "DAT Files (*.dat)")
		if cfilePath != "":
			print (cfilePath)
			self.filePath = cfilePath
			with open(cfilePath, 'r') as file:
				self.pre = file.read()
			file.close
			#print(self.pre, type(self.pre))
			self.pre = ast.literal_eval(self.pre) 
			#self.pre = json.loads(self.pre) #json does not work due to the None issue
			#print(self.pre, type(self.pre))
			self.list_preset.append(str(cfilePath))
			self.comboBox_pres.clear()
			self.comboBox_pres.addItems(self.list_preset)
			self.comboBox_pres.setCurrentIndex(0)
		else:
			self.pre = [[],[],[]]

	def savePreset(self):
		rowPosition = self.fitp0.rowCount()
		colPosition = self.fitp0.columnCount()
		list_pre_bg = []
		# save preset for bg
		for  row in range(rowPosition):
			new = []
			for col in range(colPosition):
				if (col % 2) != 0:
					if self.fitp0.item(row, col) == None or len(self.fitp0.item(row, col).text()) == 0:
						new.append('')
					else:
						new.append(float(self.fitp0.item(row, col).text()))
				else:
					if (row == 0 and col < 4) or (row > 2 and col < 8):
						if self.fitp0.item(row, col).checkState() == 2:
							new.append(2)
						else:
							new.append(0)
					else:
						if self.fitp0.item(row, col) == None  or len(self.fitp0.item(row, col).text()) == 0:
							new.append('')
						else:
							new.append(self.fitp0.item(row, col).text())
			list_pre_bg.append(new)

		rowPosition = self.fitp1.rowCount()
		colPosition = self.fitp1.columnCount()
		list_pre_pk = []
		# save preset for peaks
		for  row in range(rowPosition):
			new = []
			for col in range(colPosition):
				if (col % 2) != 0:
					if row == 0 or row == 8 or row == 10:
						new.append(self.fitp1.cellWidget(row, col).currentIndex())
					else:
						if self.fitp1.item(row, col) == None  or len(self.fitp1.item(row, col).text()) == 0:
							new.append('')
						else:
							new.append(float(self.fitp1.item(row, col).text()))
				else:
					if row != 0 and row != 8 and row != 9 and row != 10 and row != 11:
						if self.fitp1.item(row, col).checkState() == 2:
							new.append(2)
						else:
							new.append(0)
					else:
						if self.fitp1.item(row, col) == None or len(self.fitp1.item(row, col).text()) == 0:
							new.append('')
						else:
							new.append(self.fitp1.item(row, col).text())
			list_pre_pk.append(new)
			
		#self.parText = self.version + 'parameters\n\n[[Data file]]\n\n' + self.comboBox_file.currentText() + '\n\n[[BG type]]\n\n' + str(self.comboBox_bg.currentIndex()) + '\n\n[[BG parameters]]\n\n' + str(list_pre_bg) + '\n\n[[Peak parameters]]\n\n' + str(list_pre_pk)
		#print(Text)
		self.parText = [self.comboBox_bg.currentIndex()]
		self.parText.append(list_pre_bg)
		self.parText.append(list_pre_pk)
		
		
	def savePresetDia(self):
		if self.comboBox_file.currentIndex() > 0:
			cfilePath = os.path.dirname(str(self.comboBox_file.currentText()))
			fileName = os.path.basename(str(self.comboBox_file.currentText()))
			fileName = os.path.splitext(fileName)[0]+'_pars'
		else:
			cfilePath = self.filePath
			fileName = 'sample_pars'

		# S_File will get the directory path and extension.
		cfilePath,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Preset file', cfilePath+os.sep+fileName+'.dat', "DAT Files (*.dat)")
		if cfilePath != "": 
			self.filePath = cfilePath
			# Finally this will Save your file to the path selected.
			with open(cfilePath, 'w') as file:
				file.write(str(self.parText))
			file.close


	def exportResults(self):
		if self.result.empty == False:
			if self.comboBox_file.currentIndex() > 0:
				#print(self.export_pars)
				#print(self.export_out.fit_report(min_correl=0.5))
			
				cfilePath = os.path.dirname(str(self.comboBox_file.currentText()))
				fileName = os.path.basename(str(self.comboBox_file.currentText()))
				fileName = os.path.splitext(fileName)[0]
			else:
				cfilePath = self.filePath
				fileName = 'sample'
	
			# S_File will get the directory path and extension.
			cfilePath,_  = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Fit file', cfilePath+os.sep+fileName+'_fit.txt', "Text Files (*.txt)")
			if cfilePath != "":
				self.filePath = cfilePath
				if self.comboBox_file.currentIndex() == 0:
					strmode = 'simulation mode'
				else:
					strmode = self.comboBox_file.currentText()
				Text = self.version + '\n\n[[Data file]]\n\n' + strmode + '\n\n[[Fit results]]\n\n'
				
				# fit results to be checked
				#for key in self.export_out.params:
					#Text += str(key) + "\t" + str(self.export_out.params[key].value) + '\n'
				indpk =0
				indpar = 0
				strpk =''
				strpar =''
				npeak = self.fitp1.columnCount()
				npeak = int(npeak/2)
				pk_name = np.array([None] * int(npeak), dtype = 'U')
				par_name = ['amplitude','center','sigma','gamma','fwhm','height','fraction','skew','q']
				par_list = np.array([[None]*9] * int(npeak), dtype='f')
				for key in self.export_out.params:
					if str(key)[1] == 'g':
						Text += str(key) + "\t" + str(self.export_out.params[key].value) + '\n'
					else:
						if len(strpk) > 0:
							if str(key)[:int(str(key).find('_'))] == strpk:
								strpar = str(key)[int(str(key).find('_'))+1:]
								for indpar in range(len(par_name)):
									if strpar == par_name[indpar]:
										par_list[indpk][indpar] = str(self.export_out.params[key].value)
										strpk = str(key)[:int(str(key).find('_'))]
							else:
								indpk += 1
								indpar = 0
								par_list[indpk][indpar] = str(self.export_out.params[key].value)
								strpk = str(key)[:int(str(key).find('_'))]
								pk_name[indpk] =  strpk
						else:
							par_list[indpk][indpar] = str(self.export_out.params[key].value)
							strpk = str(key)[:int(str(key).find('_'))]
							pk_name[indpk] =  strpk
							
				Text += '\n'
				for indpk in range(npeak):
					Text += '\t' + pk_name[indpk]
				for indpar in range(9):
					Text += '\n' + par_name[indpar] + '\t'
					for indpk in range(npeak):
						Text += str(par_list[indpk][indpar]) + '\t'
						
				self.savePreset()
				Text += '\n\n[[LG4X parameters]]\n\n' + str(self.parText) + '\n\n[[lmfit parameters]]\n\n' + str(self.export_pars)+ '\n\n' + str(self.export_out.fit_report(min_correl=0.25)) 

				with open(cfilePath, 'w') as file:
					file.write(str(Text))
				file.close
				#print(filePath)
				filePath1 = os.path.dirname(cfilePath)
				self.result.to_csv(filePath1+os.sep+fileName+'_fit.csv', index = False)
				#print(self.result)


	def imp(self):
		index = self.comboBox_imp.currentIndex()
		if index == 1 or index == 2:
			if index == 1:
				cfilePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open csv file', self.filePath, 'CSV Files (*.csv)')
			else:
				cfilePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open tab-separated text file', self.filePath, 'TXT Files (*.txt)')
			if cfilePath != "":
				#print (cfilePath)
				self.filePath = cfilePath
				self.list_file.append(str(cfilePath))
				self.comboBox_file.clear()
				self.comboBox_file.addItems(self.list_file)
				index = self.comboBox_file.findText(str(cfilePath), QtCore.Qt.MatchFixedString)
				if index >= 0:
					self.comboBox_file.setCurrentIndex(index)
				self.plot
		if index == 3:
			dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", self.filePath, QtWidgets.QFileDialog.ShowDirsOnly)
			if dir != "":
				entries = os.listdir(dir)
				entries.sort()
				for entry in entries:
					if os.path.splitext(entry)[1] == '.csv' or os.path.splitext(entry)[1] == '.txt':
						self.list_file.append(str(dir + os.sep + entry))
				self.comboBox_file.clear()
				self.comboBox_file.addItems(self.list_file)
		self.comboBox_imp.setCurrentIndex(0)


	def plot(self):
		if self.comboBox_file.currentIndex() > 0:
			#self.df = np.loadtxt(str(self.comboBox_file.currentText()), delimiter=',', skiprows=1)
			fileName = os.path.basename(self.comboBox_file.currentText())
			if os.path.splitext(fileName)[1] == '.csv':
				self.df = np.loadtxt(str(self.comboBox_file.currentText()), delimiter=',', skiprows=1)
				#self.df = pd.read_csv(str(self.comboBox_file.currentText()), dtype = float,  skiprows=1, header=None)
			else:
				self.df = np.loadtxt(str(self.comboBox_file.currentText()), delimiter='\t', skiprows=1)
				#self.df = pd.read_csv(str(self.comboBox_file.currentText()), dtype = float,  skiprows=1, header=None, delimiter = '\t')

			x0 = self.df[:,0]
			y0 = self.df[:,1]

			#plt.cla()
			self.ar.cla()
			self.ax.cla()
			#ax = self.figure.add_subplot(221)
			self.ax.plot(x0, y0, 'o', color="b", label="raw")
			if x0[0] > x0[-1]:
				#self.ax.invert_xaxis()
				self.ax.set_xlabel('Binding energy (eV)', fontsize=11)
			else:
				self.ax.set_xlabel('Energy (eV)', fontsize=11)

			plt.xlim(x0[0], x0[-1])
			self.ax.set_ylabel('Intensity (arb. unit)', fontsize=11)
			self.ax.grid(True)
			self.ar.set_title(self.comboBox_file.currentText(), fontsize=11)
			self.ax.legend(loc = 0)
			self.canvas.draw()
			
			item = QtWidgets.QTableWidgetItem(str(x0[0]))
			self.fitp0.setItem(0, 1, item)
			item = QtWidgets.QTableWidgetItem(str(x0[len(x0)-1]))
			self.fitp0.setItem(0, 3, item)
			#print(str(plt.get_fignums()))
		# select file list index ==0 to clear figure for simulation
		if self.comboBox_file.currentIndex() == 0 and self.comboBox_file.count() > 1:
			#plt.cla()
			self.ar.cla()
			self.ax.cla()
			self.canvas.draw()
		# macOS compatibility issue on pyqt5, add below to update window
		self.repaint()

	def eva(self):
		# simulation mode if no data in file list, otherwise evaluation mode
		if self.comboBox_file.currentIndex() == 0:
			if self.fitp0.item(0, 1) != None and self.fitp0.item(0, 3) != None:
				if len(self.fitp0.item(0, 1).text()) > 0 and len(self.fitp0.item(0, 3).text()) > 0:
					x1 = float(self.fitp0.item(0, 1).text()) 
					x2 = float(self.fitp0.item(0, 3).text())
					if self.fitp0.item(0, 5) != None:
						if len(self.fitp0.item(0, 5).text()) > 0:
							pnts = int(self.fitp0.item(0, 5).text())
						else:
							pnts = 101
					else:
						pnts = 101
					self.df = np.array([[0] * 2]*pnts, dtype='f')
					self.df[:, 0] = np.linspace(x1, x2, pnts)
					self.ana('eva')
		else:
			self.ana('eva')


	def fit(self):
		if self.comboBox_file.currentIndex() > 0:
			self.ana('fit')


	def ana(self, mode):
		#self.df = np.loadtxt(str(self.comboBox_file.currentText()), delimiter=',', skiprows=1)
		x0 = self.df[:,0]
		y0 = self.df[:,1]
		#print(x0[0], x0[len(x0)-1])
		
		# plot graph after selection data from popup
		#plt.clf()
		#plt.cla()
		self.ax.cla()
		self.ar.cla()
		#ax = self.figure.add_subplot(211)
		if mode == 'fit':
			self.ax.plot(x0, y0, 'o', color='b', label='raw')
		else:
			# simulation mode
			if self.comboBox_file.currentIndex() == 0:
				self.ax.plot(x0, y0, ',', color='b', label='raw')
			# evaluation mode
			else:
				self.ax.plot(x0, y0, 'o', mfc='none', color='b', label='raw')

		if x0[0] > x0[-1]:
			self.ax.set_xlabel('Binding energy (eV)', fontsize=11)
		else:
			self.ax.set_xlabel('Energy (eV)', fontsize=11)
		plt.xlim(x0[0], x0[-1])
		self.ax.grid(True)
		self.ax.set_ylabel('Intensity (arb. unit)', fontsize=11)
		self.ar.set_title(self.comboBox_file.currentText(), fontsize=11)
		
		# fit or simulation range
		if self.fitp0.item(0, 0).checkState() == 2:
			x1 = float(self.fitp0.item(0, 1).text()) 
		else:
			x1 = x0[0]
		if self.fitp0.item(0, 2).checkState() == 2:
			x2 = float(self.fitp0.item(0, 3).text())
		else:
			x2 = x0[len(x0)-1]

		[x, y] = xpy.fit_range(x0, y0, x1, x2)

		# BG model selection and call shirley and tougaard
		colPosition = self.fitp1.columnCount()
		index_bg = self.comboBox_bg.currentIndex()
		if index_bg == 0:
			shA = float(self.fitp0.item(index_bg+1, 1).text())
			shB = float(self.fitp0.item(index_bg+1, 3).text())
			bg_mod = xpy.shirley_calculate(x, y, shA, shB)
			y = y - bg_mod
		if index_bg == 1:
			toB = float(self.fitp0.item(index_bg+1, 1).text())
			toC = float(self.fitp0.item(index_bg+1, 3).text())
			toCd = float(self.fitp0.item(index_bg+1, 5).text())
			toD = float(self.fitp0.item(index_bg+1, 7).text())
			if mode == 'fit':
				toM = float(self.fitp0.item(1, 3).text())
			else:
				toM = 1
			[bg_mod, bg_toB] = xpy.tougaard_calculate(x, y, toB, toC, toCd, toD, toM)
			item = QtWidgets.QTableWidgetItem(str(format(bg_toB, self.floating)))
			self.fitp0.setItem(index_bg+1, 1, item)
			y = y - bg_mod
		if index_bg == 3:
			mod = ThermalDistributionModel(prefix='bg_', form='fermi')
			if self.fitp0.item(index_bg+1, 1) == None or self.fitp0.item(index_bg+1, 3) == None or self.fitp0.item(index_bg+1, 5) == None:
				pars = mod.guess(y, x=x)
			else:
				if len(self.fitp0.item(index_bg+1, 1).text()) == 0 or len(self.fitp0.item(index_bg+1, 3).text()) == 0 or len(self.fitp0.item(index_bg+1, 5).text()) == 0:
					pars = mod.guess(y, x=x)
				else:
					pars = mod.make_params()
					pars['bg_amplitude'].value = float(self.fitp0.item(index_bg+1, 1).text())
					pars['bg_center'].value = float(self.fitp0.item(index_bg+1, 3).text())
					pars['bg_kt'].value = float(self.fitp0.item(index_bg+1, 5).text())
			bg_mod = 0
		if index_bg == 4 or index_bg == 5:
			if index_bg == 4:
				mod = StepModel(prefix='bg_', form='arctan')
			if index_bg == 5:
				mod = StepModel(prefix='bg_', form='erf')
			if self.fitp0.item(index_bg+1, 1) == None or self.fitp0.item(index_bg+1, 3) == None or self.fitp0.item(index_bg+1, 5) == None:
				pars = mod.guess(y, x=x)
			else:
				if len(self.fitp0.item(index_bg+1, 1).text()) == 0 or len(self.fitp0.item(index_bg+1, 3).text()) == 0 or len(self.fitp0.item(index_bg+1, 5).text()) == 0:
					pars = mod.guess(y, x=x)
				else:
					pars = mod.make_params()
					pars['bg_amplitude'].value = float(self.fitp0.item(index_bg+1, 1).text())
					pars['bg_center'].value = float(self.fitp0.item(index_bg+1, 3).text())
					pars['bg_sigma'].value = float(self.fitp0.item(index_bg+1, 5).text())
			bg_mod = 0

		# Polynomial BG to be added for all BG
		if index_bg <= 2:
			mod = PolynomialModel(3, prefix='pg_')
			if self.fitp0.item(3, 1) == None or self.fitp0.item(3, 3) == None or self.fitp0.item(3, 5) == None or self.fitp0.item(3, 7) == None:
				pars = mod.make_params()
				for index in range(4):
					pars['pg_c'+str(index)].value = 0
				# make all poly bg parameters fixed
				for col in range(4):
					item = QtWidgets.QTableWidgetItem()
					item.setCheckState(QtCore.Qt.Checked)
					self.fitp0.setItem(3, 2*col, item)
			else:
				if len(self.fitp0.item(3, 1).text()) == 0 or len(self.fitp0.item(3, 3).text()) == 0 or len(self.fitp0.item(3, 5).text()) == 0 or len(self.fitp0.item(3, 7).text()) == 0:
					pars = mod.make_params()
					for index in range(4):
						pars['pg_c'+str(index)].value = 0
					# make all poly bg parameters fixed
					for col in range(4):
						item = QtWidgets.QTableWidgetItem()
						item.setCheckState(QtCore.Qt.Checked)
						self.fitp0.setItem(3, 2*col, item)
				else:
					pars = mod.make_params()
					for index in range(4):
						pars['pg_c'+str(index)].value = float(self.fitp0.item(3, 2*index+1).text())
			if index_bg == 2:
				bg_mod = 0
		else:
			modp = PolynomialModel(3, prefix='pg_')
			if self.fitp0.item(3, 1) == None or self.fitp0.item(3, 3) == None or self.fitp0.item(3, 5) == None or self.fitp0.item(3, 7) == None:
				pars.update(modp.make_params())
				for index in range(4):
					pars['pg_c'+str(index)].value = 0
				# make all poly bg parameters fixed
				for col in range(4):
					item = QtWidgets.QTableWidgetItem()
					item.setCheckState(QtCore.Qt.Checked)
					self.fitp0.setItem(3, 2*col, item)
			else:
				if len(self.fitp0.item(3, 1).text()) == 0 or len(self.fitp0.item(3, 3).text()) == 0 or len(self.fitp0.item(3, 5).text()) == 0 or len(self.fitp0.item(3, 7).text()) == 0:
					pars.update(modp.make_params())
					for index in range(4):
						pars['pg_c'+str(index)].value = 0
					# make all poly bg parameters fixed
					for col in range(4):
						item = QtWidgets.QTableWidgetItem()
						item.setCheckState(QtCore.Qt.Checked)
						self.fitp0.setItem(3, 2*col, item)
				else:
					pars.update(modp.make_params())
					for index in range(4):
						pars['pg_c'+str(index)].value = float(self.fitp0.item(3, 2*index+1).text())
			mod += modp

		# peak model selection and construction
		npeak = self.fitp1.columnCount()
		npeak = int(npeak/2)
		
		for index_pk in range(npeak):
			#print(self.fitp1.cellWidget(0, 2*index_pk+1).currentIndex())
			#print(self.fitp1.cellWidget(0, 2*index_pk+1).currentText())
			index = self.fitp1.cellWidget(0, 2*index_pk+1).currentIndex()
			strind = self.fitp1.cellWidget(0, 2*index_pk+1).currentText()
			strind = strind[0]
			if index == 0:
				pk_mod = GaussianModel(prefix=strind + str(index_pk+1) + '_')
			if index == 1:
				pk_mod = LorentzianModel(prefix=strind + str(index_pk+1) + '_')
			if index == 2:
				pk_mod = VoigtModel(prefix=strind + str(index_pk+1) + '_')
			if index == 3:
				pk_mod = PseudoVoigtModel(prefix=strind + str(index_pk+1) + '_')
			if index == 4:
				pk_mod = ExponentialGaussianModel(prefix=strind + str(index_pk+1) + '_')
			if index == 5:
				pk_mod = SkewedGaussianModel(prefix=strind + str(index_pk+1) + '_')
			if index == 6:
				pk_mod = SkewedVoigtModel(prefix=strind + str(index_pk+1) + '_')
			if index == 7:
				pk_mod = BreitWignerModel(prefix=strind + str(index_pk+1) + '_')
			if index == 8:
				pk_mod = LognormalModel(prefix=strind + str(index_pk+1) + '_')
			if index == 9:
				pk_mod = DoniachModel(prefix=strind + str(index_pk+1) + '_')

			pars.update(pk_mod.make_params())

			# fit parameters from table
			if self.fitp1.item(1, 2*index_pk+1) != None:
				if len(self.fitp1.item(1, 2*index_pk+1).text()) > 0:
					pars[strind + str(index_pk+1) + '_center'].value = float(self.fitp1.item(1, 2*index_pk+1).text())

			if self.fitp1.item(2, 2*index_pk+1) != None:
				if len(self.fitp1.item(2, 2*index_pk+1).text()) > 0:
					pars[strind + str(index_pk+1) + '_sigma'].value = float(self.fitp1.item(2, 2*index_pk+1).text())

			if index == 2 or index == 4 or index == 5 or index == 6 or index == 9:
				if self.fitp1.item(3, 2*index_pk+1) != None:
					if len(self.fitp1.item(3, 2*index_pk+1).text()) > 0:
						pars[strind + str(index_pk+1) +	'_gamma'].value = float(self.fitp1.item(3, 2*index_pk+1).text())

			if self.fitp1.item(4, 2*index_pk+1) != None:
				if len(self.fitp1.item(4, 2*index_pk+1).text()) > 0:
					pars[strind + str(index_pk+1) + '_amplitude'].value = float(self.fitp1.item(4, 2*index_pk+1).text())

			if index == 3:
				if self.fitp1.item(5, 2*index_pk+1) != None:
					if len(self.fitp1.item(5, 2*index_pk+1).text()) > 0:
						pars[strind + str(index_pk+1) +	'_fraction'].value = float(self.fitp1.item(5, 2*index_pk+1).text())
			if index == 6:
				if self.fitp1.item(6, 2*index_pk+1) != None:
					if len(self.fitp1.item(6, 2*index_pk+1).text()) > 0:
						pars[strind + str(index_pk+1) +	'_skew'].value = float(self.fitp1.item(6, 2*index_pk+1).text())
			if index == 7:
				if self.fitp1.item(7, 2*index_pk+1) != None:
					if len(self.fitp1.item(7, 2*index_pk+1).text()) > 0:
						pars[strind + str(index_pk+1) +	'_q'].value = float(self.fitp1.item(7, 2*index_pk+1).text())

			 # sum of models
			mod += pk_mod

		if mode == 'eva':
			# constraints of BG parameters (checkbox to hold)
			for index in range(4):
				pars['pg_c' + str(index)].vary = False
			if index_bg == 3:
				pars['bg_amplitude'].vary = False
				pars['bg_center'].vary = False
				pars['bg_kt'].vary = False
			if index_bg == 4 or index_bg == 5:
				pars['bg_amplitude'].vary = False
				pars['bg_center'].vary = False
				pars['bg_sigma'].vary = False
	
			# constraints of peak parameters (checkbox to hold)
			for index_pk in range(npeak):
				index = self.fitp1.cellWidget(0, 2*index_pk+1).currentIndex()
				strind = self.fitp1.cellWidget(0, 2*index_pk+1).currentText()
				strind = strind[0]
				pars[strind + str(index_pk+1) + '_center'].vary = False
				pars[strind + str(index_pk+1) + '_sigma'].vary = False
	
				if index == 2 or index == 4 or index == 5 or index == 6 or index == 9:
					pars[strind + str(index_pk+1) +	'_gamma'].vary = False
	
				pars[strind + str(index_pk+1) + '_amplitude'].vary = False
	
				if index == 3:
					pars[strind + str(index_pk+1) + '_fraction'].vary = False
				if index == 6:
					pars[strind + str(index_pk+1) + '_skew'].vary = False
				if index == 7:
					pars[strind + str(index_pk+1) + '_q'].vary = False
		else:
			# constraints of BG parameters (checkbox to hold)
			for index in range(4):
				if self.fitp0.item(3, 2*index).checkState() == 2:
					if len(self.fitp0.item(3, 2*index+1).text()) > 0:
						pars['pg_c' + str(index)].vary = False
			if index_bg == 3:
				if self.fitp0.item(index_bg+1, 0).checkState() == 2:
					if len(self.fitp0.item(index_bg+1, 1).text()) > 0:
						pars['bg_amplitude'].vary = False
				if self.fitp0.item(index_bg+1, 2).checkState() == 2:
					if len(self.fitp0.item(index_bg+1, 3).text()) > 0:
						pars['bg_center'].vary = False
				if self.fitp0.item(index_bg+1, 4).checkState() == 2:
					if len(self.fitp0.item(index_bg+1, 5).text()) > 0:
						pars['bg_kt'].vary = False
			if index_bg == 4 or index_bg == 5:
				if self.fitp0.item(index_bg+1, 0).checkState() == 2:
					if len(self.fitp0.item(index_bg+1, 1).text()) > 0:
						pars['bg_amplitude'].vary = False
				if self.fitp0.item(index_bg+1, 2).checkState() == 2:
					if len(self.fitp0.item(index_bg+1, 3).text()) > 0:
						pars['bg_center'].vary = False
				if self.fitp0.item(index_bg+1, 4).checkState() == 2:
					if len(self.fitp0.item(index_bg+1, 5).text()) > 0:
						pars['bg_sigma'].vary = False

			#Constraints of peak parameters
			for index_pk in range(npeak):
				# fixed peak parameters (checkbox to hold)
				index = self.fitp1.cellWidget(0, 2*index_pk+1).currentIndex()
				strind = self.fitp1.cellWidget(0, 2*index_pk+1).currentText()
				strind = strind[0]
				
				if self.fitp1.item(1, 2*index_pk).checkState() == 2:
					if len(self.fitp1.item(1, 2*index_pk+1).text()) > 0:
						pars[strind + str(index_pk+1) + '_center'].vary = False
	
				if self.fitp1.item(2, 2*index_pk).checkState() == 2:
					if len(self.fitp1.item(2, 2*index_pk+1).text()) > 0:
						pars[strind + str(index_pk+1) + '_sigma'].vary = False
	
				if index == 2 or index == 4 or index == 5 or index == 6 or index == 9:
					if self.fitp1.item(3, 2*index_pk).checkState() == 2:
						if len(self.fitp1.item(3, 2*index_pk+1).text()) > 0:
							pars[strind + str(index_pk+1) +	'_gamma'].vary = False
	
				if self.fitp1.item(4, 2*index_pk).checkState() == 2:
					if len(self.fitp1.item(4, 2*index_pk+1).text()) > 0:
						pars[strind + str(index_pk+1) + '_amplitude'].vary = False
	
				if index == 3:
					if self.fitp1.item(5, 2*index_pk).checkState() == 2:
						if len(self.fitp1.item(5, 2*index_pk+1).text()) > 0:
							pars[strind + str(index_pk+1) + '_fraction'].vary = False
				if index == 6:
					if self.fitp1.item(6, 2*index_pk).checkState() == 2:
						if len(self.fitp1.item(6, 2*index_pk+1).text()) > 0:
							pars[strind + str(index_pk+1) + '_skew'].vary = False
				if index == 7:
					if self.fitp1.item(7, 2*index_pk).checkState() == 2:
						if len(self.fitp1.item(7, 2*index_pk+1).text()) > 0:
							pars[strind + str(index_pk+1) + '_q'].vary = False

				# additional peak min and max bounds (checkbox to activate)
				#list_para = ['center', 'sigma', 'gamma', 'amplitude', 'fraction', 'skew', 'q']
				if index == 0 or index == 1 or index == 8:
					list_para = ['center', 'sigma', '', 'amplitude', '', '', '']
				if index == 2 or index == 4 or index == 5 or index == 9:
					list_para = ['center', 'sigma', 'gamma', 'amplitude', '', '', '']
				if index == 3:
					list_para = ['center', 'sigma', '', 'amplitude', 'fraction', '', '']
				if index == 6:
					list_para = ['center', 'sigma', 'gamma', 'amplitude', '', 'skew', '']
				if index == 7:
					list_para = ['center', 'sigma', '', 'amplitude', '', '', 'q']
				
				for para in range(len(list_para)):
					if len(list_para[para]) != 0 and self.fitp1.item(12 + 2*para, 2*index_pk).checkState() == 2 and self.fitp1.item(12 + 2*para, 2*index_pk+1) != None:
						if len(self.fitp1.item(12 + 2*para, 2*index_pk+1).text()) > 0:
							pars[strind + str(index_pk+1) + '_' + list_para[para]].min = float(self.fitp1.item(12 + 2*para, 2*index_pk+1).text())
					if len(list_para[para]) != 0 and self.fitp1.item(12 + 2*para + 1, 2*index_pk).checkState() == 2 and self.fitp1.item(12 + 2*para+1, 2*index_pk+1) != None:
						if len(self.fitp1.item(12 + 2*para + 1, 2*index_pk+1).text()) > 0:
							pars[strind + str(index_pk+1) + '_' + list_para[para]].max = float(self.fitp1.item(12 + 2*para + 1, 2*index_pk+1).text())
	
				# amp ratio setup
				if self.fitp1.cellWidget(8, 2*index_pk+1).currentIndex() > 0:
					pktar = self.fitp1.cellWidget(8, 2*index_pk+1).currentIndex()
					strtar = self.fitp1.cellWidget(0, 2*pktar-1).currentText()
					strtar = strtar[0]
					if self.fitp1.item(9, 2*index_pk+1) != None:
						if len(self.fitp1.item(9, 2*index_pk+1).text()) > 0:
							rtotar = float(self.fitp1.item(9, 2*index_pk+1).text())
							pars[strind + str(index_pk+1) + '_amplitude'].expr = strtar + str(pktar) + '_amplitude * ' + str(rtotar)
	
				# BE diff setup
				if self.fitp1.cellWidget(10, 2*index_pk+1).currentIndex() > 0:
					pktar = self.fitp1.cellWidget(10, 2*index_pk+1).currentIndex()
					strtar = self.fitp1.cellWidget(0, 2*pktar-1).currentText()
					strtar = strtar[0]
					if self.fitp1.item(11, 2*index_pk+1) != None:
						if len(self.fitp1.item(11, 2*index_pk+1).text()) > 0:
							diftar = float(self.fitp1.item(11, 2*index_pk+1).text())
							pars[strind + str(index_pk+1) + '_center'].expr = strtar + str(pktar) + '_center + ' + str(diftar)

		# evaluate model and optimize parameters for fitting in lmfit
		init = mod.eval(pars, x=x)
		out = mod.fit(y, pars, x=x)
		comps = out.eval_components(x=x)

		# fit results to be checked
		for key in out.params:
			print(key, "=", out.params[key].value)
		
		# fit results print
		if mode == 'eva':
			strmode = 'Evalution'
		else:
			strmode = 'Fitting'
		results = strmode + ' done: ' + out.method + ', # data: ' + str(out.ndata) + ', # func evals: ' + str(out.nfev) + ', # varys: ' + str(out.nvarys) + ', r chi-sqr: ' + str(format(out.redchi, self.floating)) + ', Akaike info crit: ' + str(format(out.aic, self.floating))
		self.statusBar().showMessage(results)

		# BG results into table
		for index in range(4):
			item = QtWidgets.QTableWidgetItem(str(format(out.params['pg_c' + str(index)].value, self.floating)))
			self.fitp0.setItem(3, 2*index+1, item)
		if index_bg == 3:
			item = QtWidgets.QTableWidgetItem(str(format(out.params['bg_amplitude'].value, self.floating)))
			self.fitp0.setItem(index_bg+1, 1, item)
			item = QtWidgets.QTableWidgetItem(str(format(out.params['bg_center'].value, self.floating)))
			self.fitp0.setItem(index_bg+1, 3, item)
			item = QtWidgets.QTableWidgetItem(str(format(out.params['bg_kt'].value, self.floating)))
			self.fitp0.setItem(index_bg+1, 5, item)
		if index_bg == 4 or index_bg == 5:
			item = QtWidgets.QTableWidgetItem(str(format(out.params['bg_amplitude'].value, self.floating)))
			self.fitp0.setItem(index_bg+1, 1, item)
			item = QtWidgets.QTableWidgetItem(str(format(out.params['bg_center'].value, self.floating)))
			self.fitp0.setItem(index_bg+1, 3, item)
			item = QtWidgets.QTableWidgetItem(str(format(out.params['bg_sigma'].value, self.floating)))
			self.fitp0.setItem(index_bg+1, 5, item)

		# Peak results into table
		for index_pk in range(npeak):
			index = self.fitp1.cellWidget(0, 2*index_pk+1).currentIndex()
			strind = self.fitp1.cellWidget(0, 2*index_pk+1).currentText()
			strind = strind[0]

			item = QtWidgets.QTableWidgetItem(str(format(out.params[strind + str(index_pk+1) + '_center'].value, self.floating)))
			self.fitp1.setItem(1, 2*index_pk+1, item)
			item = QtWidgets.QTableWidgetItem(str(format(out.params[strind + str(index_pk+1) + '_sigma'].value, self.floating)))
			self.fitp1.setItem(2, 2*index_pk+1, item)

			if index == 2 or index == 4 or index == 5 or index == 6 or index == 9:
				item = QtWidgets.QTableWidgetItem(str(format(out.params[strind + str(index_pk+1) + '_gamma'].value, self.floating)))
				self.fitp1.setItem(3, 2*index_pk+1, item)

			item = QtWidgets.QTableWidgetItem(str(format(out.params[strind + str(index_pk+1) + '_amplitude'].value, self.floating)))
			self.fitp1.setItem(4, 2*index_pk+1, item)

			if index == 3:
				item = QtWidgets.QTableWidgetItem(str(format(out.params[strind + str(index_pk+1) + '_fraction'].value, self.floating)))
				self.fitp1.setItem(5, 2*index_pk+1, item)
			if index == 6:
				item = QtWidgets.QTableWidgetItem(str(format(out.params[strind + str(index_pk+1) + '_skew'].value, self.floating)))
				self.fitp1.setItem(6, 2*index_pk+1, item)
			if index == 7:
				item = QtWidgets.QTableWidgetItem(str(format(out.params[strind + str(index_pk+1) + '_q'].value, self.floating)))
				self.fitp1.setItem(7, 2*index_pk+1, item)

		if mode == 'eva':
			#ax.plot(x, init+bg_mod, 'b--', lw =2, label='initial')
			self.ax.plot(x, out.best_fit+bg_mod, 'k-', lw=2, label='initial')
			
			for index_pk in range(npeak):
				#print(index_pk, color)
				strind = self.fitp1.cellWidget(0, 2*index_pk+1).currentText()
				strind = strind[0]
				if index_bg < 2:
					self.ax.plot(x, comps[strind + str(index_pk+1) + '_']+bg_mod+comps['pg_'], label='peak_' + str(index_pk+1))
				if index_bg == 2:
					self.ax.plot(x, comps[strind + str(index_pk+1) + '_']+comps['pg_'], label='peak_' + str(index_pk+1))
				if index_bg > 2:
					self.ax.plot(x, comps[strind + str(index_pk+1) + '_']+comps['bg_']+comps['pg_'], label='peak_' + str(index_pk+1))
		else:
			#ax.plot(x, init+bg_mod, 'k:', label='initial')
			self.ax.plot(x, out.best_fit+bg_mod, 'r-', lw=2, label='fit')

			for index_pk in range(npeak):
				strind = self.fitp1.cellWidget(0, 2*index_pk+1).currentText()
				strind = strind[0]
				if index_bg < 2:
					self.ax.fill_between(x, comps[strind + str(index_pk+1) + '_']+bg_mod+comps['pg_'], bg_mod+comps['pg_'], label='peak_' + str(index_pk+1))
				if index_bg == 2:
					self.ax.fill_between(x, comps[strind + str(index_pk+1) + '_']+comps['pg_'], comps['pg_'], label='peak_' + str(index_pk+1))
				if index_bg > 2:
					self.ax.fill_between(x, comps[strind + str(index_pk+1) + '_']+comps['bg_']+comps['pg_'], comps['bg_']+comps['pg_'], label='peak_' + str(index_pk+1))

			self.ar.plot(x, out.residual, 'g.', label='residual')

		self.ax.legend(loc = 0)
		self.ar.legend(loc = 0)
		self.canvas.draw()
		
		# make fit results to be global to export
		self.export_pars = pars
		self.export_out = out
		# make dataFrame and concat to export
		df_x = pd.DataFrame(x, columns = ['x'])
		df_y = pd.DataFrame(init, columns = ['y'])
		df_f = pd.DataFrame(out.best_fit, columns = ['fit'])
		if index_bg < 2:
			df_b = pd.DataFrame(bg_mod + comps['pg_'], columns = ['bg'])
		if index_bg == 2:
			df_b = pd.DataFrame(comps['pg_'], columns = ['bg'])
		if index_bg > 2:
			df_b = pd.DataFrame(comps['bg_'] + comps['pg_'], columns = ['bg'])
		self.result = pd.concat([df_x, df_y, df_f, df_b], axis=1)
		for index_pk in range(npeak):
			strind = self.fitp1.cellWidget(0, 2*index_pk+1).currentText()
			strind = strind[0]
			df_c = pd.DataFrame(comps[strind + str(index_pk+1) + '_'], columns = [strind + str(index_pk+1)])
			self.result = pd.concat([self.result, df_c], axis =1)

		# macOS compatibility issue on pyqt5, add below to update window
		self.repaint()

	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())


def main():
	app = QtWidgets.QApplication(sys.argv)
	w = PrettyWidget()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

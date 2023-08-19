from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import PyPDF2
from PyPDF2 import PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import *
import os
from pathlib import Path
import re
import sys
from datetime import datetime
# Accessed Libraries: 
    # PyQt5.QtWidgets import QWidget for Main and secondary window addons
    # PyQt5 import QtCore, QtGui, QtWidgets for Main and secondary windows
    # PyPDF2 for PDF manipulation
    # PyPDF2 import PdfWriter for creating new pdf files
    # tkinter as tk for overall usage of the tkinter GUI library.
    # tkinter import filedialog, messagebox, ttk for file selection, pop- up windows, and progress bar. 
    # tkinter import * for extra dependencies needed for tkinter.
    # os for path manipulation and directory change
    # pathlib import Path for in-depth path manipulation
    # re for searching of counties
    # sys for running of Pyqt5 windows

# Psuedo Code -
    # 1. Display a main menu with select file and add county buttons
    # 2. When user presses "select file", calls "cleanup Process" function:
        # - User will be prompted to select a folder   
        # - Program will read through all pdf files in that folder
        # - read first page and look for a matching county from page within the dictionary (text file)
            # if text file not found, display error
        # - If match is found, remove pages using corresponding PageNumber assigned from County in dictionary
            # - Create new pdf files starting at page (PageNumber) and dumped into newly created output_folder
        # - Prompt user when process is complete
    # 3. When user presses "Add county", calls "openAddCountyWindow" function:
        # - program looks for "county_list.txt"
            # if text file is found
                # - Prompt user to enter county name and page number to start at
                # - stores values in newKey and newValue
                # - capitalizes newKey then writes newKey and newValue to text document as "newAddition" in "KEY 1" format.
                # - Displays pop-up success message stating "newAddition added to textFile"
            # elif text file not found
                # - Display "file not found" error to user
                    # - Closes "Add county window" and returns to main menu


# -------Add County Window------
class secondary_window(QWidget):
    
    #function to start secondary window
    def setupUi(self, Form):

        # window object initialization
        self.Form = Form
        
        # Sets window alternate text and size
        Form.setObjectName("Form")
        Form.resize(359, 243)
        
        # Size and style of "add county" button
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(130, 190, 101, 41))
        self.pushButton.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        
        # Close and add county/num to list command for "Finish" button 
        self.pushButton.clicked.connect(self.addCounty)
        
        # Initializes window variable content; size, object name
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(40, 60, 283, 73))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        # Initializes text for "Enter page number: " label
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        
        #Initializes user input entry box for "Enter page number:"
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)
        
        #Stores user input as page number variable for future use
        countyName = self.lineEdit_2.text()    
      
        #Initializes user input entry box for "Enter num:"
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        
        # Initializes text for "Enter county name: " label
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        # calls translation function to allow for use of gui
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
     
    # function to add county to county_list.txt
    def addCounty(self):
        
        # Input of County name and page number
        self.newKey = self.lineEdit_2.text()
        self.newValue = self.lineEdit.text()
        
        # initializes county list file, and boolean for file existence
        countyListFile = 'county_list.txt'
        fileTrue = os.path.isfile(countyListFile)
        
        # Capitalizes county name input and renames page number variable
        newKey = self.newKey.upper()
        newValue = self.newValue
        
        # Combines county name and page number into one string with proper formatting
        newAddition = f"{newKey} {newValue}"
        
        # checks if there is the county_list.txt file in current directory 
        #  and user input a county and page number to write to file
        if fileTrue == True and newAddition != " ":
            
            # opens county_list.txt if exists
            with open(countyListFile, 'a') as f:
                    
                    # Writes county name and page number to text file
                    f.write("\n")
                    f.write(newAddition)
                    
            # process success pop-up after finish button pressed
            messagebox.showinfo("PA County Cleanup", f"{newAddition} added to county list... good bye!")
        
        # if user does not enter county name or page number, window closes   
        elif newAddition == " ":
            messagebox.showinfo("PA County Cleanup", f"No county or number entered... good bye!")
            pass        
        
        # error pop up if text file not found
        else:
            messagebox.showinfo("PA County Cleanup", f"Error, could not find {countyListFile}\n please check for name correctness")
        
        # "add county" window close
        self.Form.close()
        
    # translation function to allow for use of gui
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PA County Cleanup"))
        self.pushButton.setText(_translate("Form", "Finish"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"> Enter page number:</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\">Enter county name:</span></p></body></html>"))


#--------Main Window--------
class Ui_MainWindow(object):
    
    # function to begin class
    def __init__(self, MainWindow):
        
        # block of code to initialize main window and all its design data
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(402, 220)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 140, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(74, 91, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 21, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(14, 28, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 149, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 140, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(74, 91, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 21, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(14, 28, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(138, 149, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 21, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 140, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(74, 91, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 21, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(14, 28, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 21, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 21, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 130, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(21, 43, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("\n"
"background-color: rgb(46, 130, 255);")
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        
        # Initialization of "Select file" button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        
        # Begin file clean up process command for "Select file" button
        self.pushButton_2.clicked.connect(self.cleanupProcess)
        
        # Initialization of "Add county" button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        
        #Add county function need to be added
        self.pushButton.clicked.connect(self.openAddCountyWindow)
        
        # Initialization of main window title bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 402, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # calls translation function to allow for use of gui
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    # function to start progress bar window
    def progressBar(self):
        
        # progress bar window initialization
        global root, my_progress
        root = tk.Tk()

        # size, title, and placement of window
        root.geometry("350x100")
        root.title("Cleaning up...")
        root.eval('tk::PlaceWindow . center')

        # progress bar initialization
        my_progress = ttk.Progressbar(root, orient=HORIZONTAL, length=215, mode="determinate") 
       
        # Sets progress bar value
        my_progress["value"] 
        my_progress.update()
        
    # function for PA county clean up
    def cleanupProcess(self):
        
        # # initializes county list file, and boolean for file existence
        countyList = {}
        countyListFile = 'county_list.txt'
        fileTrue = os.path.isfile(countyListFile)
        
        # checks if there is the county_list.txt file in current directory 
        #  and user input a county and page number to read from file
        if fileTrue == True:
               
               # opens county_list.txt if exists
                with open(countyListFile) as f:
                    
                    # Reads county name and page number from text file line by line
                    for line in f:
                        if line.strip():
                            
                            #converts line to dictionary format
                            (key, val) = line.split()
                            countyList[str(key)] = int(val)
                          
                                 
        # Messagebox pop up if no files selected            
        else:
            messagebox.showinfo("PA County Cleanup", f"Error, could not find {countyListFile}\n please check for name correctness")
            return
        myKeys = list(countyList.keys())
        myKeys.sort()
        sortedDict = {i: countyList[i] for i in myKeys}  
        
        # Gets current working directory
        rawCwd = os.getcwd()
        cwd = fr"{rawCwd}"
          
        # Pop up for user to pick folder
        pdfDirectory = filedialog.askdirectory(title="Select a folder", initialdir=cwd)
        
        # If folder selected, continue with process
        if pdfDirectory:
            pass
        
        # If folder not selected, return to menu
        else:
            messagebox.showinfo("PA Cleanup", f"No file selected, good bye!")
            return
        
        # Changes working directory to selected folder and iterates through all PDF files in folder
        os.chdir(pdfDirectory)
        files = ([f for f in os.listdir(pdfDirectory) if f.endswith(".pdf") or f.endswith(".PDF")])
     
        # Initialize output folder
        global output_folder, output_folder_name
        output_folder_name = "output_folder"
        output_folder = Path(pdfDirectory) / output_folder_name
        output_folder.mkdir(parents=True, exist_ok=True)
        
        
        now = datetime.now()
        time = now.time()
        date = now.date()
        temp = sys.stdout
        outputLog = sys.stdout = f = open(f"{output_folder}\\output_log_({date}).txt", 'w')
    
        print("Date: ", date)
        print("Time: ", time)  
        # Initialize Writer object
        pdf_writer = PdfWriter()
        
        # Counter for progress bar incrementation
        fileCount = 0
        for input_path in files:
            fileCount += 1
        newCount = 100 / fileCount
        
        # Calls progress bar function and pops-up window
        self.progressBar()
        my_progress.pack(pady=20)
        
        # Initializes "Current File" text and updates progress bar window
        progressLabel = Label(root)
        progressLabel.pack()
        root.update()
        
        # Counter for current file iteration
        labelCount = 0
        
        # For loop to iterate through each file found as pdf
        for input_path in files:

            #Increment of current file
            labelCount += 1
            
            # Output folder file placement
            output_file_name = f"{Path(input_path).stem}.pdf"
            output_path = output_folder / output_file_name

            # Opens current operating file
            with open(input_path, 'rb') as input_file:
                
                # Initializes Reader object(currentFile) and writer object
                pdf_reader = PyPDF2.PdfReader(input_file)
                pdf_writer = PyPDF2.PdfWriter() 

                # Begins reading first page
                if pdf_reader.pages[0]:
                    
                    # Extract text from page
                    page_content = pdf_reader.pages[0].extract_text()
            
                    # Counter for what doesn't match
                    noneCounter = 0
                    
                    # for loop that iterates through each county in dictionary and searches for a match 
                    for county, pgNum in sortedDict.items():
                        
                        # match find variable
                        match = re.search(county, page_content)
                  
                        # if there is no match, add one to none counter
                        if match == None:
                            noneCounter += 1
                   
                            # If loop iterates through whole dictionary and no match is found, error pop up displayed
                            if noneCounter == len(sortedDict):
                                # messagebox.showinfo("PA Cleanup", f"No matched counties found in {input_path}, good bye!")
                                print(f"No matched counties found in: {input_path}")
                                
            
                        # If match is found, use number assigned to county to start newly
                        # created file at specified page number
                        elif match != None:
                            
                            # Takes off metadata from match name
                            cleanMatch = match.group(0)

                            # Returns county name from match and subtracts two from page number
                            # to account for Python number index
                            rawCountyValue = sortedDict.get(cleanMatch)
                            countyValue = rawCountyValue - 2

                            print(f"County match {cleanMatch} found in {input_path}")   
                            
                            # creates new file with new page range
                            for outPage in range(len(pdf_reader.pages)):
                                
                                # adds current page one by one
                                current_page = pdf_reader.pages[outPage]

                                # Condition for if length of pages is <= county page number
                                if outPage <= countyValue:
                                    continue
                                
                                # Adds page to new file
                                pdf_writer.add_page(current_page)

                            
                            # Creates and saves new file
                            with open(output_path, 'wb') as output_file:
                                    
                                pdf_writer.write(output_file)

                            output_file.close()

            # Increment progress bar value after each file completed
            my_progress["value"] += newCount
            my_progress.update()

            # Updates "Current file" to display current file number
            progressLabel.config(text= f"Processing file: {labelCount}", font=('Arial', 14))

        # Process completion pop-up
        messagebox.showinfo("PA Cleanup", "Task Successfully Completed!")
        
        # Closes progress bar window and reverts directory 
        # to directory where program is stored
        
        root.destroy()
        os.chdir(cwd)
        sys.stdout = temp
        outputLog.close()

            
  
    # function to call on the "add county" class
    def openAddCountyWindow(self):
        
        # Class first function in secondary_window class to run class
        self.window = QtWidgets.QMainWindow()
        self.ui = secondary_window()
        self.ui.setupUi(self.window)
        self.window.show()
    

    # calls translation function to allow for use of gui
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PA County Cleanup"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">PA County Cleanup</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Select File"))
        self.pushButton.setText(_translate("MainWindow", "Add County"))
    

# Begins whole program through calling mainWindow class
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# keeps progress bar window running
root.mainloop()

from PyQt5 import QtCore, QtWidgets
import os
from tkinter import messagebox

class secondary_window(object):
    
    def setupUi(self, Form):
        
        Form.setObjectName("Form")
        Form.resize(359, 243)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(130, 190, 101, 41))
        self.pushButton.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        
        #close window
        self.pushButton.clicked.connect(self.addCounty)
        
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(40, 60, 283, 73))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        
        self.lineEdit_2.setText("")
        countyName = self.lineEdit_2.text()    
        print("this is county - ", countyName)
        
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        
        self.lineEdit.setText("")
        
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    
    def addCounty(self):
        
        self.newKey = self.lineEdit_2.text()
        self.newValue = self.lineEdit.text()
        
        print("county", self.lineEdit_2.text())
        print("number", self.lineEdit.text())
    
        countyList = {}
        countyListFile = 'county_list.txt'
        fileTrue = os.path.isfile(countyListFile)
        
        newKey = self.newKey.upper()
        newValue = self.newValue
        newAddition = f"{newKey} {newValue}"
        
        print("newAddition - ", newAddition)
        if fileTrue == True and newAddition != " ":
            print("file True - ", fileTrue)
            with open(countyListFile, 'a') as f:
                    
                    f.write("\n")
                    f.write(newAddition)
                    print("Full dictionary - ", countyList)
        elif newAddition == " ":
            
            messagebox.showinfo("PA County Cleanup", f"No county or number entered... good bye!")
            pass        
        else:
            messagebox.showinfo("PA County Cleanup", f"Error, could not find {countyListFile}\n please check for name correctness")
        QtWidgets.QApplication.instance().quit()
      
 
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PA County Cleanup"))
        self.pushButton.setText(_translate("Form", "Finish"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"> Enter page number:</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\">Enter county name:</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = secondary_window()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

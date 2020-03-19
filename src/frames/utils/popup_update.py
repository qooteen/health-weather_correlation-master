from PyQt5 import QtCore, QtWidgets

class Ui_Form_update(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 100)
        self.box_label = QtWidgets.QLabel(Form)
        self.box_label.setGeometry(QtCore.QRect(20, 15, 10, 10))
        self.box_label.setMinimumSize(QtCore.QSize(400, 20))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(425, 45, 190, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QtCore.QSize(100, 20))
        self.sampels_box = QtWidgets.QComboBox(Form)
        self.sampels_box.setGeometry(QtCore.QRect(10, 45, 0, 20))
        self.sampels_box.setMinimumSize(QtCore.QSize(400, 40))
        self.sampels_box.setObjectName("sampels_box")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить показатели здоровья для выбранного пациента"))
        self.pushButton.setText(_translate("Form", "Добавить показатели"))
        self.box_label.setText(_translate("Form", "Выбрать пациента:"))


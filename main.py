import decimal
import sys
import os
import re
from PyQt5 import QtWidgets
from decimal import Decimal
from decimal import *
import design


def to_string(number):
    return format(number.normalize(), '^10,.10f').replace(',', ' ').rstrip('0').rstrip('.')


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.initiate_calculation)
        self.lab12.triggered.connect(self.set_lab12)
        self.lab3.triggered.connect(self.set_lab3)
        self.answer_number = 0
        self.lab_number = 1

    def set_lab12(self):
        self.lab_number = 0
        self.number1.setText("Эта клетка заблокирована")
        self.number4.setText("Эта клетка заблокирована")
        self.rounded.setText("Эта клетка заблокирована")

    def set_lab3(self):
        self.lab_number = 1

    def parse_strings(self, str):
        if re.fullmatch(r'^((\+)|-)?(\d{1,3})((( ?(\d{3}))?)+)(((\.)|,)(\d{1,10}))?$', str):
            str = str.replace(',', '.')
            str = str.replace(' ', '')
            return Decimal(str), 0
        else:
            return 0, 1

    def switch_operator(self, oper, num1, num2):
        result = 0
        match oper:
            case ("+"):
                result = Decimal(num1 + num2)
            case ("-"):
                result = Decimal(num1 - num2)
            case ("*"):
                result = Decimal(num1 * num2)
            case ("/"):
                if num2 == Decimal("0"):
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("Абшыбка")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setText("Я вам запрещаю делить на 0")
                    msg.exec_()
                    return Decimal("0")
                result = Decimal(num1 / num2)

        return result

    def initiate_calculation(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Абшыбка")
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        error = 0
        getcontext().prec = 24
        self.answer.setText("Жду пока введут нормальное число:(")
        if self.lab_number == 1:
            nums = [self.number1.text(), self.number2.text(), self.number3.text(), self.number4.text()]
            values = [0, 0, 0, 0]
        else:
            nums = [self.number2.text(), self.number3.text()]
            values = [0, 0, 0, 0]

        for index, num in enumerate(nums, 1):
            if num == '':
                num = Decimal("0")
                match (index):
                    case 1:
                        self.number1.setText("0")
                    case 2:
                        self.number2.setText("0")
                    case 3:
                        self.number3.setText("0")
                    case 4:
                        self.number4.setText("0")
            else:
                if self.lab_number==1:
                    values[index - 1], error = self.parse_strings(num)
                else:
                    values[index], error = self.parse_strings(num)
                if error:
                    msg.setText("Пожалуйста, введите НОРМАЛЬНОЕ число")
                    msg.exec_()
                    return

        oper2 = self.comboBox.currentText()
        oper1 = self.operator1.currentText()
        oper3 = self.operator3.currentText()

        res = self.switch_operator(oper2, values[1], values[2])
        if self.lab_number == 1:
            if oper3 == "*" or oper3 == "/":
                res3 = self.switch_operator(oper3, res, values[3])
                res = self.switch_operator(oper1, values[0], res3)
            else:
                res1 = self.switch_operator(oper1, values[0], res)
                res = self.switch_operator(oper3, res1, values[3])

        self.answer_number = res
        self.answer.setText(to_string(res))
        if self.lab_number == 1:
            self.initiate_rounding()
        else:
            self.number1.setText("")
            self.number4.setText("")
            self.rounded.setText("")

    def initiate_rounding(self):
        switch = self.rounding.currentText()

        match switch:
            case "Математическое округление":
                self.rounded.setText((to_string(self.answer_number.quantize(Decimal("1."), decimal.ROUND_HALF_UP))))
            case "Банковское Округление":
                self.rounded.setText(
                    (to_string(self.answer_number.quantize(Decimal("1."), decimal.ROUND_HALF_EVEN))))
            case "Усечение":
                self.rounded.setText(
                    (to_string(self.answer_number.quantize(Decimal("1."), decimal.ROUND_FLOOR))))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.setFixedHeight(150)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

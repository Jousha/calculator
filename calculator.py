"""

Calculator programme with GUI functions
Allows for basic mathematical functions as well as x² and √x
Allows for accounting functions VAT+ and VAT-
M+ and recall functions also available

"""

import sys
import math
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QButtonGroup, QMessageBox
from PyQt5.QtCore import Qt

VAT_PLUS = 1.2
VAT_MINUS = (5/6)


class Calculator(QWidget):

    def __init__(self):
        '''
        Initialisation of class object, show GUI and pass to ui initialisation 
        function.
        '''        
        super().__init__()
        
        self.setGeometry(600, 300, 395, 355)
        self.setWindowTitle("Calculator")
        
        self.show()
        
        self.init_ui()
        
    def init_ui(self):
        '''
        Initialise all buttons for the calculator and place them on the GUI.
        Also stores button click connections so to pass to required functions.
        '''
        
        # Top QLineEdit to store input and answers
        self.answer_box = QLineEdit("0")
        self.answer_box.setStyleSheet("font-size: 30px")
        self.answer_box.setFixedSize(400, 80)
        # Set alignment of text within answer_box
        self.answer_box.setAlignment(Qt.AlignRight)

        # Dictionaries to store all buttons and references
        # self.number_dict for numbers
        # self.operand_dict for all other operators
        # Keys will be face values i.e, "="
        # Values will be the reference to the QPushButton associated
        self.number_dict = {}
        self.operand_dict = {}
        
        # Create QHBoxLayouts needed for formatting
        # Order placed is order to appear on GUI
        h_layout_ops = QHBoxLayout()
        h_layout_funcs = QHBoxLayout()
        h_layout_seven = QHBoxLayout()
        h_layout_four = QHBoxLayout()
        h_layout_one = QHBoxLayout()
        h_layout_zero = QHBoxLayout()
        
        # Initialise buttons for h_layout_ops line
        self.memory_set = self.create_button("M+", (75, 35), h_layout_ops)
        self.memory_recall = self.create_button("MR", (75, 35), h_layout_ops)
        self.vat_add = self.create_button("VAT+", (75, 35), h_layout_ops)
        self.vat_minus = self.create_button("VAT-", (75, 35), h_layout_ops)
        self.clear_everything = self.create_button("CE", (75, 35), h_layout_ops)
        
        # Initialise buttons for h_layout_funcs
        self.open_bracket = self.create_button("(", (75, 35), h_layout_funcs)
        self.close_bracket = self.create_button(")", (75, 35), h_layout_funcs)
        self.x_squared = self.create_button("x²", (75, 35), h_layout_funcs)
        self.square_root = self.create_button("√x", (75, 35), h_layout_funcs)
        self.clear = self.create_button("C", (75, 35), h_layout_funcs)
        
        # Initialise buttons for 0 - 9
        for i in range(0, 10):
            self.btn = QPushButton(str(i))
            self.btn.setFixedSize(95, 60)
            if i == 0:
                h_layout_zero.addWidget(self.btn)
            elif 1 <= i <= 3:
                h_layout_one.addWidget(self.btn)
            elif 4 <= i <= 6:
                h_layout_four.addWidget(self.btn)
            else:
                h_layout_seven.addWidget(self.btn)
            self.number_dict[i] = self.btn

        # Initialise remaining buttons for h layouts seven, four, one and zero
        self.plus = self.create_button("+", (95, 60), h_layout_seven)
        h_layout_seven.setAlignment(Qt.AlignCenter)
        
        self.minus = self.create_button("-", (95, 60), h_layout_four)
        h_layout_four.setAlignment(Qt.AlignCenter)
        
        self.times = self.create_button("*", (95, 60), h_layout_one)
        h_layout_one.setAlignment(Qt.AlignCenter)
        
        self.decimal_point = self.create_button(".", (95, 60), h_layout_zero)
        self.equals = self.create_button("=", (95, 60), h_layout_zero)
        self.divide = self.create_button("/", (95, 60), h_layout_zero)
        h_layout_zero.setAlignment(Qt.AlignCenter)
        
        # Add operators to dict for later function connections
        self.operand_dict["+"] = self.plus
        self.operand_dict["-"] = self.minus
        self.operand_dict["*"] = self.times
        self.operand_dict["/"] = self.divide
        self.operand_dict["("] = self.open_bracket
        self.operand_dict[")"] = self.close_bracket
        self.operand_dict["."] = self.decimal_point
        
        # Set up final layout
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.answer_box)
        v_layout.addLayout(h_layout_ops)
        v_layout.addLayout(h_layout_funcs)
        v_layout.addLayout(h_layout_seven)
        v_layout.addLayout(h_layout_four)
        v_layout.addLayout(h_layout_one)
        v_layout.addLayout(h_layout_zero)
        v_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(v_layout)
        
        # Pass to button functions
        self.connections()
        
    def create_button(self, shown_name, size, layout):
        '''
        Creates a QPushButton object from parameters given.
        Input:
            shown_name - A string of the name to be shown on the button
            size - A tuple of the width and height of the button
            layout - A QVBoxLayout or QHBoxLayout where the button will 
            be added to
        Returns:
            QPushButton object
        '''
        
        self.btn = QPushButton(shown_name)
        self.btn.setFixedSize(size[0], size[1])
        layout.addWidget(self.btn)
        return self.btn
        
    def connections(self):
        '''
        Connections from buttons clicked to the functions which perform the 
        required action.
        '''
        # Button groups to be used in button functions
        self.number_group = QButtonGroup()
        self.operand_group = QButtonGroup()
        
        for key, value in self.number_dict.items():
            self.number_group.addButton(value)
        
        for key, value in self.operand_dict.items():
            self.operand_group.addButton(value)
        
        # Checks on user input and self.answer_box formatting
        self.equals_used = False
        self.answer_box.textChanged.connect(self.answer_box_updated)
        self.answer_box.returnPressed.connect(self.equals_clicked)
        
        # Connections to button functions stored in order of appearance on GUI
        self.number_group.buttonClicked.connect(self.number_clicked)
        self.operand_group.buttonClicked.connect(self.operand_clicked)
        self.memory_set.clicked.connect(self.memory_set_clicked)
        self.memory_recall.clicked.connect(self.memory_recall_clicked)
        self.vat_add.clicked.connect(self.vat_add_clicked)
        self.vat_minus.clicked.connect(self.vat_minus_clicked)
        self.clear_everything.clicked.connect(self.clear_everything_clicked)
        self.x_squared.clicked.connect(self.x_squared_clicked)
        self.square_root.clicked.connect(self.square_root_clicked)
        self.clear.clicked.connect(self.clear_clicked)
        self.equals.clicked.connect(self.equals_clicked)
        
    def answer_box_updated(self):
        '''
        Checks that the user does not enter unusable characters such as letters.
        '''
        acceptable_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "(", ")", "/", "*", "-", "+"]
        text = self.answer_box.text()
        for i in text:
            try:
                acceptable_list.index(i)
            except Exception:
                self.answer_box.setText(text.replace(i, ""))
                QMessageBox.about(self, "Input Error", "Input must be a number or operator")
        
    def number_clicked(self, number):
        '''
        Edits value of self.answer_box to represent which button the user has 
        clicked. Keeps track of self.equals_used to determine if field should 
        be wiped and restarted as the first sum has ended.
        '''
        
        if self.equals_used:
            self.answer_box.setText(number.text())
            self.equals_used = False
        else:
            if self.answer_box.text() == "0":
                self.answer_box.setText(number.text())
            else:
                self.answer_box.setText("{}{}".format(self.answer_box.text(), number.text()))
        
    def operand_clicked(self, operand):
        '''
        Update self.answer_box with mathematical operators.
        '''
        self.answer_box.setText("{}{}".format(self.answer_box.text(), operand.text()))
        self.equals_used = False
                
    def memory_set_clicked(self):
        '''
        Stores self.answer_box.text() in memory.
        '''
        self.memory = self.answer_box.text()
        
    def memory_recall_clicked(self):
        '''
        Recalls stored memory for use in sum.
        '''
        if self.answer_box.text() == "" or self.answer_box.text()[-1] in self.operand_dict.keys():
            self.answer_box.setText("{}{}".format(self.answer_box.text(), self.memory))
        else:
            self.answer_box.setText(self.memory)

    def vat_add_clicked(self):
        '''
        Adds VAT to current value in self.answer_box.
        '''
        global VAT_PLUS
        self.answer_box.setText(str(eval(self.answer_box.text())*VAT_PLUS))
        self.equals_clicked()
        
    def vat_minus_clicked(self):
        '''
        Removes VAT from current value in self.answer_box.
        '''        
        global VAT_MINUS
        self.answer_box.setText(str(eval(self.answer_box.text())*VAT_MINUS))
        self.equals_clicked()

    def clear_everything_clicked(self):
        '''
        Resets the value of self.answer_box to 0.
        '''
        self.answer_box.setText("0")
    
    def x_squared_clicked(self):
        '''
        Squares and updates the current value of self.answer_box.
        '''
        self.answer_box.setText(str(eval(self.answer_box.text())**2))
        self.equals_clicked()
        
    def square_root_clicked(self):
        '''
        Square roots and updates the current value of self.answer_box.
        '''
        self.answer_box.setText(str(math.sqrt(eval(self.answer_box.text()))))
        self.equals_clicked()
        
    def clear_clicked(self):
        '''
        Removes the last value input into self.answer_box.
        '''
        self.answer_box.setText(self.answer_box.text()[:-1])

    def equals_clicked(self):
        '''
        Evaluates the value in self.answer_box.
        '''
        try:
            self.answer_box.setText(str(eval(self.answer_box.text())))
            if self.answer_box.text()[-2:] == ".0":
                self.answer_box.setText(self.answer_box.text()[0:-2])
            self.equals_used = True
        except SyntaxError:
            QMessageBox.about(self, "Sum Error", "Sum not valid")
 
def main():
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

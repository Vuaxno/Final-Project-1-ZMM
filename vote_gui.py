from PyQt6 import QtCore, QtWidgets
from logic import VoteManager

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(265, 283)
        MainWindow.setMaximumSize(QtCore.QSize(500, 400))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vote_title = QtWidgets.QLabel(parent=self.centralwidget)
        self.vote_title.setGeometry(QtCore.QRect(60, 20, 141, 31))
        self.vote_title.setToolTipDuration(0)
        self.vote_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.vote_title.setAutoFillBackground(True)
        self.vote_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vote_title.setObjectName("vote_title")
        self.button_Frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.button_Frame.setGeometry(QtCore.QRect(70, 110, 120, 91))
        self.button_Frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.button_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.button_Frame.setObjectName("button_Frame")
        self.jane_button = QtWidgets.QRadioButton(parent=self.button_Frame)
        self.jane_button.setGeometry(QtCore.QRect(20, 20, 82, 17))
        self.jane_button.setObjectName("jane_button")
        self.john_button = QtWidgets.QRadioButton(parent=self.button_Frame)
        self.john_button.setGeometry(QtCore.QRect(20, 40, 82, 17))
        self.john_button.setObjectName("john_button")
        self.candidate_label = QtWidgets.QLabel(parent=self.button_Frame)
        self.candidate_label.setGeometry(QtCore.QRect(20, 0, 71, 16))
        self.candidate_label.setObjectName("candidate_label")
        self.submit_button = QtWidgets.QPushButton(parent=self.button_Frame)
        self.submit_button.setGeometry(QtCore.QRect(20, 60, 81, 21))
        self.submit_button.setMaximumSize(QtCore.QSize(500, 400))
        self.submit_button.setObjectName("submit_button")
        self.input_box = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.input_box.setGeometry(QtCore.QRect(100, 60, 113, 20))
        self.input_box.setObjectName("input_box")
        self.id_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.id_label.setGeometry(QtCore.QRect(70, 60, 16, 16))
        self.id_label.setObjectName("id_label")
        self.error_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.error_label.setGeometry(QtCore.QRect(10, 210, 210, 16))
        self.error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.error_label.setObjectName("error_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 265, 21))
        self.menubar.setObjectName("menubar")
        self.menuZaids_voting = QtWidgets.QMenu(parent=self.menubar)
        self.menuZaids_voting.setObjectName("menuZaids_voting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuZaids_voting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "vote_gui"))
        self.vote_title.setText(_translate("MainWindow", "VOTING APPLICATION"))
        self.jane_button.setText(_translate("MainWindow", "Jane"))
        self.john_button.setText(_translate("MainWindow", "John"))
        self.candidate_label.setText(_translate("MainWindow", "CANDIDATES"))
        self.submit_button.setText(_translate("MainWindow", "SUBMIT VOTE"))
        self.id_label.setText(_translate("MainWindow", "ID"))
        self.error_label.setText(_translate("MainWindow", "Already Voted"))
        self.menuZaids_voting.setTitle(_translate("MainWindow", "Zaids voting"))

class VotingApp(QtWidgets.QMainWindow):
    def __init__(self) :
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # clear any placeholder text
        self.ui.error_label.setText("")

        # initialize business logic
        self.manager = VoteManager("votes.csv")

        # connect submit button
        self.ui.submit_button.clicked.connect(self.submit_vote)

    def submit_vote(self) :
        voter_id = self.ui.input_box.text().strip()
        candidate = "Jane" if self.ui.jane_button.isChecked() else "John"

        try:
            self.manager.record_vote(voter_id, candidate)
        except ValueError as ve:
            return self.show_message(str(ve), success=False)
        except IOError as ioe:
            return self.show_message(str(ioe), success=False)

        # success
        self.show_message("Vote recorded!", success=True)
        self.show_results()

    def show_message(self, msg: str, success: bool) :
        """
        Display feedback in the label: green on success, red on error.
        """
        color = "green" if success else "red"
        self.ui.error_label.setStyleSheet(f"color: {color}")
        self.ui.error_label.setText(msg)

    def show_results(self) :
        """
        Pop up a dialog with vote counts and current winner.
        """
        results = self.manager.get_results()
        winner = self.manager.get_winner()
        lines = [f"{cand}: {count}" for cand, count in results.items()]
        summary = "\n".join(lines) + f"\n\nWinner: {winner}"
        QtWidgets.QMessageBox.information(self, "Current Results", summary)




class VotingApp(QtWidgets.QMainWindow):
    def __init__(self) :
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # clear any placeholder text
        self.ui.error_label.setText("")

        # initialize business logic
        self.manager = VoteManager("votes.csv")

        # connect submit button
        self.ui.submit_button.clicked.connect(self.submit_vote)

    def submit_vote(self) :
        voter_id = self.ui.input_box.text().strip()
        candidate = "Jane" if self.ui.jane_button.isChecked() else "John"

        try:
            self.manager.record_vote(voter_id, candidate)
        except ValueError as ve:
            return self.show_message(str(ve), success=False)
        except IOError as ioe:
            return self.show_message(str(ioe), success=False)

        # success
        self.show_message("Vote recorded!", success=True)
        self.show_results()

    def show_message(self, msg: str, success: bool) :
        """
        Display feedback in the label: green on success, red on error.
        """
        color = "green" if success else "red"
        self.ui.error_label.setStyleSheet(f"color: {color}")
        self.ui.error_label.setText(msg)

    def show_results(self) :
        """
        Pop up a dialog with vote counts and current winner.
        """
        results = self.manager.get_results()
        winner = self.manager.get_winner()
        lines = [f"{cand}: {count}" for cand, count in results.items()]
        summary = "\n".join(lines) + f"\n\nWinner: {winner}"
        QtWidgets.QMessageBox.information(self, "Current Results", summary)

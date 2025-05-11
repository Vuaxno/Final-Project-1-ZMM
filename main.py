from vote_gui import *
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = VotingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

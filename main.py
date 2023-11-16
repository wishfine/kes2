# main.py
import sys
from PyQt5.QtWidgets import QApplication
from teaching_plan_generator import TeachingPlanGenerator

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TeachingPlanGenerator()
    window.show()
    sys.exit(app.exec_())

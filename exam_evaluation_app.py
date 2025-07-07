# exam_evaluation_app.py

import tkinter as tk
from login_page import LoginPage
from student_details import StudentDetailsPage
from offline_page import OfflineEvaluationPage
from online_page import OnlineEvaluationPage

class ExamEvaluationApp:
    def __init__(self, root):
        self.root = root
        self.show_login()

    def show_login(self):
        self.login_page = LoginPage(self.root, self.on_login_success)

    def on_login_success(self, student_login_info):
        self.show_student_details(student_login_info)

    def show_student_details(self, student_login_info):
        self.details_page = StudentDetailsPage(
            self.root,
            student_login_info,
            self.on_mode_selected
        )

    def on_mode_selected(self, mode, full_student_info):
        if mode == "offline":
            self.offline_page = OfflineEvaluationPage(self.root, full_student_info)
        else:
            self.online_page = OnlineEvaluationPage(self.root, full_student_info)

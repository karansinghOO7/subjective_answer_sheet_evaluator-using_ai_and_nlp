import tkinter as tk
from login_page import LoginPage
from student_details import StudentDetailsPage
from offline_page import OfflineEvaluationPage
from online_page import OnlineEvaluationPage

class ExamEvaluationApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Exam Evaluation System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.student_info = {}
        self.show_login()

    def show_login(self):
        self.clear_window()
        self.login_page = LoginPage(self.root, self.on_login_success)

    def on_login_success(self, user_info):
        """Callback after successful login"""
        self.student_info = user_info
        self.show_student_details()

    def show_student_details(self):
        self.clear_window()
        self.student_details_page = StudentDetailsPage(
            self.root,
            self.student_info,
            self.on_mode_selected
        )

    def on_mode_selected(self, selected_mode, updated_info):
        """Callback from student details page after selecting mode"""
        self.student_info.update(updated_info)

        if selected_mode == "offline":
            self.show_offline_evaluation()
        elif selected_mode == "online":
            self.show_online_evaluation()
        else:
            print("Invalid mode selected")

    def show_offline_evaluation(self):
        self.clear_window()
        self.offline_page = OfflineEvaluationPage(self.root, self.student_info)

    def show_online_evaluation(self):
        self.clear_window()
        self.online_page = OnlineEvaluationPage(self.root, self.student_info)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamEvaluationApp(root)
    root.mainloop()

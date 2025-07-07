import tkinter as tk
from tkinter import messagebox

class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Student Exam Grading System - Login")
        self.root.geometry("600x300")
        self.create_login_ui()

    def create_login_ui(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        

        frame = tk.Frame(self.root)
        frame.pack(pady=50)

        tk.Label(frame, text="Roll No.").grid(row=0, column=0, sticky="w", pady=5)
        self.roll_entry = tk.Entry(frame)
        self.roll_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Date of Birth (dd/mm/yyyy)").grid(row=1, column=0, sticky="w", pady=5)
        self.dob_entry = tk.Entry(frame)
        self.dob_entry.grid(row=1, column=1, pady=5)

        login_btn = tk.Button(frame, text="Login", command=self.validate_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)

    def validate_login(self):
        roll = self.roll_entry.get().strip()
        dob = self.dob_entry.get().strip()
        if roll and dob:
            self.on_login_success({"roll_no": roll, "dob": dob})
        else:
            messagebox.showerror("Login Failed", "Please enter both Roll No. and Date of Birth.")

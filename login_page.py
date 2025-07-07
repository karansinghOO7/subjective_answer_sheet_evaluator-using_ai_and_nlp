import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginPage:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.root.title("Student Exam Grading System - Login")
        self.root.geometry("600x300")
        self.create_login_ui()

    def create_login_ui(self):
        self.clear_frame()

        left_frame = tk.Frame(self.root, width=250, height=300)
        left_frame.pack(side="left", fill="y")

        right_frame = tk.Frame(self.root, width=350, height=300)
        right_frame.pack(side="right", fill="both", expand=True)

        try:
            img_path = r"C:\Users\karan\Desktop\major_project\new_2\picture1.jpg"
            image = Image.open(img_path)
            image = image.resize((250, 300))
            photo = ImageTk.PhotoImage(image)
            img_label = tk.Label(left_frame, image=photo)
            img_label.image = photo
            img_label.pack()
        except Exception:
            tk.Label(left_frame, text="Image not found").pack()

        tk.Label(right_frame, text="Login", font=("Helvetica", 18)).pack(pady=20)

        tk.Label(right_frame, text="Roll No.").pack()
        self.roll_entry = tk.Entry(right_frame)
        self.roll_entry.pack()

        tk.Label(right_frame, text="Date of Birth (dd/mm/yyyy)").pack()
        self.dob_entry = tk.Entry(right_frame)
        self.dob_entry.pack()

        tk.Button(right_frame, text="Login", command=self.validate_login).pack(pady=20)

    def validate_login(self):
        roll = self.roll_entry.get().strip()
        dob = self.dob_entry.get().strip()
        if roll and dob:
            user_info = {
                "roll": roll,
                "dob": dob
            }
            self.on_success_callback(user_info)
        else:
            messagebox.showerror("Login Failed", "Please enter both Roll No. and Date of Birth.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

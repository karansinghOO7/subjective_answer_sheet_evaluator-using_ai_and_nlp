import tkinter as tk
from tkinter import filedialog, messagebox

class StudentDetailsPage:
    def __init__(self, root, student_info, on_mode_selected):
        self.root = root
        self.student_info = student_info
        self.on_mode_selected = on_mode_selected
        self.create_ui()

    def create_ui(self):
        self.clear_window()

        tk.Label(self.root, text="Student Details", font=("Helvetica", 18)).pack(pady=10)

        self.name_var = tk.StringVar()
        self.branch_var = tk.StringVar()
        self.subject_var = tk.StringVar()

        tk.Label(self.root, text="Name").pack()
        self.name_entry = tk.Entry(self.root, textvariable=self.name_var)
        self.name_entry.pack()

        tk.Label(self.root, text="Branch").pack()
        self.branch_entry = tk.Entry(self.root, textvariable=self.branch_var)
        self.branch_entry.pack()

        tk.Label(self.root, text="Subject").pack()
        self.subject_entry = tk.Entry(self.root, textvariable=self.subject_var)
        self.subject_entry.pack()

        tk.Button(self.root, text="Upload Student Answer PDF", command=self.upload_pdf).pack(pady=10)

        # Buttons to choose between offline and online evaluation
        tk.Button(self.root, text="Offline Evaluation", command=self.select_offline).pack(pady=5)
        tk.Button(self.root, text="Online Evaluation", command=self.select_online).pack(pady=5)

    def upload_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            self.student_info['pdf_path'] = filepath
            messagebox.showinfo("PDF Uploaded", f"Selected File: {filepath}")

    def select_offline(self):
        if self.check_details_complete():
            self.on_mode_selected("offline", self.get_student_info())
        else:
            messagebox.showwarning("Missing Info", "Please fill all details and upload the PDF.")

    def select_online(self):
        if self.check_details_complete():
            self.on_mode_selected("online", self.get_student_info())
        else:
            messagebox.showwarning("Missing Info", "Please fill all details and upload the PDF.")

    def get_student_info(self):
        return {
            "name": self.name_var.get().strip(),
            "branch": self.branch_var.get().strip(),
            "subject": self.subject_var.get().strip(),
            "pdf": self.student_info.get("pdf_path", "")
        }

    def check_details_complete(self):
        return (
            self.name_var.get().strip() and
            self.branch_var.get().strip() and
            self.subject_var.get().strip() and
            self.student_info.get("pdf_path", "")
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

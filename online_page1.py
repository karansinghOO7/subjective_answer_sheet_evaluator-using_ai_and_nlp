import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
import io

class OnlineEvaluationPage:
    def __init__(self, root, student_info):
        self.root = root
        self.student_info = student_info
        self.root.title("Online Evaluation")
        self.root.geometry("800x600")
        self.create_ui()

    def create_ui(self):
        self.clear_frame()
        self.text_box = tk.Text(self.root, wrap="word", height=25)
        self.text_box.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self.root, text="Upload Answer Sheet (PDF)", command=self.upload_pdf).pack(pady=5)
        tk.Button(self.root, text="Start Evaluation", command=self.evaluate).pack(pady=10)

    def upload_pdf(self):
        self.student_pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.student_pdf_path:
            messagebox.showinfo("PDF Selected", f"Student Answer Sheet Loaded: {self.student_pdf_path}")

    def evaluate(self):
        if not hasattr(self, 'student_pdf_path'):
            messagebox.showerror("Missing PDF", "Please upload a student answer sheet.")
            return

        extracted_text = self.extract_text_from_pdf(self.student_pdf_path)
        self.text_box.insert(tk.END, "Extracted Text:\n" + extracted_text + "\n\n")
        
        # Mock DeepSeek R1 API Call (replace with actual API call)
        response = self.send_to_deepseek_api(extracted_text)
        self.text_box.insert(tk.END, "Evaluation Feedback:\n" + response)

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes()))
            gray = img.convert('L')
            binarized = gray.point(lambda x: 0 if x < 128 else 255, '1')
            ocr_text = pytesseract.image_to_string(binarized)
            text += ocr_text + "\n"
        return text.strip()

    def send_to_deepseek_api(self, text):
        # This is a placeholder for actual DeepSeek R1 API integration
        # Replace with code that calls the API and returns the evaluation result
        return "DeepSeek Evaluation (Mocked):\n - Answer Relevance: 8/10\n - Clarity: 7/10\n - Overall Score: 7.5/10"

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

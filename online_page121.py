import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import openai
import os

class OnlineEvaluationPage:
    def __init__(self, root, student_info):
        self.root = root
        self.student_info = student_info
        self.root.title("Online Evaluation with DeepSeek R1")
        self.root.geometry("800x600")
        self.api_key = "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"
        self.create_ui()

    def create_ui(self):
        self.clear_frame()

        self.text_box = tk.Text(self.root, wrap="word", height=25)
        self.text_box.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self.root, text="Upload Model Answer", command=self.upload_model_answer).pack(pady=5)
        tk.Button(self.root, text="Start Online Evaluation", command=self.evaluate_online).pack(pady=10)

    def upload_model_answer(self):
        self.model_answer_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.model_answer_path:
            messagebox.showinfo("Model Answer", f"Loaded: {self.model_answer_path}")

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes()))
            gray = img.convert('L')
            bin_img = gray.point(lambda x: 0 if x < 128 else 255, '1')
            page_text = pytesseract.image_to_string(bin_img)
            text += page_text + "\n"
        return text

    def split_answers(self, raw_text):
        parts = raw_text.split("ANS")
        return [ans.strip() for ans in parts[1:]]

    def load_model_answers(self):
        with open(self.model_answer_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return [ans.strip() for ans in text.split("ANS")[1:]]

    def evaluate_online(self):
        if not hasattr(self, 'model_answer_path'):
            messagebox.showerror("Error", "Please upload a model answer first.")
            return

        self.text_box.insert(tk.END, "Extracting and evaluating answers...\n")
        extracted_text = self.extract_text_from_pdf(self.student_info["pdf"])
        student_answers = self.split_answers(extracted_text)
        model_answers = self.load_model_answers()

        if len(student_answers) != len(model_answers):
            self.text_box.insert(tk.END, "⚠️ Number of student answers and model answers do not match.\n")

        for i, (student_ans, model_ans) in enumerate(zip(student_answers, model_answers)):
            try:
                score, feedback = self.get_deepseek_score(student_ans, model_ans)
                result_text = f"Q{i+1} Score: {score}/10\nFeedback: {feedback}\n\n"
                self.text_box.insert(tk.END, result_text)
            except Exception as e:
                self.text_box.insert(tk.END, f"Q{i+1} Error: {str(e)}\n")

    def get_deepseek_score(self, student_answer, model_answer):
        openai.api_key = self.api_key

        prompt = (
            f"You are an exam evaluator.\n"
            f"Model Answer: {model_answer}\n"
            f"Student Answer: {student_answer}\n\n"
            f"Task:\n"
            f"1. Score the student answer out of 10.\n"
            f"2. Give a short explanation or feedback for the score.\n"
            f"Format the response as:\n"
            f"Score: <number>\n"
            f"Feedback: <your feedback>\n"
        )

        response = openai.ChatCompletion.create(
            model="deepseek-chat",  # adjust model name if needed
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response['choices'][0]['message']['content']
        score_line = next((line for line in content.splitlines() if line.lower().startswith("score")), "Score: 0")
        feedback_line = next((line for line in content.splitlines() if line.lower().startswith("feedback")), "Feedback: None")

        score = int(score_line.split(":")[1].strip())
        feedback = feedback_line.split(":", 1)[1].strip()

        return score, feedback

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

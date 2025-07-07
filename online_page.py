import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re
import threading
from openai import OpenAI


class OnlineEvaluationPage:
    def __init__(self, root, student_info):
        self.root = root
        self.student_info = student_info
        self.root.title("Online Evaluation with DeepSeek R1")
        self.root.geometry("800x600")
        self.api_key = "ADD YOUR API KEY" 
        self.create_ui()

    def create_ui(self):
        self.clear_frame()

        self.text_box = tk.Text(self.root, wrap="word", height=25)
        self.text_box.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self.root, text="Upload Answer Sheet", command=self.upload_pdf).pack(pady=5)
        tk.Button(self.root, text="Start Online Evaluation", command=self.evaluate_online).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def upload_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            self.student_info["pdf"] = pdf_path
            messagebox.showinfo("PDF Uploaded", f"Student answer sheet loaded:\n{pdf_path}")

    def evaluate_online(self):
        self.text_box.insert(tk.END, "Extracting and evaluating answers...\n")
        self.root.update()

        thread = threading.Thread(target=self.run_online_evaluation)
        thread.start()

    def run_online_evaluation(self):
        try:
            extracted_text = self.extract_text_from_pdf(self.student_info["pdf"])
            student_answers = self.split_answers(extracted_text)

            if not student_answers:
                self.text_box.insert(tk.END, "❌ No answers found after OCR.\n")
                return

            for i, answer in enumerate(student_answers):
                try:
                    score, feedback = self.get_deepseek_score(answer)
                    result_text = f"\nQ{i+1} Score: {score}/10\nFeedback: {feedback}\n"
                    self.text_box.insert(tk.END, result_text)
                except Exception as e:
                    self.text_box.insert(tk.END, f"\nQ{i+1} Error: {str(e)}\n")
        except Exception as e:
            self.text_box.insert(tk.END, f"\n❌ Evaluation failed: {str(e)}\n")

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
        pattern = r"Ans\s*\d+\s*(.*?)(?=(?:Ques\s*\d+|$))"
        matches = re.findall(pattern, raw_text, re.DOTALL | re.IGNORECASE)
        return [match.strip() for match in matches if match.strip()]


    def get_deepseek_score(self, student_answer):
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

        prompt = (
            f"You are an exam evaluator. Evaluate the following answer out of 10 "
            f"and provide a short feedback.\n\n"
            f"Student Answer:\n{student_answer}\n\n"
            f"Respond in this format:\n"
            f"Score: <number>\n"
            f"Feedback: <short feedback>"
        )

        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-zero:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "https://your-site.com",
                "X-Title": "StudentAnswerGrader"
            },
            temperature=0.3
        )

        content = response.choices[0].message.content
        score_match = re.search(r"score\s*:\s*(\d+)", content, re.IGNORECASE)
        feedback_match = re.search(r"feedback\s*:\s*(.*)", content, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 0
        feedback = feedback_match.group(1).strip() if feedback_match else "No feedback provided."

        return score, feedback

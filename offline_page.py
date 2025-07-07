import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors
import os
import io

# NLTK downloads
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load Word2Vec model
word2vec_model_path = r"C:\Users\karan\Desktop\major_project\new_2\word2vec\GoogleNews-vectors-negative300.bin"
try:
    w2v_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
    print("✅ Word2Vec model loaded successfully!")
except FileNotFoundError:
    print(f"❌ Model not found at {word2vec_model_path}")
    w2v_model = None
except Exception as e:
    print(f"❌ Error loading Word2Vec model: {e}")
    w2v_model = None


class OfflineEvaluationPage:
    def __init__(self, root, student_info):
        self.root = root
        self.student_info = student_info
        self.root.title("Offline Evaluation")
        self.root.geometry("1000x700")
        self.create_ui()

    def create_ui(self):
        self.clear_frame()

        tk.Label(self.root, text="Offline Evaluation", font=("Helvetica", 18)).pack(pady=10)

        self.text_box = tk.Text(self.root, wrap="word", height=25)
        self.text_box.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Button(self.root, text="Upload Model Answer", command=self.upload_model_answer).pack(pady=5)
        tk.Button(self.root, text="Start Evaluation", command=self.evaluate).pack(pady=10)

    def upload_model_answer(self):
        self.model_answer_path = filedialog.askopenfilename(filetypes=[("PDF or Text Files", "*.pdf *.txt")])
        if self.model_answer_path:
            messagebox.showinfo("Model Answer", f"Model Answer Loaded:\n{self.model_answer_path}")

    def evaluate(self):
        if not hasattr(self, 'model_answer_path'):
            messagebox.showerror("Missing Model Answer", "Please upload a model answer first.")
            return

        try:
            student_text = self.extract_text_from_pdf(self.student_info['pdf'])
            model_text = self.extract_text_from_pdf(self.model_answer_path)
        except Exception as e:
            messagebox.showerror("PDF Error", f"Error reading PDF:\n{str(e)}")
            return

        # Show OCR results first
        self.text_box.insert(tk.END, "===== OCR: Student Answer Sheet =====\n")
        self.text_box.insert(tk.END, student_text + "\n\n")
        self.text_box.insert(tk.END, "===== OCR: Model Answer Sheet =====\n")
        self.text_box.insert(tk.END, model_text + "\n\n")

        student_answers = self.split_answers(student_text)
        model_answers = self.split_answers(model_text)
        
        # Scoring
        results = []
        for i in range(min(len(student_answers), len(model_answers))):
            score, cos_sim, wmd_score = self.compare_answers(model_answers[i], student_answers[i])
            result = f"Q{i+1} Score: {score:.2f}/10 | Cosine: {cos_sim:.2f} | WMD Score: {wmd_score:.2f}\n"
            results.append(result)

        self.text_box.insert(tk.END, "\n===== Evaluation Results =====\n")
        self.text_box.insert(tk.END, "\n".join(results))

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
        return text

    def split_answers(self, text):
        split_text = text.split("ANS")
        answers = [part.strip() for part in split_text[1:]]
        return answers

    def compare_answers(self, model_ans, student_ans):
        # Tokenize and remove stopwords
        model_tokens = [w for w in word_tokenize(model_ans.lower()) if w.isalpha() and w not in stop_words]
        student_tokens = [w for w in word_tokenize(student_ans.lower()) if w.isalpha() and w not in stop_words]

        # Word Mover's Distance
        if w2v_model:
            try:
                wmd_distance = w2v_model.wmdistance(model_tokens, student_tokens)
                wmd_score = 1 / (1 + wmd_distance)
            except Exception as e:
                print(f"WMD Error: {e}")
                wmd_score = 0.0
        else:
            wmd_score = 0.0

        # Cosine Similarity using average Word2Vec vectors
        def get_avg_embedding(tokens):
            vectors = [w2v_model[word] for word in tokens if word in w2v_model]
            if not vectors:
                return [0] * 300
            return sum(vectors) / len(vectors)

        model_vector = get_avg_embedding(model_tokens)
        student_vector = get_avg_embedding(student_tokens)

        cos_sim = cosine_similarity([model_vector], [student_vector])[0][0]

        # Combine scores
        final_score = (cos_sim * 5 + wmd_score * 5)  # scale to 10

        return final_score, cos_sim, wmd_score

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

📝 Student Answer Sheet Evaluation System
A modular Python-based application to automatically evaluate student answer sheets (PDFs) using both offline NLP methods (Word2Vec, cosine similarity, WMD) and online AI models (DeepSeek R1 via OpenRouter API). Built with a user-friendly Tkinter GUI.

🚀 Features
🔐 Login system for students

📄 PDF upload of handwritten/typed answer sheets

🔍 OCR with PyMuPDF and Tesseract to extract answers

✨ Offline Evaluation

Compare with model answer using Word2Vec, Cosine Similarity, Word Mover's Distance

☁️ Online Evaluation

Evaluate directly via DeepSeek R1 API without model answers

📊 Score and feedback generation

🧠 Pre-trained models like Word2Vec and BERT (optional)

📋 Result displayed on GUI

🖥️ Tech Stack
Component	Technology
GUI	Python Tkinter
OCR	Tesseract, PyMuPDF
NLP	NLTK, Gensim (Word2Vec), Transformers
API Integration	OpenRouter API (DeepSeek R1)
Evaluation Logic	Cosine Similarity, WMD
Embeddings	GoogleNews Word2Vec (local .bin file)

📁 Folder Structure
eduevaluator/
├── gui/
│   ├── login.py
│   ├── student_details.py
│   ├── offline_page.py
│   └── online_page.py
├── evaluation/
│   ├── ocr_utils.py
│   ├── word2vec_utils.py
│   └── deepseek_api.py
├── models/
│   └── word2vec/
│       └── GoogleNews-vectors-negative300.bin
├── assets/
│   └── sample_pdfs/
├── main.py
├── README.md
└── requirements.txt
📦 Installation
1. Clone the repo
in cmd type-
git clone https://github.com/yourusername/eduevaluator.git
cd eduevaluator
2. Set up a virtual environment (optional)
type in cmd- python -m venv venv
venv\Scripts\activate  # On Windows
3. Install dependencies
in cmd type-
pip install -r requirements.txt
4. Install Tesseract OCR
Download: https://github.com/tesseract-ocr/tesseract

Add the installation path to your environment variables.

You may need to set the Tesseract path in code if not globally accessible:

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
⚙️ Configuration
🔑 DeepSeek API (via OpenRouter)
Replace this in online_page.py:
self.api_key = "your_openrouter_api_key"
Sign up and get a free key from:
👉 https://openrouter.ai

▶️ How to Run

python main.py
Then:

Login with roll number and DOB

Enter student details

Upload answer sheet (PDF)

Choose Offline or Online mode

View evaluation score and feedback!

✅ Sample Output

Extracting and evaluating answers...

Q1 Score: 7.5/10 | Cosine: 0.82 | WMD: 0.67
Q2 Score: 6.0/10 | Cosine: 0.74 | WMD: 0.58
Or for online mode:


Q1 Score: 8/10
Feedback: Clear and mostly correct, but lacks detail on edge cases.
🧠 Future Improvements
Export report to CSV or PDF

Admin dashboard for bulk evaluation

Add charts/analytics of performance

Cloud deployment with Flask/FastAPI

🧑‍💻 Contributors
Karan Singh – B.Tech Final Year, CSE
(Open to internships, job roles in AI, NLP, backend, or full stack)

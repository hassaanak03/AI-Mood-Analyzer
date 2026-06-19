# 🧠 AI Mood Analyzer

AI Mood Analyzer is a **Generative AI-powered web application** that analyzes user-provided text and detects the underlying mood or emotional state using the **Groq Compound** Large Language Model. The application features an intuitive web interface built with **Gradio** and is deployed on **Hugging Face Spaces**.

🔗 **Live Demo:** https://huggingface.co/spaces/hassaankhan/AI-Mood-Analyzer

---

## 🚀 Features

- Detects the mood from any text or message.
- Supports natural language input of any length.
- Provides fast AI-powered mood analysis.
- Clean and interactive Gradio interface.
- Cloud deployment with Hugging Face Spaces.
- Powered by Groq's high-speed inference API.

---

## 🛠️ Tech Stack

- **Python**
- **Gradio**
- **Groq API**
- **Groq Compound (LLM)**
- **Prompt Engineering**
- **Hugging Face Spaces**

---

## 📂 Project Structure

```text
AI-Mood-Analyzer/
│
├── app.py              # Main application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Mood-Analyzer.git
cd AI-Mood-Analyzer
```

### 2. Create a virtual environment (Optional)

```bash
python -m venv venv
```

Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run the Application

```bash
python app.py
```

The application will start locally and can be accessed through your browser.

---

## 💡 How It Works

1. Enter a sentence, paragraph, or message.
2. Click the **Analyze Mood** button.
3. The text is sent to the **Groq Compound** model through the **Groq API**.
4. The LLM analyzes the emotional context using carefully designed prompts.
5. The detected mood is displayed instantly.

---

## 🎯 Example

**Input**

```
I finally achieved my goal after months of hard work. I'm so excited!
```

**Output**

```
Mood: Excited 🎉
```

---

## 🧠 Skills Demonstrated

- Generative AI
- Large Language Models (LLMs)
- Prompt Engineering
- Natural Language Processing (NLP)
- Python Development
- API Integration
- Gradio UI Development
- AI Application Deployment

---

## 🌐 Deployment

The application is deployed on **Hugging Face Spaces**.

🔗 https://huggingface.co/spaces/hassaankhan/AI-Mood-Analyzer

---

## 🔮 Future Improvements

- Detect multiple emotions with confidence scores.
- Emotion visualization using charts.
- Emotion history tracking.
- Multilingual mood detection.
- Voice-to-text mood analysis.
- Sentiment trend analysis.
- Export analysis results.

---

## 👨‍💻 Author

**Hassaan Ahmed Khan**

- GitHub: https://github.com/hassaanak03
- LinkedIn: https://www.linkedin.com/in/hassaanak/
- Hugging Face: https://huggingface.co/hassaankhan

---
---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!

"""
AI Mood Analyzer (Groq-powered) - app.py
Deployable on Hugging Face Spaces.
- Uses Groq's OpenAI-compatible Chat Completions API.
- Gradio UI for user-facing interface.
- Requires GROQ_API_KEY in Space Secrets.
"""

import os
import json
import re
import requests
from typing import Tuple, Dict, Any
import gradio as gr
from datetime import datetime

# ----------------------------
# Configuration / Constants
# ----------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. Please add it in Hugging Face Space Secrets."
    )

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"

# Use a valid, non-deprecated Groq model:
DEFAULT_MODEL = "groq/compound"

REQUEST_TIMEOUT = 30  # seconds


# ----------------------------
# Prompt Engineering
# ----------------------------
BASE_SYSTEM_PROMPT = """
You analyze the emotional mood conveyed by a piece of text.
Return ONLY a JSON object with 3 keys:
  - mood: one of ["Happy","Sad","Angry","Stressed","Neutral","Surprised","Fearful","Disgusted"]
  - confidence: value between 0.0 and 1.0
  - explanation: one-sentence reason (<= 40 words)
"""

PROMPT_TEMPLATE = """
Text: \"\"\"{user_text}\"\"\"
Return valid JSON only, following this format strictly:
{{
  "mood": "...",
  "confidence": ...,
  "explanation": "..."
}}
"""


# ----------------------------
# JSON Extraction Utility
# ----------------------------
def extract_json_from_text(text: str) -> Dict[str, Any]:
    """Attempt to extract a JSON object from the model output."""
    text = text.strip()

    # Direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Find {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            return json.loads(candidate)
        except Exception:
            try:
                return json.loads(candidate.replace("'", '"'))
            except Exception:
                pass

    # Fallback: parse simple key/value style
    result = {}
    lines = text.splitlines()
    for line in lines:
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip().lower()
            v = v.strip().strip('"').strip("'")
            if k in ["mood", "explanation"]:
                result[k] = v
            elif k == "confidence":
                nums = re.findall(r"[0-9]*\.?[0-9]+", v)
                if nums:
                    result[k] = float(nums[0])

    return result


# ----------------------------
# Groq Chat Completion Call
# ----------------------------
def call_groq_chat(user_text: str, model: str = DEFAULT_MODEL) -> str:
    """Call Groq's OpenAI-compatible completion endpoint."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": BASE_SYSTEM_PROMPT},
            {"role": "user", "content": PROMPT_TEMPLATE.format(user_text=user_text)},
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(GROQ_CHAT_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200:
        raise RuntimeError(f"Groq API error: {response.text}")

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return json.dumps(data)


# ----------------------------
# Core Mood Analyzer
# ----------------------------
def analyze_mood(text: str) -> Tuple[str, float, str]:
    try:
        model_output = call_groq_chat(text)
    except Exception as e:
        return "Neutral", 0.0, f"Error contacting Groq API: {e}"

    parsed = extract_json_from_text(model_output)

    allowed = {"Happy","Sad","Angry","Stressed","Neutral","Surprised","Fearful","Disgusted"}

    mood = parsed.get("mood", "Neutral").title()
    if mood not in allowed:
        mood = "Neutral"

    confidence = parsed.get("confidence")
    if not isinstance(confidence, (float, int)):
        confidence = 0.5

    explanation = parsed.get("explanation", f"Classified as {mood}.").strip()

    return mood, float(confidence), explanation


# ----------------------------
# Gradio Interface Wrapper
# ----------------------------
def gradio_predict(text: str):
    mood, confidence, explanation = analyze_mood(text)
    return mood, f"{confidence:.3f}", explanation


# ----------------------------
# Build the Gradio App
# ----------------------------
def build_ui():
    with gr.Blocks(title="AI Mood Analyzer (Groq)") as demo:
        gr.Markdown("# **AI Mood Analyzer — By Hassaan Ahmed Khan**")
        gr.Markdown("Enter a message and the model will detect the mood.")

        inp = gr.Textbox(
            lines=4,
            label="Input Text",
            placeholder="Type how you're feeling or paste a message..."
        )

        out_mood = gr.Textbox(label="Predicted Mood", interactive=False)
        out_conf = gr.Textbox(label="Confidence", interactive=False)
        out_expl = gr.Textbox(label="Explanation", interactive=False)

        btn = gr.Button("Analyze Mood")
        btn.click(gradio_predict, inputs=inp, outputs=[out_mood, out_conf, out_expl])

    return demo


# ----------------------------
# Launch
# ----------------------------
if __name__ == "__main__":
    demo = build_ui()
    demo.launch()
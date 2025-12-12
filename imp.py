import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Email Tone Checker", page_icon="📧", layout="wide")

# -------------------------
# Sidebar Settings
# -------------------------
st.sidebar.title("Settings")
model_choice = st.sidebar.selectbox("Choose Model", ["phi3"])
show_sentiment = st.sidebar.checkbox("Show Sentiment Analysis", True)
show_rewrite = st.sidebar.checkbox("Show Polite Rewrite", True)
show_score = st.sidebar.checkbox("Show Professionalism Score", True)

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
    <style>
        .main-title {text-align: center; font-size: 40px; font-weight: 700; color: #4A4A4A; padding: 10px 0;}
        .sub-heading {font-size: 22px; margin-top: 25px; font-weight: 600; color: #333333;}
        .result-card {background: #ffffff; padding: 20px; border-radius: 12px; margin-top: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.10);}
        .sentiment-badge {padding: 6px 14px; border-radius: 20px; font-weight: 600; color: white; display: inline-block; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📧 Email Tone Checker</h1>", unsafe_allow_html=True)

# -------------------------
# Input Email
# -------------------------
email_text = st.text_area("Paste your email here:", height=200, placeholder="Type your email...")

# -------------------------
# Sentiment Analyzer
# -------------------------
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# -------------------------
# Ollama API
# -------------------------
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_choice, "prompt": prompt, "stream": False},
            timeout=60
        )
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    return "".join([c.get("response", "") for c in data])
                return data.get("response", "No response found")
            except:
                return response.text
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Ollama not running ({e})"

# -------------------------
# Analyze Button
# -------------------------
if st.button("Analyze Email"):

    if email_text.strip() == "":
        st.warning("Please enter your email first.")
    else:
        # --------------------- Sentiment ---------------------
        if show_sentiment:
            st.markdown("<div class='sub-heading'>🔍 Sentiment Analysis</div>", unsafe_allow_html=True)

            scores = analyze_sentiment(email_text)
            compound = scores.get("compound", 0)

            sentiment = "Neutral"
            color = "gray"
            emoji = "😐"

            if compound > 0.05:
                sentiment = "Positive"
                color = "#22c55e"
                emoji = "😃"
            elif compound < -0.05:
                sentiment = "Negative"
                color = "#ef4444"
                emoji = "😡"

            st.markdown(
                f"<div class='sentiment-badge' style='background:{color}'>{emoji} {sentiment}</div>",
                unsafe_allow_html=True
            )

            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.json(scores)
            st.markdown("</div>", unsafe_allow_html=True)

        # --------------------- Polite Rewrite ---------------------
        if show_rewrite:
            st.markdown("<div class='sub-heading'>🧑‍💼 Polite Rewrite</div>", unsafe_allow_html=True)

            polite_text = ask_ollama(
                f"Rewrite this email in a polite, professional, and concise tone:\n\n{email_text}"
            )

            # Side by side layout
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Email")
                st.text_area("Original", email_text, height=200)
            with col2:
                st.subheader("Polite Rewrite")
                st.text_area("Rewrite", polite_text, height=200)

            # download button
            st.download_button(
                "Download Polite Email",
                data=polite_text,
                file_name="polite_email.txt"
            )

        # --------------------- Professionalism Score ---------------------
        if show_score:
            st.markdown("<div class='sub-heading'>📊 Professionalism Score</div>", unsafe_allow_html=True)

            score_prompt = (
                "Rate the professionalism of this email from 0 to 100.\n"
                "0 = rude, 100 = highly professional.\n\nEmail:\n"
                + email_text +
                "\nReturn only the number."
            )

            score_response = ask_ollama(score_prompt)

            match = re.search(r'\d+', score_response)
            score_value = int(match.group()) if match else 50

            # Color
            score_color = "#22c55e" if score_value >= 75 else "#f97316" if score_value >= 50 else "#ef4444"

            st.markdown(
                f"<div class='result-card' style='border-left: 6px solid {score_color}; padding-left: 10px;'>",
                unsafe_allow_html=True
            )
            st.metric("Professionalism Score", f"{score_value}/100")
            st.markdown("</div>", unsafe_allow_html=True)

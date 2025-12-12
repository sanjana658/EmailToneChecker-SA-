Sentiment Analysis

The tool evaluates your email using VADER sentiment analysis and breaks it down into positive, negative, and neutral scores. It also shows a compound score, which represents the overall tone of the message. This helps you understand how your email “comes across” emotionally.

Polite Rewrite

Using the Phi-3 model, your email is rewritten into a more refined, constructive, and respectful version. The goal isn’t to change your message — just to present it more professionally. This is especially useful when dealing with sensitive topics, complaints, or formal communication.

Professionalism Score

The AI rates your email from 0 to 100 based on politeness, clarity, and professional tone. This simple score instantly tells you whether your email is ready to send or needs a bit more refinement.

The UI is developed using Streamlit, offering a clean, friendly interface with toggle options, side-by-side comparisons, and download support for the rewritten email.

Overall, this project is built to help anyone communicate more effectively and confidently. It’s practical, easy to use, and entirely offline — a small tool that makes a big difference in everyday communication.

How to Run

-Install dependencies using pip install -r requirements.txt

-Make sure Ollama is installed and running with the command:

-ollama run phi3


-Start the app:

-streamlit run app.py


The Email Tone Checker will open in your browser automatically.

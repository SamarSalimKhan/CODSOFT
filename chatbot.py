# chatbot.py
"""
Simple rule-based chatbot for CodSoft AI Internship (Task 1)
Run: python chatbot.py
Designed for terminal / console usage (VS Code integrated terminal)
"""

import re
import json
from datetime import datetime

# --- Intent patterns and responses (extend as needed) ---
INTENTS = [
    {
        "name": "greeting",
        "patterns": [r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\bgood (morning|afternoon|evening)\b"],
        "responses": ["Hello! How can I help you today?", "Hi there! What would you like to know?"]
    },
    {
        "name": "ask_about_task",
        "patterns": [r"\btask\b", r"\bassign(ment|ment)?\b", r"\bwhat.*(task|project)\b", r"\bai task\b"],
        "responses": [
            "This internship requires completing at least 3 AI tasks: Chatbot, Tic-Tac-Toe AI, and Image Captioning.",
            "You can complete Rule-based Chatbot, Tic-Tac-Toe AI, and Image Captioning as suggested in the PDF."
        ]
    },
    {
        "name": "ask_submission",
        "patterns": [r"\bsubmit\b", r"\bsubmission\b", r"\bform\b", r"\bhow to submit\b"],
        "responses": [
          "You will be asked to share your GitHub repo link and a demo video in the submission form shared via email.",
          "Make sure your repo is named CODSOFT and include each task in a separate folder with README and demo video link."
        ]
    },
    {
        "name": "thanks",
        "patterns": [r"\bthanks\b", r"\bthank you\b", r"\bthx\b"],
        "responses": ["You're welcome! Happy to help.", "No problem — good luck with the internship!"]
    },
    {
        "name": "goodbye",
        "patterns": [r"\bbye\b", r"\bgoodbye\b", r"\bsee you\b", r"\blater\b"],
        "responses": ["Goodbye! All the best.", "See you — feel free to message if you need more help."]
    },
    {
        "name": "help",
        "patterns": [r"\bhelp\b", r"\bhow to\b", r"\bwhat to do\b"],
        "responses": [
            "Tell me what you need — code help, GitHub setup, or how to make the demo video?",
            "I can guide you step-by-step: which task do you want to start with?"
        ]
    }
]

FALLBACK_RESPONSES = [
    "Sorry, I didn't get that. Can you rephrase?",
    "I am not sure about that. Ask me about tasks, submission, or GitHub setup."
]

# --- Utility functions ---
def match_intent(message):
    message = message.lower()
    for intent in INTENTS:
        for pat in intent["patterns"]:
            if re.search(pat, message):
                return intent
    return None

def get_response(intent):
    import random
    if intent is None:
        return random.choice(FALLBACK_RESPONSES)
    return random.choice(intent["responses"])

# --- Conversation logging ---
LOGFILE = "chat_logs.jsonl"

def log_message(user_msg, bot_msg):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": user_msg,
        "bot": bot_msg
    }
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# --- Main chat loop ---
def main():
    print("CodSoft AI - Rule-based Chatbot (Task 1)")
    print("Type 'exit' or 'quit' to end the chat. Type 'help' for guidance.")
    while True:
        try:
            user_msg = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        if not user_msg:
            print("Bot: Please type something.")
            continue

        if user_msg.lower() in ("exit", "quit"):
            print("Bot: Goodbye! Good luck with your internship.")
            log_message(user_msg, "Goodbye! Good luck with your internship.")
            break

        intent = match_intent(user_msg)
        bot_msg = get_response(intent)
        print("Bot:", bot_msg)
        log_message(user_msg, bot_msg)

if __name__ == "__main__":
    main()
    
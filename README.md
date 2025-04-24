# 💊 MedLens: AI-Powered Accessible Medication Consultant

A software project submitted to HopHacks 2023. 

**MedLens** is an AI-powered mobile application that helps users—especially those with visual impairments—safely understand and take their medications. Built as a submission for **HopHacks 2023**, MedLens leverages OCR and generative AI to transform complex, densely packed drug label information into clear, accessible, and actionable guidance.

---

## 🔍 Problem

Medication packaging often features **small, dense, and hard-to-read print**. For visually impaired individuals or elderly users, this poses a major challenge, leading to misuse or underuse of critical medications. MedLens solves this by:
- Scanning and understanding printed medication instructions.
- Providing accessible summaries and actionable guidance using AI.

---

## 🧠 Key Features

- 📷 **OCR Integration**  
  Capture and read text from medication bottles, labels, or instruction leaflets using your phone's camera.

- 🤖 **Generative AI Assistant**  
  Leverages ChatGPT to explain medication details in a **clear, simplified**, and **personalized** way.

- 🗣 **Voice Output & Large Text UI**  
  Offers both text and voice-based responses for better accessibility.

- 🛠 **Real-time Performance**  
  Built with asynchronous programming to handle API calls without blocking UI responsiveness.

---

## 🏗 Tech Stack

- **Backend**: Python, Flask, asyncio
- **AI**: OpenAI's ChatGPT API for natural language understanding and generation
- **OCR**: Tesseract OCR (or mobile-native libraries)
- **Frontend**: Mobile app (React Native or similar)
- **Database**: Supabase (for session and audio file storage)

---

## 📦 How It Works

1. **Scan** a medication label using the in-app camera.
2. **OCR** extracts the raw text from the image.
3. **ChatGPT API** processes the text and generates an accessible explanation.
4. **User receives** instructions in readable text and synthesized voice.


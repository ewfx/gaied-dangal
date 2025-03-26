# 🚀 Gen AI-Based Email Classification and OCR

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Problem Statement - Commercial Bank Lending service teams receive a significant volume of service requests through emails. These emails contain diverse requests, often with attachments and will be ingested to the loan servicing platform and creates service requests which will go through the workflow processing. Incoming service requests (SR) via email require a manual triage process with "Gatekeeper".

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
This challange is to automate email classification and data extraction using Generative AI (LLMs) and eliminate the manual triage process with "Gatekeeper".

## ⚙️ What It Does
Functionalities of your project.
1. Read all the emails (.eml format) from any folder (configurable).
2. Process the email body and attachments (.pdf, .doc, .jpg formats) and extract the content.
3. Pass the email content as a prompt to different Gen AI LLM models like GPT, LLaMA, Gemini (configurable).
4. AI model will analyze the email content and identify the request & sub request type, duplicate or not, confidence score, etc.
![_- visual selection](https://github.com/user-attachments/assets/8e3fa8f1-6d8d-438e-9bb7-29483d7e3d84)


## 🛠️ How We Built It
Technologies, frameworks, and tools used in development.
1. React & Node JS for UI development
2. Python Fast API for Rest API development
3. UVICon as Web Server to receive request from UI clients & send response to it.
4. Gen AI LLMs – LLaMA, GPT, Gemini for email classification and data extraction 
5. Python Libraries – PyMuPDF, docx, pytesseract, Imgage, BytesParser, policy to process PDF, DOC & Image attachments

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/gaied-dangal.git
   ```
2. Install dependencies  
   ```sh
   npm install (for React)
   pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start (for UI)
   python app.py (for Backend)
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React & Node.js
- 🔹 Backend:  Python, FastAPI & UVICon
- 🔹 Gen AI LLMs: LLaMA, GPT & Gemini

## 👥 Team Dangal
- **Madan Mohan** - [LinkedIn](#)
- **Sakshi** - [LinkedIn](#)
- **Prasanna** - [LinkedIn](#)
- **Tanuja** - [LinkedIn](#)
- **Rajendhar** - [LinkedIn](#)

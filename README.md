# recipe-generator-web

AI Recipe Generator
=====================

This repository is a simple project that utilizes both locally hosted LLMs and OpenAI GPT to generate recipes. This project is far from being complete.

## Features
- Uses AnythingLLM scrap online store 
- Uses AnythingLLM RAG to use grocery items data from scraped online store
- OCR scanning receipts using opencv and pytesseract and use GPT 3.5 to convert raw text into JSON
- Generate recipes (with macros, cost etc) using GPT or Llama

## TODO
- Monitor inflation
- Save past requests/prompts
- Improve tranform on creased paper (so can scan using camera)
- Fix cost calculation for non-GPT models
- Considering fine-tuning for better output

## Requirements
- Powerful enough PC to run Llama3-8b Q4
- AnythingLLM
- Ollama/LMStudio
- PostgreSQL database
- OpenAI api key

## Example
![Screenshot 2024-10-19 000534](https://github.com/user-attachments/assets/cd4c95e3-360d-43ad-b136-91d9fca59c93)


![Screenshot 2024-10-18 214843](https://github.com/user-attachments/assets/44591337-4b50-4580-adf6-94dafb1619f1)



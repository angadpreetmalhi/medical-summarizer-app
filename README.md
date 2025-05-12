# 🩺 Medical Report Summarizer & Explorer

## 📌 Overview
**Medical Report Summarizer & Explorer** is a Streamlit-based web app designed to help healthcare professionals, researchers, and students interactively explore and summarize medical case reports.

It supports both **dataset search** and **user-uploaded medical reports (TXT/PDF)** for instant summarization and named entity recognition.

---

## 💡 Features

- ✅ **Upload Medical Reports**: Accepts `.txt` or `.pdf` files and extracts key summaries.
- 🔍 **Search Dataset**: Filter over 4,000+ pre-labeled medical summaries by:
  - Medical specialty (e.g., Cardiology, Orthopedic)
  - Named entities (e.g., medications, diagnoses, symptoms)
  - Full-text keyword matches
- 📊 **Top Entities Visualization**: Displays the most frequent terms from filtered results.
- 📥 **Download Results**: Save selected records to CSV for further use.

---

## 🧠 Use Cases

| User Type        | Benefit |
|------------------|---------|
| **Doctors**       | Quickly summarize and review lengthy reports. |
| **Medical Researchers** | Identify trends and focus areas across specialties. |
| **Health Data Analysts** | Perform entity-based search across thousands of records. |
| **Medical Students** | Study real-world summaries from various medical fields. |

---

## 🚀 Technologies Used

- **Python**, **Streamlit** – UI and app logic
- **spaCy** – Named Entity Recognition
- **Transformers (HuggingFace)** – BART model for text summarization
- **pandas, seaborn, matplotlib** – Data handling and visualizations

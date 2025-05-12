import streamlit as st
import pandas as pd
import ast
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
from transformers import pipeline

# Load summarizer and spaCy model (assumes both are available)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
nlp = spacy.load("en_core_web_sm")  # ✅ Make sure it's installed via requirements.txt

# Sidebar upload
st.sidebar.header("📤 Upload Your Own Report")
uploaded_file = st.sidebar.file_uploader("Upload a medical report (.txt)", type=["txt"])

# Title
st.title("🩺 Medical Report Search & Explorer")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mtsamples_with_entities.csv")  # ✅ Make sure this file is uploaded to GitHub
    df['entities'] = df['entities'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    return df

df = load_data()

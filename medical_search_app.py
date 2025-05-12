import streamlit as st
import pandas as pd
import ast
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/mtsamples_with_entities.csv")
    df['entities'] = df['entities'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    return df

df = load_data()

st.title("🩺 Medical Report Search & Explorer")

# Filter by medical specialty
specialties = sorted(df['medical_specialty'].dropna().unique())
selected_specialty = st.selectbox("🔬 Filter by Medical Specialty:", ["All"] + specialties)

if selected_specialty != "All":
    df = df[df['medical_specialty'] == selected_specialty]

# Search mode
search_mode = st.radio("🔎 Search in:", ["Named Entities", "Full Summary Text"])
query = st.text_input("Enter keyword to search:")

# Filter logic
if query:
    keyword = query.lower()
    if search_mode == "Named Entities":
        filtered_df = df[df['entities'].apply(lambda ents: any(keyword in e.lower() for e in ents))]
    else:
        filtered_df = df[df['summary'].str.lower().str.contains(keyword)]
else:
    filtered_df = df

# Show results
st.write(f"### 📋 Found {len(filtered_df)} matching records")
st.dataframe(filtered_df[['medical_specialty', 'summary', 'entities']])

# Download button
st.download_button(
    label="📥 Download Results as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_medical_summaries.csv',
    mime='text/csv'
)

# Top entities chart
if not filtered_df.empty:
    all_ents = [e.lower() for row in filtered_df['entities'] for e in row]
    top_ents = Counter(all_ents).most_common(10)
    if top_ents:
        ents_df = pd.DataFrame(top_ents, columns=['Entity', 'Frequency'])

        st.write("### 📊 Top Entities in Results")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=ents_df, x='Frequency', y='Entity', palette='crest', ax=ax)
        st.pyplot(fig)

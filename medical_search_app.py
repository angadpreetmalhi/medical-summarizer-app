import streamlit as st
    df = pd.read_csv("mtsamples_with_entities.csv")
    df['entities'] = df['entities'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
    return df

df = load_data()

# If user uploads a report
if uploaded_file is not None:
    report_text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Original Report")
    st.write(report_text)

    # Summarize the report
    st.subheader("📝 Summary")
    summary_result = summarizer(report_text[:1000], max_length=130, min_length=30, do_sample=False)
    st.write(summary_result[0]['summary_text'])

    # Extract entities
    st.subheader("🔍 Named Entities")
    doc = nlp(report_text)
    entities = [ent.text for ent in doc.ents]
    st.write(entities)

else:
    # Search interface for dataset
    specialties = sorted(df['medical_specialty'].dropna().unique())
    selected_specialty = st.selectbox("🔬 Filter by Medical Specialty:", ["All"] + specialties)

    if selected_specialty != "All":
        df = df[df['medical_specialty'] == selected_specialty]

    search_mode = st.radio("🔎 Search in:", ["Named Entities", "Full Summary Text"])
    query = st.text_input("Enter keyword to search:")

    if query:
        keyword = query.lower()
        if search_mode == "Named Entities":
            filtered_df = df[df['entities'].apply(lambda ents: any(keyword in e.lower() for e in ents))]
        else:
            filtered_df = df[df['summary'].str.lower().str.contains(keyword)]
    else:
        filtered_df = df

    st.write(f"### 📋 Found {len(filtered_df)} matching records")
    st.dataframe(filtered_df[['medical_specialty', 'summary', 'entities']])

    st.download_button(
        label="📥 Download Results as CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='filtered_medical_summaries.csv',
        mime='text/csv'
    )

    if not filtered_df.empty:
        all_ents = [e.lower() for row in filtered_df['entities'] for e in row]
        top_ents = Counter(all_ents).most_common(10)
        if top_ents:
            ents_df = pd.DataFrame(top_ents, columns=['Entity', 'Frequency'])

            st.write("### 📊 Top Entities in Results")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=ents_df, x='Frequency', y='Entity', palette='crest', ax=ax)
            st.pyplot(fig)

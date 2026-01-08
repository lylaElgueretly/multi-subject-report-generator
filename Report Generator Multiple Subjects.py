# =========================================
# ENGLISH & SCIENCE REPORT COMMENT GENERATOR
# Streamlit Version for Years 7 & 8
# =========================================

import random
import streamlit as st
from docx import Document

TARGET_CHARS = 499  # target character count including spaces

# ---------- IMPORT ALL STATEMENTS ----------
from statements_year7_english import opening_phrases as opening_7_eng, attitude_bank as attitude_7_eng, reading_bank as reading_7_eng, reading_target_bank as target_7_eng, closer_bank as closer_7_eng
from statements_year8_english import opening_phrases as opening_8_eng, attitude_bank as attitude_8_eng, reading_bank as reading_8_eng, reading_target_bank as target_8_eng, closer_bank as closer_8_eng
from statements_year7_science import opening_phrases as opening_7_sci, attitude_bank as attitude_7_sci, science_bank as science_7_sci, target_bank as target_7_sci, closer_bank as closer_7_sci
from statements_year8_science import opening_phrases as opening_8_sci, attitude_bank as attitude_8_sci, science_bank as science_8_sci, target_bank as target_8_sci, closer_bank as closer_8_sci

# ---------- HELPERS ----------
def get_pronouns(gender):
    gender = gender.lower()
    if gender == "male":
        return "he", "his"
    elif gender == "female":
        return "she", "her"
    return "they", "their"

def lowercase_first(text):
    return text[0].lower() + text[1:] if text else ""

def truncate_comment(comment, target=TARGET_CHARS):
    if len(comment) <= target:
        return comment
    truncated = comment[:target].rstrip(" ,;.")
    if "." in truncated:
        truncated = truncated[:truncated.rfind(".")+1]
    return truncated

# ---------- GENERATE COMMENT FUNCTION ----------
def generate_comment(name, gender, year, subject, att, achieve, target, attitude_target=None):
    p, p_poss = get_pronouns(gender)

    # Select the right banks based on year and subject
    if year == "Year 7" and subject == "English":
        opening, attitude_b, achievement_b, target_b, closer_b = (
            opening_7_eng, attitude_7_eng, reading_7_eng, target_7_eng, closer_7_eng
        )
    elif year == "Year 8" and subject == "English":
        opening, attitude_b, achievement_b, target_b, closer_b = (
            opening_8_eng, attitude_8_eng, reading_8_eng, target_8_eng, closer_8_eng
        )
    elif year == "Year 7" and subject == "Science":
        opening, attitude_b, achievement_b, target_b, closer_b = (
            opening_7_sci, attitude_7_sci, science_7_sci, target_7_sci, closer_7_sci
        )
    elif year == "Year 8" and subject == "Science":
        opening, attitude_b, achievement_b, target_b, closer_b = (
            opening_8_sci, attitude_8_sci, science_8_sci, target_8_sci, closer_8_sci
        )
    else:
        raise ValueError("Year/Subject combination not found")

    opening_phrase = random.choice(opening)
    attitude_sentence = f"{opening_phrase} {name} {attitude_b[att]}."
    achievement_sentence = f"{p.capitalize()} {achievement_b[achieve]}."
    target_sentence = f"For the next term, {p} should {lowercase_first(target_b[target])}."
    attitude_target_sentence = f" {lowercase_first(attitude_target)}" if attitude_target else ""
    closer_sentence = random.choice(closer_b)

    comment_parts = [
        attitude_sentence + attitude_target_sentence,
        achievement_sentence,
        target_sentence,
        closer_sentence
    ]

    comment = " ".join(comment_parts)
    return truncate_comment(comment, TARGET_CHARS)

# ---------- STREAMLIT APP ----------
st.title("English & Science Report Comment Generator (~499 chars)")

st.markdown(
    "Fill in the student details and click **Generate Comment**. You can add multiple students before downloading the full report."
)

if 'all_comments' not in st.session_state:
    st.session_state['all_comments'] = []

# ---------- FORM ----------
with st.form("report_form"):
    name = st.text_input("Student Name")
    gender = st.selectbox("Gender", ["Male", "Female"])
    year = st.selectbox("Year", ["Year 7", "Year 8"])
    subject = st.selectbox("Subject", ["English", "Science"])

    # Band options
    band_options = [90,85,80,75,70,65,60,55,40,0]
    att = st.selectbox("Attitude band", band_options)
    achieve = st.selectbox("Achievement band", band_options)
    target = st.selectbox("Next term target band", band_options)

    attitude_target = st.text_input("Optional Attitude Next Steps")

    submitted = st.form_submit_button("Generate Comment")

# ---------- GENERATE COMMENT ----------
if submitted and name:
    comment = generate_comment(name, gender, year, subject, att, achieve, target, attitude_target)
    char_count = len(comment)

    st.text_area("Generated Comment", comment, height=200)
    st.write(f"Character count (including spaces): {char_count} / {TARGET_CHARS}")

    st.session_state['all_comments'].append(f"{name} ({year} {subject}): {comment}")

    if st.button("Add Another Comment"):
        st.experimental_rerun()

# ---------- DOWNLOAD FULL REPORT ----------
if st.session_state['all_comments']:
    if st.button("Download Full Report (Word)"):
        doc = Document()
        for c in st.session_state['all_comments']:
            doc.add_paragraph(c)
        file_name = "Report_Comments.docx"
        doc.save(file_name)
        with open(file_name, "rb") as f:
            st.download_button(
                label="Download Word File",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# ---------- SHOW ALL COMMENTS ----------
if st.session_state['all_comments']:
    st.markdown("### All Generated Comments:")
    for c in st.session_state['all_comments']:
        st.write(c)
# Write your code here :-)

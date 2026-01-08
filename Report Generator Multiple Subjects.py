# =========================================
# MULTI-SUBJECT REPORT COMMENT GENERATOR - Streamlit Version
# Supports English and Science, Years 7 & 8
# =========================================

import random
import streamlit as st
from docx import Document

TARGET_CHARS = 499  # target character count including spaces

# ---------- IMPORT STATEMENTS ----------
# Make sure filenames match exactly your uploaded files
from statements_year7_English import (
    opening_phrases as opening_7_eng,
    attitude_bank as attitude_7_eng,
    reading_bank as reading_7_eng,
    writing_bank as writing_7_eng,
    reading_target_bank as target_7_eng,
    writing_target_bank as target_write_7_eng,
    closer_bank as closer_7_eng
)

from statements_year8_English import (
    opening_phrases as opening_8_eng,
    attitude_bank as attitude_8_eng,
    reading_bank as reading_8_eng,
    writing_bank as writing_8_eng,
    reading_target_bank as target_8_eng,
    writing_target_bank as target_write_8_eng,
    closer_bank as closer_8_eng
)

from statements_year7_science import (
    opening_phrases as opening_7_sci,
    attitude_bank as attitude_7_sci,
    science_bank as science_7_sci,
    target_bank as target_7_sci,
    closer_bank as closer_7_sci
)

from statements_year8_science import (
    opening_phrases as opening_8_sci,
    attitude_bank as attitude_8_sci,
    science_bank as science_8_sci,
    target_bank as target_8_sci,
    closer_bank as closer_8_sci
)

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

def generate_comment(subject, year, name, gender, att, achieve, target, pronouns, attitude_target=None):
    p, p_poss = pronouns

    # Choose the correct banks
    if subject == "English":
        if year == 7:
            opening = random.choice(opening_7_eng)
            attitude_sentence = f"{opening} {name} {attitude_7_eng[att]}."
            reading_sentence = f"In reading, {p} {reading_7_eng[achieve]}."
            writing_sentence = f"In writing, {p} {writing_7_eng[achieve]}."
            reading_target_sentence = f"For the next term, {p} should {lowercase_first(target_7_eng[target])}."
            writing_target_sentence = f"Additionally, {p} should {lowercase_first(target_write_7_eng[target])}."
            closer_sentence = random.choice(closer_7_eng)
        else:  # Year 8
            opening = random.choice(opening_8_eng)
            attitude_sentence = f"{opening} {name} {attitude_8_eng[att]}."
            reading_sentence = f"In reading, {p} {reading_8_eng[achieve]}."
            writing_sentence = f"In writing, {p} {writing_8_eng[achieve]}."
            reading_target_sentence = f"For the next term, {p} should {lowercase_first(target_8_eng[target])}."
            writing_target_sentence = f"Additionally, {p} should {lowercase_first(target_write_8_eng[target])}."
            closer_sentence = random.choice(closer_8_eng)

    else:  # Science
        if year == 7:
            opening = random.choice(opening_7_sci)
            attitude_sentence = f"{opening} {name} {attitude_7_sci[att]}."
            reading_sentence = f"{p} {science_7_sci[achieve]}."
            reading_target_sentence = f"For the next term, {p} should {lowercase_first(target_7_sci[target])}."
            writing_target_sentence = ""  # Not used for science
            closer_sentence = random.choice(closer_7_sci)
            writing_sentence = ""  # Not used for science
        else:  # Year 8
            opening = random.choice(opening_8_sci)
            attitude_sentence = f"{opening} {name} {attitude_8_sci[att]}."
            reading_sentence = f"{p} {science_8_sci[achieve]}."
            reading_target_sentence = f"For the next term, {p} should {lowercase_first(target_8_sci[target])}."
            writing_target_sentence = ""  # Not used for science
            closer_sentence = random.choice(closer_8_sci)
            writing_sentence = ""  # Not used for science

    # optional attitude target
    attitude_target_sentence = f" {lowercase_first(attitude_target)}" if attitude_target else ""

    comment_parts = [
        attitude_sentence + attitude_target_sentence,
        reading_sentence,
        writing_sentence,
        reading_target_sentence,
        writing_target_sentence,
        closer_sentence
    ]

    comment = " ".join([c for c in comment_parts if c])  # remove empty strings
    comment = truncate_comment(comment, TARGET_CHARS)
    return comment

# ---------- STREAMLIT APP ----------
st.title("Multi-Subject Report Comment Generator (~499 chars)")

st.markdown(
    "Select subject, year, fill in the student details, and click **Generate Comment**. You can add multiple students before downloading the full report."
)

if 'all_comments' not in st.session_state:
    st.session_state['all_comments'] = []

with st.form("report_form"):
    subject = st.selectbox("Subject", ["English", "Science"])
    year = st.selectbox("Year", [7, 8])
    name = st.text_input("Student Name")
    gender = st.selectbox("Gender", ["Male", "Female"])
    att = st.selectbox("Attitude band", [90,85,80,75,70,65,60,55,40])
    achieve = st.selectbox("Achievement band", [90,85,80,75,70,65,60,55,40])
    target = st.selectbox("Target band", [90,85,80,75,70,65,60,55,40])
    
    # optional attitude next steps
    attitude_target = st.text_input("Optional Attitude Next Steps")

    submitted = st.form_submit_button("Generate Comment")

if submitted and name:
    pronouns = get_pronouns(gender)
    comment = generate_comment(subject, year, name, gender, att, achieve, target, pronouns, attitude_target)
    char_count = len(comment)

    st.text_area("Generated Comment", comment, height=200)
    st.write(f"Character count (including spaces): {char_count} / {TARGET_CHARS}")

    st.session_state['all_comments'].append(f"{name}: {comment}")

    if st.button("Add Another Comment"):
        st.experimental_rerun()

# ---------- DOWNLOAD FULL REPORT ----------
if st.session_state['all_comments']:
    if st.button("Download Full Report (Word)"):
        doc = Document()
        for c in st.session_state['all_comments']:
            doc.add_paragraph(c)
        file_name = "Multi_Subject_Report_Comments.docx"
        doc.save(file_name)
        with open(file_name, "rb") as f:
            st.download_button(
                label="Download Word File",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# ---------- SHOW ALL COMMENTS SO FAR ----------
if st.session_state['all_comments']:
    st.markdown("### All Generated Comments:")
    for c in st.session_state['all_comments']:
        st.write(c)

import streamlit as st
import requests

st.set_page_config(page_title="AI Image Agent", layout="centered")

st.title("🎨 AI Text-to-Image Agent")
st.write("Generate and edit AI image prompts")

# Generate section
st.subheader("Generate Image")

user_input = st.text_input("Enter your idea (e.g. car, house, bike)")

if st.button("Generate"):
    if user_input:
        res = requests.post(
            "http://localhost:8000/generate",
            params={"user_input": user_input}
        )
        data = res.json()

        st.success("Generated Prompt:")
        st.write(data["prompt"])

        st.image(data["image"])

# Edit section
st.subheader("Edit Image")

edit_input = st.text_input("Modify previous image (e.g. sunset lighting)")

if st.button("Edit"):
    if edit_input:
        res = requests.post(
            "http://localhost:8000/edit",
            params={"edit_text": edit_input}
        )
        data = res.json()

        st.success("Updated Prompt:")
        st.write(data["prompt"])

        st.image(data["image"])
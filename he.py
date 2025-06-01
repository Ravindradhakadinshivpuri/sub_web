import streamlit as st
from note_utils import save_note, load_note
from PIL import Image, ImageEnhance
import requests
import json
from deep_translator import GoogleTranslator

st.set_page_config(page_title="📓 Text Notepad & Learning Tool", layout="wide")

st.title(":notebook_with_decorative_cover: Text Notepad & Learning Tool")

# Log visitor IP (for admin)
def log_visitor():
    try:
        ip = requests.get('https://api.ipify.org').text
        user_agent = st.session_state.get("user_agent", "Unknown")
        entry = {"ip": ip, "user_agent": user_agent}
        with open("visitors.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass

log_visitor()

# Sidebar as buttons
with st.sidebar:
    st.markdown("## 📂 Menu")
    section = st.radio("Go to", [
        "✏️ Notepad", 
        "📚 Learning Line", 
        "🌐 Best Websites", 
        "📦 More Tools", 
        "🅳️ English Translator",
    ])

# ---- Notepad ----
if section == "✏️ Notepad":
    st.subheader("📝 Write and Save Your Notes")
    note_text = st.text_area("Your notes:", height=300, value=load_note())
    if st.button("📏 Save Note"):
        save_note(note_text)
        st.success("Note saved successfully!")

# ---- Learning Line ----
elif section == "📚 Learning Line":
    st.subheader("💡 Type a Line to Learn")
    learning_input = st.text_input("Type something you're learning (e.g., quote, word, line of code)")
    if learning_input:
        st.markdown(f"**You typed:** `{learning_input}`")
        st.success("Keep practicing this line!")

# ---- Best Websites ----
elif section == "🌐 Best Websites":
    st.subheader("🌍 Best Free Learning Websites")
    st.markdown("""
    - [Khan Academy](https://www.khanacademy.org/)
    - [freeCodeCamp](https://www.freecodecamp.org/)
    - [Coursera](https://www.coursera.org/)
    - [edX](https://www.edx.org/)
    - [Codecademy](https://www.codecademy.com/)
    - [GeeksforGeeks](https://www.geeksforgeeks.org/)
    - [W3Schools](https://www.w3schools.com/)
    - [Duolingo](https://www.duolingo.com/)
    """)

# ---- More Tools ----
elif section == "📦 More Tools":
    st.subheader("🧰 More Tools")
    tool = st.selectbox("Select a Tool", ["Upload & Edit Image", "Mini Terminal", "My Info"])

    if tool == "Upload & Edit Image":
        st.markdown("### Upload an Image")
        image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if image_file:
            image = Image.open(image_file)
            st.image(image, caption="Original Image", use_column_width=True)
            if st.checkbox("Grayscale"):
                image = image.convert("L")
            if st.checkbox("Enhance Sharpness"):
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(2.0)
            st.image(image, caption="Edited Image", use_column_width=True)

    elif tool == "Mini Terminal":
        st.markdown("### 🧪 Try Python Code")
        code_input = st.text_area("Type Python code to run (safe code only!)")
        if st.button("▶️ Run Code"):
            try:
                local_vars = {}
                exec(code_input, {}, local_vars)
                st.success("Code executed successfully!")
                if local_vars:
                    st.write("💾 Output:")
                    st.write(local_vars)
            except Exception as e:
                st.error(f"Error: {e}")

    elif tool == "My Info":
        st.markdown("### 🙋 Enter Your Info")
        name = st.text_input("Your Name")
        bio = st.text_area("About You")
        photo = st.file_uploader("Upload Your Photo", type=["jpg", "jpeg", "png"])
        if name and bio:
            st.markdown(f"#### 👤 Hello, {name}!")
            st.markdown(f"> {bio}")
        if photo:
            image = Image.open(photo)
            st.image(image, caption="🖼️ Your Photo (Preview)", use_column_width=True)

# ---- English/Hindi Translator ----
elif section == "🅳️ English Translator":
    st.subheader("Translate Hindi ↔ English")
    text = st.text_area("Enter text to translate")
    if st.button("Translate"):
        if text:
            try:
                if any("\u0900" <= char <= "\u097F" for char in text):
                    translated = GoogleTranslator(source='auto', target='en').translate(text)
                    st.markdown(f"**English:** {translated}")
                else:
                    translated = GoogleTranslator(source='auto', target='hi').translate(text)
                    st.markdown(f"**Hindi:** {translated}")
            except Exception as e:
                st.error(f"Translation failed: {e}")
  
 
import streamlit as st
from openai import OpenAI
from pathlib import Path
from datetime import date

# ============================================================
# Learnora AI - Version 1.0
# See. Learn. Discover.
# ============================================================

st.set_page_config(
    page_title="Learnora AI",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_NAME = "Learnora AI"
TAGLINE = "See. Learn. Discover."

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "assets" / "images"
VIDEO_DIR = BASE_DIR / "assets" / "videos"


def get_ai_client():
    """Create the OpenAI client if a Streamlit secret is configured."""
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def build_learning_prompt(age_group, level, subject, topic, goal):
    return f"""
You are Learnora AI, a friendly educational tutor for children.

Learner age group: {age_group}
Learning level: {level}
Subject: {subject}
Topic: {topic}
Learning goal: {goal}

Create a safe, age-appropriate lesson.

Requirements:
- Use simple, encouraging language.
- Explain the concept clearly.
- Break difficult ideas into small steps.
- Include one relatable real-world example.
- Avoid frightening, mature, or inappropriate content.
- Do not ask for personal information.
- End with 5 short multiple-choice quiz questions.
- Do not provide answers immediately after each question.

Use these headings:
# Lesson
## What is it?
## Simple Explanation
## Step-by-Step
## Real-World Example
## Remember This
## Quick Quiz
"""


def ask_ai(prompt):
    """Send a prompt to the configured model."""
    client = get_ai_client()
    if client is None:
        return None, "AI API key is not configured."

    # Change this model name to a model available in your API account.
    model = st.secrets.get("OPENAI_MODEL", "gpt-5")

    try:
        response = client.responses.create(
            model=model,
            input=prompt,
        )
        return response.output_text, None
    except Exception as exc:
        return None, str(exc)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7fbff 0%, #ffffff 50%, #f5f8ff 100%);
    }

    .block-container {
        max-width: 1350px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    .brand {
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .tagline {
        font-size: 16px;
        opacity: 0.7;
        margin-top: -8px;
        margin-bottom: 20px;
    }

    .hero {
        padding: 42px;
        border-radius: 28px;
        background: linear-gradient(135deg, #4c6fff, #7852ff);
        color: white;
        box-shadow: 0 15px 45px rgba(50, 60, 150, 0.18);
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 46px;
        margin: 0 0 10px 0;
        font-weight: 800;
    }

    .hero p {
        font-size: 19px;
        max-width: 760px;
        line-height: 1.6;
        margin: 0;
    }

    .card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 23px;
        font-weight: 750;
    }

    .learning-card {
        background: white;
        padding: 30px;
        border-radius: 22px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.07);
        margin-top: 25px;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
        font-size: 16px;
    }

    .footer {
        text-align: center;
        margin-top: 60px;
        padding: 25px;
        opacity: 0.65;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "lesson" not in st.session_state:
    st.session_state.lesson = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="brand">🌟 {APP_NAME}</div>
    <div class="tagline">{TAGLINE}</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Learning can be an adventure! 🚀</h1>
        <p>
            Explore science, mathematics, languages, space, nature and
            much more with your personal AI learning companion.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 👋 Learner Profile")

    learner_name = st.text_input(
        "Your name",
        placeholder="Optional",
    )

    age_group = st.selectbox(
        "Age group",
        ["6–8 years", "9–11 years", "12–14 years", "15–17 years"],
    )

    learning_level = st.selectbox(
        "Learning level",
        ["Beginner", "Intermediate", "Advanced"],
    )

    st.divider()

    st.markdown("### 🎨 Learning Style")

    visual_learning = st.checkbox("🖼️ Visual explanations", value=True)
    examples = st.checkbox("💡 Real-world examples", value=True)
    quizzes = st.checkbox("🧩 Interactive quizzes", value=True)

# ============================================================
# LEARNING FORM
# ============================================================

st.markdown(
    """
    <div class="card">
        <div class="card-title">📚 What would you like to learn?</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    subject = st.selectbox(
        "Subject",
        [
            "🔬 Science",
            "➗ Mathematics",
            "📖 English",
            "🌍 Geography",
            "🏛️ History",
            "🌌 Space",
            "🐾 Nature & Animals",
            "💻 Computer Science",
            "🎨 Art & Creativity",
        ],
    )

with col2:
    topic = st.text_input(
        "Topic",
        placeholder="e.g. Solar System",
    )

learning_goal = st.selectbox(
    "🎯 Learning goal",
    [
        "Learn a new concept",
        "Understand a difficult topic",
        "Prepare for a test",
        "Practice with examples",
        "Take a quiz",
    ],
)

st.write("")

generate_button = st.button(
    "🚀 START LEARNING",
    type="primary",
    use_container_width=True,
)

# ============================================================
# GENERATE LESSON
# ============================================================

if generate_button:
    if not topic.strip():
        st.warning("Please enter a topic that you want to learn.")
    else:
        prompt = build_learning_prompt(
            age_group,
            learning_level,
            subject,
            topic.strip(),
            learning_goal,
        )

        with st.spinner("🤖 Your AI teacher is preparing your lesson..."):
            lesson, error = ask_ai(prompt)

        if error:
            st.error(error)
            st.info(
                "For local testing, create .streamlit/secrets.toml "
                "and add OPENAI_API_KEY."
            )
        else:
            st.session_state.lesson = lesson
            st.session_state.messages = []

# ============================================================
# LESSON
# ============================================================

if st.session_state.lesson:
    st.divider()

    st.markdown(
        '<div class="learning-card">',
        unsafe_allow_html=True,
    )

    st.markdown("## 📖 Your AI Lesson")
    st.markdown(st.session_state.lesson)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# VISUAL LEARNING
# ============================================================

if st.session_state.lesson:
    st.divider()
    st.markdown("## 🖼️ Visual Learning")

    image_files = [
        p for p in IMAGE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]

    if image_files:
        cols = st.columns(min(3, len(image_files)))
        for index, image_file in enumerate(image_files[:3]):
            with cols[index]:
                st.image(
                    str(image_file),
                    caption=image_file.stem.replace("_", " ").title(),
                    use_container_width=True,
                )
    else:
        st.info(
            "Add educational images to assets/images/ to display them here."
        )

# ============================================================
# VIDEO LEARNING
# ============================================================

if st.session_state.lesson:
    st.divider()
    st.markdown("## 🎬 Short Educational Video")

    video_files = [
        p for p in VIDEO_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".webm"}
    ]

    if video_files:
        st.video(str(video_files[0]))
    else:
        st.info(
            "Add an approved educational video to assets/videos/ "
            "to display it here."
        )

# ============================================================
# AI TUTOR
# ============================================================

st.divider()
st.markdown("## 🤖 Ask Your AI Teacher")
st.write("Ask a question about the topic you are learning.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input("Ask your teacher something...")

if user_question:
    st.session_state.messages.append(
        {"role": "user", "content": user_question}
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    tutor_prompt = f"""
You are Learnora AI, a safe and friendly educational tutor.

Learner age group: {age_group}
Learning level: {learning_level}
Subject: {subject}
Current topic: {topic or "not specified"}

Answer this question:
{user_question}

Rules:
- Use age-appropriate language.
- Explain rather than simply giving an answer.
- Use a simple example when useful.
- Encourage curiosity.
- Do not request personal information.
- Avoid mature or inappropriate content.
"""

    with st.chat_message("assistant"):
        answer, error = ask_ai(tutor_prompt)

        if error:
            st.error(error)
        else:
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🌟 <b>Learnora AI</b><br>
        See. Learn. Discover.<br><br>
        AI-powered educational learning experience
    </div>
    """,
    unsafe_allow_html=True,
)

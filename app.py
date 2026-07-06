import streamlit as st
import time
import whisper
import tempfile
import base64
import streamlit.components.v1 as components

from search import web_search
from ai import get_ai_response
from streamlit_mic_recorder import mic_recorder 
from streamlit_float import float_init, float_parent

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

whisper_model = load_whisper()

st.set_page_config(
    page_title="Suri AI",
    page_icon="🤖",
    layout="wide"
)

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

with open("script.js") as f:
    js = f.read()

components.html(
    f"""
    <script>
    {js}
    </script>
    """,
    height=0,
)

float_init()

st.title("🤖 Suri AI")
st.caption("🚀 AI Search Assistant powered by Groq + Tavily")

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.title("🤖 Suri AI")

    st.success("🟢 Status: Online")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("💡 Example Questions")

    examples = [
        "What is Artificial Intelligence?",
        "Latest AI news",
        "Explain Python",
        "Who is Elon Musk?",
        "Best programming language"
    ]

    for q in examples:
        if st.button(q, use_container_width=True):
            st.session_state.example_prompt = q

    st.divider()

    st.subheader("📊 Chat Stats")

    st.metric(
        "Messages",
        len(st.session_state.get("messages", []))
    )

    st.divider()

    st.subheader("ℹ️ About")

    st.info("""
### Suri AI v0.1

🚀 Groq LLM

🌐 Tavily Search

🎨 Streamlit UI

Built with ❤️ by Suri
""")

# ---------------- Session Memory ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "example_prompt" not in st.session_state:
    st.session_state.example_prompt = ""

# ---------------- Show Previous Messages ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.subheader("🎤 Voice Input")

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True,
)

if audio:
    st.success("✅ Voice recorded successfully!")
    st.info("🗣️ Speech-to-text conversion will be added in the next step.")
    st.write(audio)

    uploaded_files = st.file_uploader(
    "📎 Upload Files / Images",
    type=["png", "jpg", "jpeg", "pdf", "docx", "txt"],
    accept_multiple_files=True
)

camera_image = st.camera_input("📷 Take a Photo")

prompt = st.chat_input("Ask me anything...")

if not prompt and st.session_state.example_prompt:
    prompt = st.session_state.example_prompt
    st.session_state.example_prompt = ""

if prompt:

    start_time = time.time()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("🔍 Searching the web..."):

        context, results = web_search(prompt)

        messages = [
            {
                "role": "system",
                "content": f"""
You are Suri AI.

Use conversation history and web search.

Rules:

- Be accurate.
- Don't make up facts.
- Keep answers simple.
- Explain clearly.

Web Information:

{context}
"""
            }
        ]

        messages.extend(st.session_state.messages)

        answer = get_ai_response(messages)

        # ---------------- Assistant Reply ---------------- #

    with st.chat_message("assistant"):

        st.write("🧠 Suri AI is thinking...")

        placeholder = st.empty()

        full_text = ""

        for word in answer.split():

            full_text += word + " "

            placeholder.markdown(full_text + "▌")

            time.sleep(0.02)

        placeholder.markdown(full_text)

        st.divider()

        st.subheader("📋 Copy Response")

        st.code(answer, language="text")
        
        st.download_button(
    label="📄 Download Response (.txt)",
    data=answer,
    file_name="suri_ai_response.txt",
    mime="text/plain",
    use_container_width=True,
)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "👍 Helpful",
                key=f"like_{len(st.session_state.messages)}"
            ):
                st.success("Thanks for your feedback! ❤️")

        with col2:
            if st.button(
                "👎 Not Helpful",
                key=f"dislike_{len(st.session_state.messages)}"
            ):
                st.info("Thanks! I'll keep improving. 🚀")

        if results:

            st.divider()

            with st.expander("📚 Sources", expanded=False):

                for i, result in enumerate(results, start=1):

                    title = result.get("title", "No Title")
                    url = result.get("url", "")

                    st.markdown(f"**{i}. {title}**")

                    if url:
                        st.link_button(
                            "🌐 Open Source",
                            url,
                            key=f"link_{i}_{len(st.session_state.messages)}"
                        )

        st.divider()

        end_time = time.time()

        st.caption(
            f"⚡ Response Time: {end_time-start_time:.2f} seconds"
        )

        st.markdown("### 💡 Suggested Follow-up")

        suggestions = [
            "Explain in simple words",
            "Give an example",
            "Summarize this",
            "Tell me more"
        ]

        cols = st.columns(2)

        for index, suggestion in enumerate(suggestions):

            with cols[index % 2]:
                st.button(
                    suggestion,
                    key=f"suggest_{index}_{len(st.session_state.messages)}"
                )

    # ---------------- Save Chat ---------------- #

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Keep only last 10 messages

    if len(st.session_state.messages) > 10:
        st.session_state.messages = (
            st.session_state.messages[-10:]
        )
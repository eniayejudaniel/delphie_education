import streamlit as st
from delphi_ai_assistant import ask_groq, load_history, save_history

# --- PAGE SETUP ---
st.set_page_config(page_title="Delphi Education Assistant", page_icon="🎓")

st.title("🎓 Delphi Education Assistant")
st.write("Chat with your study abroad assistant about UK universities, visas, and scholarships.")

# --- LOAD CHAT HISTORY ---
if "history" not in st.session_state:
    st.session_state.history = load_history()

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.history:
    role = msg.get("role")
    content = msg.get("content", "")
    if role == "user":
        st.chat_message("user").write(content)
    elif role == "assistant":
        st.chat_message("assistant").write(content)

# --- USER INPUT ---
prompt = st.chat_input("Ask your question about studying in the UK...")

if prompt:
    # Display user input immediately
    st.chat_message("user").write(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    # Get assistant reply
    reply = ask_groq(prompt, st.session_state.history)

    # Display assistant reply
    st.chat_message("assistant").write(reply)
    st.session_state.history.append({"role": "assistant", "content": reply})

    # Save conversation
    save_history(st.session_state.history)

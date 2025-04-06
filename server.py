import streamlit as st
from load import get_student_summary
from chatbot import query_huggingface, build_prompt
from streamlit_chat import message

st.set_page_config(page_title="Student Advisory Bot", layout="centered")

st.title("🎓 Student Advisory Bot")
st.markdown("Ask questions related to your academic progress!")

# Initialize session state
if "student_loaded" not in st.session_state:
    st.session_state["student_loaded"] = False
    st.session_state["student_context"] = ""
    st.session_state["chat_history"] = []

if not st.session_state["student_loaded"]:
    emplid = st.text_input("Enter your EMPLID (Student ID):")
    if emplid:
        try:
            emplid = int(emplid)
            student_context = get_student_summary(emplid)
            st.session_state["student_context"] = student_context
            st.session_state["student_loaded"] = True
            st.success("Student data loaded successfully!")
        except ValueError:
            st.error("Please enter a valid numeric EMPLID.")
        except Exception as e:
            st.error(f"Error loading data: {e}")

# If student is loaded, show details and chat interface
if st.session_state["student_loaded"]:
    st.subheader("📄 Student Summary")
    st.text(st.session_state["student_context"])

    with st.form(key="chat_form", clear_on_submit=True):
        user_question = st.text_input("Ask your question:")
        submit = st.form_submit_button("Send")

    if submit and user_question:
        prompt = build_prompt(st.session_state["student_context"], user_question)
        full_response = query_huggingface(prompt)
        cleaned_response = full_response.replace(prompt.strip(), "").strip()

        # Store chat history
        st.session_state["chat_history"].append(("You", user_question))
        st.session_state["chat_history"].append(("Bot", cleaned_response))

    # Display chat history
    for role, msg in st.session_state["chat_history"]:
        message(msg, is_user=(role == "You"))

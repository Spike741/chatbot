import streamlit as st
import os
from groq import Groq

# Your Groq API key
GROQ_API_KEY ="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" # Or paste your key here for testing

# Define your groq_chat function
def groq_chat(context, question, model="llama3-8b-8192"):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": (
                    "You are a helpful legal assistant. "
                    "Only answer questions that are related to law, legal advice, or legal topics. "
                    "If the user's question is not related to law, politely respond: "
                    "'I'm sorry, I can only answer questions related to legal matters.' "
                    "Answer questions based only on the provided context."
                )},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ],
            temperature=0.2,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from Groq API: {e}"

# Example legal context (you can expand or update this as needed)
LEGAL_CONTEXT = (
    "This chatbot provides information about legal matters such as contracts, property law, employment law, "
    "intellectual property, and general legal rights. It does not provide medical, financial, or other non-legal advice."
)

# Streamlit UI
st.title("Legal Chatbot (Groq API)")
st.write("Ask me anything about law or legal matters. I will only answer legal questions.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    # Get reply from Groq legal chatbot
    bot_reply = groq_chat(LEGAL_CONTEXT, user_input)
    # Add to chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("LegalBot", bot_reply))

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")


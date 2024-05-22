import streamlit as st
import time
from groq import Groq
from PyPDF2 import PdfReader

# Set page config
st.set_page_config(
    page_title="JALI!",
    page_icon=":heart:",
    initial_sidebar_state="collapsed",
)

# Initialize Groq client
client = Groq(
    api_key = st.secrets["API_KEY"]
)

# Define a function to stream text
def stream_data(text):
    for char in text:
        yield char
        time.sleep(0.02)

# Define a function to summarize text
def summarize_text(text, manner):
    summariser = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are a helpful assistant named Jali to help explain elements to students of the Wikitech KNUST community, clearly explain this: {text} considering {manner} especially."
            }
        ],
        model="llama3-8b-8192",
        temperature=0.6
    )
    return summariser.choices[0].message.content

# Define a function to store conversation
def store_conversation(content):
    with open("talk.txt", "a") as file:
        file.write("\n")
        file.write(content)

# Main app
st.title(':heart: _Project_ :blue[JALI!] ')

st.caption("Just Ask JALI to help you with your study materials!")
st.write("")

# Side bar
st.sidebar.image(image='logo.png', width=80)
st.sidebar.subheader("Welcome")
st.sidebar.caption("Hello students of the Wikitech Student Community! I am JALI, your personal assistant. I am here to help you with your study materials. ")

uploaded_file = st.sidebar.file_uploader('File uploader')

slider = st.sidebar.slider("Move scope", 0, 3000, 0, 10)
if slider is not None:
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        page = st.number_input("Enter page number", 0, 200, 0, 1)
        try:
            page = reader.pages[page]
            topic = page.extract_text()[0:slider]
            st.write(topic)
            manner = st.text_input("Highlight the manner in which you want the explanation to be given e.g. with practical examples, in a more relatable context etc.")

            if st.sidebar.button("Explain this to me"):
                st.write(summarize_text(topic, manner))
                store_conversation(summarize_text(topic, manner))

            if st.sidebar.button("Store this conversation"):
                store_conversation(summarize_text(topic, manner))

        except:
            st.write("No text found")

# Chat input
input_ = st.chat_input("Say something")
if input_:
    with open("talk.txt", "w") as file:
        file.write(input_)

    with st.chat_message("user"):
        st.write(f"{input_}")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_
            }
        ],
          model="mixtral-8x7b-32768",
        temperature=0.75
    )

    

    with st.chat_message("AI"):
        st.write("Wikibot:")
        data = f"{chat_completion.choices[0].message.content}"
        st.write_stream(stream_data(data))

    st.write(summarize_text(topic, manner))

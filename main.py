import streamlit as st
import time
from groq import Groq
from PyPDF2 import PdfReader

# stream effect
st.set_page_config(
    page_title="JALI!",
    page_icon=":heart:",
    initial_sidebar_state="collapsed",
)

def stream_data(stream):
    for word in stream.split(" "):
         yield word + " "
         time.sleep(0.02)

client = Groq(
    api_key="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",
)    

topic = str()
focus_pointer = int()

st.image(image='logo.png', width=60)

# logo = st.image(image='logo.png', width=60)
st.title(':heart: _Project_ :blue[JALI!] ')

st.caption("Just Ask JALI to help you with your study materials!")
st.write("")

# side
st.sidebar.image(image='logo.png', width=80)
st.sidebar.subheader("Welcome")
st.sidebar.caption("Hello students of the Wikitech Student Community! I am JALI, your personal assistant. I am here to help you with your study materials. ")

uploaded_file = st.sidebar.file_uploader('File uploader')

slider = st.sidebar.slider("Move scope", 0, 3000, 0, 10)
# read as string
if slider is not None:
     if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        page = st.number_input("Enter page number", 0, 200, 0, 1)
        #  st.write(reader)
        
        try:
            page = reader.pages[page]
            topic = page.extract_text()[focus_pointer:focus_pointer+slider]
            st.write(topic)
            manner = st.text_input("Highlight the manner in which you want the explanation to be given e.g. with practical examples, in a more relatable context etc.")

        except:
            st.write("No text found")
        # focus_pointer += slider
 
summarise = st.sidebar.button("Explain this to me")

# store = st.sidebar.button("Store this conversation")      

def store_conversation(content):
    with open("talk.txt", "a") as file:
        file.write("\n")
        file.write(content)
# file = open("talk.txt", "r")


if summarise:
    summariser = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"You are a helpful assistant named Jali to help explain elements to students of the Wikitech KNUST community, clearly explain this: {topic} condering {manner} especially."
        }
    ],
    model="llama3-8b-8192",
    temperature=0.6
 )

    with st.chat_message("AI"):
        st.write("Summary:")
        data = f"{summariser.choices[0].message.content}"
        st.write_stream(stream_data(data))

        with open("talk.txt", "a") as file:
            file.write("\n")
            file.write("#"*50)
            file.write(summariser.choices[0].message.content)

        st.sidebar.download_button("Download conversation", data, "Conversation_with_JALI!.txt",  key="pull")

    with open("talk.txt", "a") as file:
        file.write("\n")
        file.write("#"*50)
        file.write(summariser.choices[0].message.content)

# Display a chat input widget.
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
    model="llama3-8b-8192")
     
     summariser = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Explain this more clearly and with more relatable, practical real-world examples: {topic}."
        }
    ],
    model="mixtral-8x7b-32768",
    temperature=0.75
 )

     with st.chat_message("AI"):
        st.write("Wikibot:")
        data = f"{chat_completion.choices[0].message.content}"
        st.write_stream(stream_data(data))

     def summarise_text():
        with st.chat_message("AI"):
            st.write("Summary:")
            data = f"{summariser.choices[0].message.content}"
            st.write_stream(stream_data(data))

     


    





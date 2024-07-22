import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from dotenv import load_dotenv
import openai
import os


# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def getOpenaiResponse(query_text):
    # Create CLI.
    # parser = argparse.ArgumentParser()
    # parser.add_argument("query_text", type=str, help="The query text.")
    # args = parser.parse_args()
    # query_text = "Give me the summary of math application"

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    print('Query is', query_text)
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        # print(f"Unable to find matching results.", results)
        return ":orange[**Ooooopsss**] :pensive: ... Perhaps I am not aware of this. But I can assist you with queries regarding the Math calculator"

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f":blue[Hurray] :sunglasses: :\n {response_text}\n\nSources: {sources}"
    print(formatted_response)
    return formatted_response

st.set_page_config(page_title="Doc AI Demo")
st.header("Dhaval's Doc AI")
input=st.text_input("Ask me anything about Math calculator 👇 ",key="input")
submit=st.button("Ask the question")

## If ask button is clicked
if submit:
    response=getOpenaiResponse(input)
    resphdr=st.subheader("The Response is", divider='rainbow')
    hdrtext="The Response is"
    respdata=st.write(response)
# elif 1:
#     st.subheader("Your response will appear here", divider='rainbow')
else:
    st.subheader("Your response will appear here", divider='rainbow')
    
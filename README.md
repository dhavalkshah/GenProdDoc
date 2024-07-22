# Generate Product Documentation

## Environment Variable
* OPENAI_API_KEY - Input your Open API key here
* DATA_PATH - Path to the directory where HTMLs are present

## Installation
```pip install -r requirements.txt```

## Steps
- Refresh RAG DB
  ```py refreshdb.py```
  This will scan all the HTMLs present in *DATA_PATH*. Extact all the html content. Tokenize the content and store it in Chroma DB.
  The process will split the content in different chunks and then insert it into Chroma DB.
  
- Run Application
  ```streamlit run app.py```
  It will prompt the user to input the query.
  Query will be tokenized and compared to already stored tokens from Chroma DB.
  If the similarity is above threshold (70% in this case), the query will be passed to OpenAI (chatGpt).
  The response will be then sent back to the user.

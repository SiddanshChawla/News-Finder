from newsapi import NewsApiClient
from news import extract_phrases
import streamlit as st
import numpy as np
from datetime import date
from datetime import timedelta
import nltk
nltk.download('stopwords')
nltk.download('punkt')

today = date.today()
week_before = today - timedelta(days = 7)

# Set up NewsAPI client
newsapi = NewsApiClient(api_key='0eab831ebf9c402ba6f4f2312b355ad6')

# Example description
description = st.text_input("Enter the text to search news article...")
keywords = extract_phrases(description)
important_keywords = keywords[:2]

# Search for news articles related to the keywords
articles = []
for keyword in important_keywords:
    keyword = keyword
    news = newsapi.get_everything(q=keyword, from_param=week_before, language='en')
    articles.extend(news['articles'])

# Print article titles and description
for article in articles:
    st.write(article['title'])
    st.write(article['description'])
    st.write(article['url'])
    st.write('---')

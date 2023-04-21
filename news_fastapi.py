from fastapi import FastAPI
from datetime import date
from datetime import timedelta
from newsapi import NewsApiClient
from rake_nltk import Rake

app = FastAPI()

# news api client
newsapi = NewsApiClient(api_key='0eab831ebf9c402ba6f4f2312b355ad6')

def extract_phrases(text : str = None):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    phrases = rake.get_ranked_phrases_with_scores()
    important_phrases = [phrase for _, phrase in phrases]
    return important_phrases

def get_data(text: str = None):
    keywords = extract_phrases(text)
    important_keywords = keywords[:2]
    return important_keywords

@app.get("/news")
def return_news(text: str = None):
    important_keywords = get_data(text)
    articles = []
    for keyword in important_keywords:
        keyword = keyword
        today = date.today()
        week_before = today - timedelta(days = 7)
        news = newsapi.get_everything(q=keyword, from_param=week_before, language='en')
        articles.extend(news['articles'])
    return [{"title": article['title'], "description": article['description'], "url": article['url']} for article in articles]

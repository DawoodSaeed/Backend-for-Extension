import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Establishing the connection with the database
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://amnewsing:hmIiNbPsAeOgohyA@fypcluster.yuntl03.mongodb.net/?retryWrites=true&w=majority")
    db = client["test"]
    return client, db

# Preprocess text: remove stop words, perform stemming and lemmatization
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stop_words]
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in stemmed_tokens]

    processed_text = ' '.join(lemmatized_tokens)
    return processed_text

# Fetch news articles from the database
def get_news_articles_from_db(query, db, until_date):
    collection = db["news"]
    articles = collection.find({
        "$or": [
            {"headline": {"$regex": query, "$options": "i"}},
            {"body": {"$regex": query, "$options": "i"}}
        ]
    })
    return list(articles)

# Fetch articles from news API
def get_news_articles_from_api(query):
    url = "https://newsapi.org/v2/everything"
    news_api_key = "93ecb5242de146e1b68a7237230d48a5"
    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")
    params = {
        "q": query,
        "apiKey": news_api_key,
        "from": from_date,
        "to": to_date,
        "pageSize": 10
    }

    response = requests.get(url, params=params)
    articles = response.json()["articles"]
    return articles

# Remove duplicate articles based on text similarity
def remove_duplicates(db_articles, api_articles, threshold=0.8):
    unique_articles = db_articles.copy()

    for api_article in api_articles:
        is_duplicate = False
        api_text = preprocess_text(api_article["content"])
        
        for db_article in db_articles:
            db_text = preprocess_text(db_article["body"])
            similarity = SequenceMatcher(None, api_text, db_text).ratio()

            if similarity >= threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_articles.append(api_article)

    return unique_articles

def generate_news_history(query):
    client, db = connect_to_mongodb()
    until_date = datetime.now()
    db_articles = get_news_articles_from_db(query, db, until_date)
    api_articles = get_news_articles_from_api(query)

    all_articles = db_articles + api_articles
    deduplicated_articles = remove_duplicates(db_articles, api_articles)

    history = []
    for i, article in enumerate(deduplicated_articles, start=1):
        title = article.get("title", article.get("headline", ""))
        date = article.get("publishedAt", article.get("time", ""))
        url = article["url"]

        if i <= len(db_articles):
            source = "Database"
        else:
            source = "News API"

        history.append({
            "source": source,
            "title": title,
            "date": date,
            "url": url
        })

    client.close()
    return {"history": history}
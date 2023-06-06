from create_generic_sentence import generate_generic_sentence
from news_history_generator import generate_news_history
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pydantic import BaseModel
from newspaper import Article
# Create FastAPI instance
app = FastAPI()

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",  # Add the origin of your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def connect_to_mongodb():
    client = MongoClient("mongodb+srv://amnewsing:hmIiNbPsAeOgohyA@fypcluster.yuntl03.mongodb.net/?retryWrites=true&w=majority")
    db = client["test"]
    return client, db


# Route for news history
@app.get("/news-history/{query}")
def get_news_history(query: str):
    return generate_news_history(query)
    
@app.get("/generate_generic_sentence/{title}")
def get_generic_sentence(title: str):
    return generate_generic_sentence(title)
class URLItem(BaseModel):
    url: str



    # Check if the article already exists;
    # if it does then send that article; (display it on the frontend)
    # If not then 
@app.get("/authenticity")
def get_authenticity(url_item: URLItem):
    url = str(url_item.url)
    print(url)
    client, db = connect_to_mongodb()
    collection = db["news"]
    article = collection.find_one({"url": url})

    # if the article exists then display this article;
    if article is not None:
        print(article)
        article["_id"] = str(article["_id"])
        return JSONResponse(content=article)
    # if it doesnt then scrap it 
    else:
        scrapped_article = Article(url=url)
        # Download and parse the article;
        scrapped_article.download()
        scrapped_article.parse()
        # Now what I need to store this article in the DB
        #url newsSource mainImage time authenticity headline author body topic
        # After parsing I need to send the article I want to check it authentity;


        
        article = {
            "url": url,
            "mainImage": scrapped_article.top_image,
            "headline": scrapped_article.title,
            "body": scrapped_article.text,
            "author": scrapped_article.authors[0] if scrapped_article.keywords else "Unknown",
            "topic": scrapped_article.keywords[0] if scrapped_article.keywords else "Unknown" 
        }

        return JSONResponse(content=article)
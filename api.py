from fastapi import FastAPI, Query
import pandas as pd
import os

app = FastAPI()

# Load CSV data
df = pd.read_csv("scraping_results (14).csv")

@app.get("/")
def home():
    return {
        "message": "Medium Article Search API",
        "articles": len(df),
        "usage": "/search?query=your_keywords"
    }

@app.get("/search")
def search(query: str = "technology", top_n: int = 10):
    # Simple search in titles
    results = df[df['title'].str.contains(query, case=False, na=False)]
    
    if len(results) == 0:
        results = df.head(top_n)
    
    return {
        "query": query,
        "results": results.head(top_n)[['title', 'url']].to_dict('records')
    }

@app.get("/articles")
def all_articles():
    return df[['title', 'url']].to_dict('records')

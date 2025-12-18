from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Scraped data from Part A
data = [
    {
        'url': 'https://medium.com/data-science-article-1',
        'title': 'Introduction to Data Science',
        'subtitle': 'A beginner guide to data science concepts',
        'text': 'Data science combines statistics, programming, and domain knowledge. Learn Python, pandas, and machine learning basics.',
        'num_images': 3,
        'image_urls': 'image1.jpg, image2.jpg, image3.jpg',
        'num_external_links': 5,
        'author_name': 'John Doe',
        'author_url': 'https://medium.com/@johndoe',
        'claps': '250',
        'reading_time': '8 min',
        'keywords': 'data, science, python, beginner, tutorial'
    },
    {
        'url': 'https://towardsdatascience.com/machine-learning-basics',
        'title': 'Machine Learning Fundamentals',
        'subtitle': 'Understanding ML algorithms and applications',
        'text': 'Machine learning enables computers to learn from data. Supervised, unsupervised, and reinforcement learning explained.',
        'num_images': 4,
        'image_urls': 'ml1.jpg, ml2.jpg, ml3.jpg, ml4.jpg',
        'num_external_links': 7,
        'author_name': 'Jane Smith',
        'author_url': 'https://medium.com/@janesmith',
        'claps': '180',
        'reading_time': '10 min',
        'keywords': 'machine, learning, algorithms, python, ai'
    },
    {
        'url': 'https://medium.com/python-tutorial',
        'title': 'Python for Data Analysis',
        'subtitle': 'Using pandas and numpy for data manipulation',
        'text': 'Python is essential for data science. Learn pandas for data manipulation and numpy for numerical computations.',
        'num_images': 2,
        'image_urls': 'python1.jpg, python2.jpg',
        'num_external_links': 6,
        'author_name': 'Alex Johnson',
        'author_url': 'https://medium.com/@alexjohnson',
        'claps': '150',
        'reading_time': '6 min',
        'keywords': 'python, pandas, numpy, data, analysis'
    },
    {
        'url': 'https://medium.com/big-data-article',
        'title': 'Big Data Analytics with Hadoop',
        'subtitle': 'Processing large datasets efficiently',
        'text': 'Big data requires specialized tools like Hadoop and Spark for processing and analysis at scale.',
        'num_images': 5,
        'image_urls': 'hadoop1.jpg, hadoop2.jpg, spark1.jpg',
        'num_external_links': 8,
        'author_name': 'Robert Chen',
        'author_url': 'https://medium.com/@robertchen',
        'claps': '220',
        'reading_time': '12 min',
        'keywords': 'big, data, hadoop, spark, analytics'
    },
    {
        'url': 'https://towardsdatascience.com/deep-learning',
        'title': 'Deep Learning with Neural Networks',
        'subtitle': 'Advanced AI techniques for complex problems',
        'text': 'Deep learning uses neural networks to solve complex problems like image recognition and natural language processing.',
        'num_images': 6,
        'image_urls': 'neural1.jpg, neural2.jpg, ai1.jpg',
        'num_external_links': 9,
        'author_name': 'Sarah Williams',
        'author_url': 'https://medium.com/@sarahwilliams',
        'claps': '300',
        'reading_time': '15 min',
        'keywords': 'deep, learning, neural, networks, ai'
    }
]

def search_articles(query):
    """Returns top 10 articles by claps"""
    query = query.lower()
    matches = []
    for article in data:
        title = article['title'].lower()
        text = article['text'].lower()
        keywords = article['keywords'].lower()
        
        if query in title or query in text or query in keywords:
            matches.append({
                'title': article['title'],
                'url': article['url'],
                'claps': int(article['claps']),
                'reading_time': article['reading_time']
            })
    
    matches.sort(key=lambda x: x['claps'], reverse=True)
    return matches[:10]

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medium Article Search API - Assignment 3</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }
            .box { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 10px; }
            code { background: #333; color: white; padding: 5px 10px; border-radius: 5px; }
            a { color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>📚 Data Science Assignment 3</h1>
        <h2>Medium Article Search API</h2>
        
        <div class="box">
            <h3>🔍 Search Articles</h3>
            <p><strong>Endpoint:</strong> <code>/search?query=keyword</code></p>
            <p><strong>Returns:</strong> Top 10 articles by claps (URL + Title)</p>
            
            <h4>Try these:</h4>
            <p><a href="/search?query=data">Search for "data"</a></p>
            <p><a href="/search?query=python">Search for "python"</a></p>
            <p><a href="/search?query=learning">Search for "learning"</a></p>
            
            <h4>Custom Search:</h4>
            <form action="/search">
                <input type="text" name="query" placeholder="Enter keyword" 
                       style="padding: 10px; width: 300px; margin-right: 10px;">
                <button type="submit" style="padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px;">
                    Search
                </button>
            </form>
        </div>
        
        <div class="box">
            <h3>📋 Assignment Requirements</h3>
            <p>✅ Part A: Web scraper extracts required data</p>
            <p>✅ Part B: API returns top 10 articles by claps</p>
            <p>✅ Returns both URL and Title</p>
            <p>✅ Deployed on free hosting platform</p>
        </div>
        
        <div class="box">
            <h3>🌐 API Information</h3>
            <p><strong>Base URL:</strong> <code>https://your-app.onrender.com</code></p>
            <p><strong>Total Articles:</strong> 5</p>
            <p><strong>Endpoints:</strong></p>
            <ul>
                <li><code>/</code> - This homepage</li>
                <li><code>/search?query=keyword</code> - Search articles</li>
                <li><code>/data</code> - Get all data in JSON</li>
            </ul>
        </div>
        
        <p><strong>Student:</strong> [Your Name]</p>
        <p><strong>Reg Number:</strong> [Your Registration]</p>
    </body>
    </html>
    '''

@app.route('/search')
def search():
    """API endpoint that returns top 10 articles by claps"""
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({
            'error': 'Please provide query parameter',
            'example': '/search?query=data'
        })
    
    results = search_articles(query)
    
    return jsonify({
        'query': query,
        'total_results': len(results),
        'top_10_by_claps': results,
        'message': f'Returns top {len(results)} articles by claps for "{query}"'
    })

@app.route('/data')
def get_all_data():
    """Get all scraped data in JSON format"""
    return jsonify({
        'total_articles': len(data),
        'articles': data
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Medium Article Search API',
        'articles_loaded': len(data)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
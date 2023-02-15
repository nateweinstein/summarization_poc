from flask import Flask, jsonify,make_response, request
from flask_cors import CORS

from tinydb import TinyDB, Query
db = TinyDB('db/parsed_db.json')
from lib.get_web import strip_tags, search_word_in_string
from lib.search import search


app = Flask(__name__)
cors = CORS(app)


@app.route('/authors', methods=['GET'])
def get_authors():
    all = db.all()
    authors =[]
    for a in all:
        # print(a['author'])
        try:
            authors.append(a['author'])
            # authors.extend(a['author'].replace(', ', ',').split(','))
        except:
            pass
    authors =sorted(set(authors))
    response = make_response({'authors': authors})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/articles', methods=['GET'])
def get_articles():
    entry  = Query()
    author = request.args.get('author')
    authorArticles = db.search(entry.author.matches('.*'+author+'.*'))
    authors = []
    for a in authorArticles:
        # print(a['author'])
        try:
            authors.append(a['title'])
            # authors.extend(a['author'].replace(', ', ',').split(','))
        except:
            pass
    
    articles =sorted(set(authors))
    print("AUTHORS!!", authors)    
    response = make_response({'articles': articles})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



@app.route('/summarize', methods=['GET'])
def summarize():
    author = request.args.get('author')
    term = request.args.get('keyword')
    contents, num_articles, relevant = search(author, term)

    response = make_response({'content': contents,'num_articles': num_articles,'original_content':relevant})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    app.run(debug=True)

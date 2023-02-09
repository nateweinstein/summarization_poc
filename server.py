from flask import Flask, jsonify,make_response, request
from tinydb import TinyDB, Query
db = TinyDB('db/database.json')
from transformers import pipeline
from lib.get_web import strip_tags, search_word_in_string

print("Starting summarizer")
summarizer = pipeline("summarization", 
    model="my_awesome_billsum_model")
print('finished')

app = Flask(__name__)


@app.route('/authors', methods=['GET'])
def get_authors():
    all = db.all()
    authors =[]
    for a in all:
        try:
            authors.extend(a['author'].replace(', ', ',').split(','))
        except:
            pass
    authors =sorted(set(authors))
    response = make_response({'authors': authors})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



@app.route('/summarize', methods=['GET'])
def summarize():
    author = request.args.get('author')
    term = request.args.get('keyword')

    # Search db
    entry = Query()
    authorArticles = db.search(entry.author.matches('.*'+author+'.*') & entry.body.search('.*'+term+'.*'))
    relevant = ''

    for art in authorArticles:
        cleaned = strip_tags(art['body'])
        relevant = relevant +' '+ search_word_in_string(term, cleaned, 7000)    
    

    contents = summarizer(relevant)[0]['summary_text']
    
    response = make_response({'content': contents})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    app.run(debug=True)

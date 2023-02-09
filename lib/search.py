import torch
import os
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import time
import re
from .get_web import strip_tags
from tinydb import TinyDB, Query

dirname = os.path.dirname(__file__)
db_file = os.path.join(dirname, '../db/database.json')
db = TinyDB(db_file)

# Load a pre-trained model semantic search model
# Use this tutorial: https://medium.com/mlearning-ai/how-to-build-a-semantic-search-engine-using-python-5c68e8442df1
print('compiling sentence transforrmer....')
model =SentenceTransformer('msmarco-MiniLM-L-12-v3')
print('DOne!')


print("Pipelining summarizer")
summarizer_model = os.path.join(dirname, '../my_awesome_billsum_model')
summarizer = pipeline("summarization", 
    model=summarizer_model)
print('finished')

r = re.compile('<p(|\s+[^>]*)>(.*?)<\/p\s*>')


def search(author,term):
    print("Starting... 0")
    t=time.time()
    # Search db
    print("Db search")
    entry = Query()
    
    # Get articles from just the author
    authorArticles = db.search(entry.author.matches('.*'+author+'.*'))
    print("Done: {}".format(time.time()-t))
    relevant = []
    num_articles = len(authorArticles)
    print('regex')

    for art in authorArticles:
        # Get everything between a <p> tag
        cleaned = r.findall(art['body'])
        for clean in cleaned:
            relevant.append(strip_tags(clean[1]))
        # clean = [strip_tags(c) for c in cleaned]
        # Remove extraneous html
        # relevant.extend(clean)
    print("Done: {}".format(time.time()-t))
    print('model compile')
    print(relevant)
    print('length: '+str(len(relevant)))

    # Encode the corpus and term for semantic search
    compiled = model.encode(relevant)
    query = model.encode(term)
    print("Done: {}".format(time.time()-t))
    # query_vector = model.encode([term])
    # k = 10
    # top_k = compiled.search(query_vector, k)
    print("semantic search")
    top_k = util.semantic_search(query, compiled, top_k=10)
    # results = [relevant[_id] for _id in top_k[1].tolist()[0]][]
    results =''
    for k in top_k[0]:
        results = results + ' '+relevant[k['corpus_id']]
    print('totaltime: {}'.format(time.time()-t))
    contents = summarizer(results[:512])[0]['summary_text']

    print(contents)
    return [contents, num_articles, relevant]

    

# search('Andrew Chen', 'what are the best marketplaces')
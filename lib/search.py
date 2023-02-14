import torch
import os
import spacy


# see here for context on sentenceTransformers https://www.sbert.net/examples/applications/semantic-search/README.html
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import time
import re
from .get_web import strip_tags
from tinydb import TinyDB, Query

dirname = os.path.dirname(__file__)
db_file = os.path.join(dirname, '../db/parsed_db.json')
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


def extract_entities(query):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities


def search(author,term):
    print("Starting... 0")
    t=time.time()
    # Search db
    print("Db search")
    entry = Query()

    author = extract_entities(term)
    author = author[0][0].title()
    # print("AUTHOR", author)
    # Get articles from just the author
    authorArticles = db.search(entry.author.matches('.*'+author+'.*'))
    print("Done: {}".format(time.time()-t))
    relevant = []
    num_articles = len(authorArticles)
    print("NUM", str(num_articles))
    print('regex')

    for art in authorArticles:
        # Get everything between a <p> tag
        relevant.append(art['content'])
    print("Done: {}".format(time.time()-t))
    print('model compile')
    print(relevant)
    input()
    print('length: '+str(len(relevant)))

    # Encode the corpus and term for semantic search
    term = term.replace(author.lower(), '')
    print(term)
    compiled = model.encode(relevant)
    query = model.encode(term)
    print("Done: {}".format(time.time()-t))
    # query_vector = model.encode([term])
    # k = 10
    # top_k = compiled.search(query_vector, k)
    print("semantic search")
    top_k = util.semantic_search(query, compiled, top_k=10)
    print(top_k)
    # results = [relevant[_id] for _id in top_k[1].tolist()[0]][]
    results =''
    for k in top_k[0]:
        results = results + ' '+relevant[k['corpus_id']]
    print(results)
    print('totaltime: {}'.format(time.time()-t))
    contents = summarizer(results[:512])[0]['summary_text']

    print(contents)
    return [contents, num_articles, relevant]

    

# search('Andrew Chen', 'what are the best marketplaces')
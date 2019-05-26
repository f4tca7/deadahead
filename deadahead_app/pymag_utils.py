from pymagnitude import *

NYT_PATH = 'pymag_data/nyt_preprocessed_2000_1_2019_1.magnitude'
FB_WIKI_PATH = 'pymag_data/wiki-news-300d-1M.magnitude'
GOOGLE_NEWS_PATH = 'pymag_data/GoogleNews-vectors-negative300.magnitude'
FB_COMMON_PATH = 'pymag_data/crawl-300d-2M.magnitude'

def analyze_vectors(vectors, term1, term2, topn):
    dist = 0
    sim = 0
    n_most_sim_1 = {}
    n_most_sim_2 = {}    
    n_most_sim_1 = vectors.most_similar(term1, topn = topn)
    n_most_sim_2 = vectors.most_similar(term2, topn = topn)
    dist = vectors.distance(term1, term2)
    sim = vectors.similarity(term1, term2)
    return dist, sim, n_most_sim_1, n_most_sim_2

def analyze_w2v(corpus, term1, term2, topn):
    dist = 0
    sim = 0
    n_most_sim_1 = {}
    n_most_sim_2 = {}
    vectors = None
    if corpus == 'NYT':
        vectors = Magnitude(NYT_PATH)
 
    if corpus == 'FB_WIKI':
        vectors = Magnitude(FB_WIKI_PATH)

    if corpus == 'GOGGLE_NEWS':
        vectors = Magnitude(GOOGLE_NEWS_PATH)

    if corpus == 'FB_COMMON':
        vectors = Magnitude(FB_COMMON_PATH)

    if vectors != None:
        dist, sim, n_most_sim_1, n_most_sim_2 = analyze_vectors(vectors, term1, term2, topn)

    return dist, sim, n_most_sim_1, n_most_sim_2
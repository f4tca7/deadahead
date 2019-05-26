from pymagnitude import *

nyt_path = 'pymag_data/nyt_preprocessed_2000_1_2019_1.magnitude'

def analyze_w2v(corpus, term1, term2):
    dist = 0
    sim = 0
    n_most_sim_1 = {}
    n_most_sim_2 = {}
    if corpus == 'NYT':
        vectors_nyt = Magnitude(nyt_path)
        n_most_sim_1 = vectors_nyt.most_similar(term1, topn = 20)
        n_most_sim_2 = vectors_nyt.most_similar(term2, topn = 20)
        dist = vectors_nyt.distance(term1, term2)
        sim = vectors_nyt.similarity(term1, term2)
    return dist, sim, n_most_sim_1, n_most_sim_2
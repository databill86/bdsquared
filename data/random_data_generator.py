from __future__ import unicode_literals
from random import randrange, uniform
from json import dumps
from contextlib import closing

CLUSTERS_FILE = "clusters_toy.json"
TIMELINE_FILE = "timeline_toy.json"
FORCE_FILE = "force_toy.json"

NUM_OF_CLUSTERS = 10


def create_clusters():
    word_list = ["cat", "dog", "mum", "spoon", "chair", "apple", "dot", "sea", "run"]
    clusters = []
    for cluster_id in range(1, NUM_OF_CLUSTERS + 1):
        words = []
        remaining_weight = 1
        for i in range(0, 5):
            index = randrange(1, len(word_list) - 1)
            word = word_list[index]
            weight = uniform(0, remaining_weight)
            remaining_weight = remaining_weight - weight
            words.append({"name": word, "weight": weight})
        clusters.append({"cluster_id": cluster_id, "words": words})

    with closing(open(CLUSTERS_FILE, "w")) as cluster_file:
        cluster_file.write(dumps(clusters))


def create_timeline():
    timeline_list = []
    for cluster_id in range(1, NUM_OF_CLUSTERS + 1):
        month_list = []
        for i in range(1, 24 + 1):
            count = randrange(0, 5000)
            month_list.append({"month_id": i, "weight": count})
        timeline_list.append({"cluster_id": cluster_id, "months": month_list})

    with closing(open(TIMELINE_FILE, "w")) as timeline_file:
        timeline_file.write(dumps(timeline_list))


def create_force():
    sources = ['repubblica.it', 'corriere.it', 'iltempo.it', 'ilsole24ore.com', 'padania.org', 'ilgiornale.it', 'panorama.it', 'ilsecoloxix.it', 'ilfattoquotidiano.it', 'lastampa.it', 'lagazzettadelmezzogiorno.it', 'unionesarda.it', 'ilmessaggero.it', 'ilgiorno.it', 'leggo.it', 'ilmattino.it', 'unita.it', 'ilmanifesto.it']
    word_list = ["cat", "dog", "mum", "spoon", "chair", "apple", "dot", "sea", "run", "try", "end", "big", "dive"]

    node_list = []
    remaining_source_weight = 1
    for source in sources:
        # % of participation to the corpus of articles
        source_weight = uniform(0, remaining_source_weight)
        remaining_source_weight = remaining_source_weight - source_weight
        cluster_source_weights = []
        for cluster_id in range(1, NUM_OF_CLUSTERS + 1):
            # % of participation to the cluster
            cluster_source_weights.append({"cluster_id": cluster_id, "weight": uniform(0, 1)})
        node_list.append({"name": source, "type": "source", "weight": source_weight, "clusters": cluster_source_weights})

    remaining_word_weight = 1
    for word in word_list:
        # % of participation to the corpus of articles
        word_weight = uniform(0, remaining_word_weight)
        remaining_word_weight = remaining_word_weight - word_weight
        cluster_word_weights = []
        for cluster_id in range(1, NUM_OF_CLUSTERS + 1):
            # % of participation to the cluster
            cluster_word_weights.append({"cluster_id": cluster_id, "weight": uniform(0, 1)})
        node_list.append({"name": word, "type": "word", "weight": word_weight, "clusters": cluster_word_weights})

    edge_list = []
    for source in sources:
        for word in word_list:
            edge_force = randrange(0, 100)
            cluster_edge_forces = []
            for cluster_id in range(1, NUM_OF_CLUSTERS + 1):
                cluster_edge_force = randrange(0, 100)
                cluster_edge_forces.append({"cluster_id": cluster_id, "force": cluster_edge_force})
            edge_list.append({"source": source, "word": word, "force": edge_force, "clusters": cluster_edge_forces})

    force_list = {"nodes": node_list, "edges": edge_list}

    with closing(open(FORCE_FILE, "w")) as force_file:
        force_file.write(dumps(force_list))


def create_force_OLD():
    sources = ['repubblica.it', 'corriere.it', 'iltempo.it', 'ilsole24ore.com', 'padania.org', 'ilgiornale.it', 'panorama.it', 'ilsecoloxix.it', 'ilfattoquotidiano.it', 'lastampa.it', 'lagazzettadelmezzogiorno.it', 'unionesarda.it', 'ilmessaggero.it', 'ilgiorno.it', 'leggo.it', 'ilmattino.it', 'unita.it', 'ilmanifesto.it']
    word_list = ["cat", "dog", "mum", "spoon", "chair", "apple", "dot", "sea", "run", "try", "end", "big", "dive"]
    force_list = []
    for cluster_id in range(1, NUM_OF_CLUSTERS + 1):
        edge_list = []
        node_list = []
        for word in word_list:
            node_list.append({"node": word, "type": "word"})
        for source in sources:
            node_list.append({"node": source, "type": "source"})
            for i in range(0, 5):
                distance = randrange(0, 100)
                index = randrange(1, len(word_list) - 1)
                word = word_list[index]
                edge_list.append({"source": source, "word": word, "distance": distance})
        force_list.append({"cluster_id": cluster_id, "nodes": node_list, "edges": edge_list})

    with closing(open(FORCE_FILE, "w")) as force_file:
        force_file.write(dumps(force_list))

create_clusters()
create_timeline()
create_force()

import codecs, sys, json
from math import log, pow

edge_weights = []
edge_topic_weight = []
topics_ids = [1,4,6,7,8,12,13,14,15,16,17,18,19]
top_words = set([u"societ\xe0", u"monti", u"siria", u"rialzo", u"legge", u"dice", u"oggi", u"fornero", u"chiude", u"spettacolo", u"lavoro", u"spettacoli", u"nord", u"rischio", u"2012", u"borse", u"maroni", u"auto", u"merkel", u"de", u"notte", u"bis", u"germania", u"lazio", u"vendola", u"posti", u"formigoni", u"elettorale", u"crisi", u"crescita", u"parigi", u"btp", u"madrid", u"milan", u"video", u"cultura", u"giro", u"feriti", u"napolitano", u"banche", u"strada", u"solo", u"foto", u"europa", u"punti", u"spagna", u"lombardia", u"ora", u"inter", u"napoli", u"muore", u"gusto", u"renzi", u"sindacati", u"berlusconi", u"italiani", u"elezioni", u"protesta", u"belsito", u"alfano", u"accordo", u"usa", u"lega", u"tutta", u"spread", u"italia", u"pd", u"calo", u"arte", u"grecia", u"bossi", u"imprese", u"governo", u"obama", u"incidente", u"18", u"ancora", u"s\xec", u"ue", u"apre", u"tav", u"soldi", u"premier", u"romney", u"moto", u"morti", u"tosi", u"morto", u"affari", u"citt\xe0", u"primarie", u"juve", u"bund", u"no", u"scontro", u"torino", u"pdl", u"musica", u"giovani", u"bersani", u"sotto", u"appuntamenti", u"quota", u"senza", u"tasse", u"corteo", u"piazza", u"coppa", u"borsa", u"milano", u"prandelli", u"tagli", u"riforma", u"londra"])
category = {'ansa.it':'agenzie',
'asca.it':'agenzie',
'adnkronos.com':'agenzie',
'ilvelino.it':'agenzie',
'direttanews.it':'agenzie',
'agi.it':'agenzie',
'italpress.com':'agenzie',
'irispress.it':'agenzie',
'omniroma.it':'agenzie',
'italia-news.it':'agenzie',
'repubblica.it':'testate in edicola',
'corriere.it':'testate in edicola',
'iltempo.it':'testate in edicola',
'ilsole24ore.com':'testate in edicola',
'padania.org':'testate in edicola',
'ilgiornale.it':'testate in edicola',
'panorama.it':'testate in edicola',
'ilsecoloxix.it':'testate in edicola',
'ilfattoquotidiano.it':'testate in edicola',
'lastampa.it':'testate in edicola',
'lagazzettadelmezzogiorno.it':'testate in edicola',
'unionesarda.it':'testate in edicola',
'ilmessaggero.it':'testate in edicola',
'ilgiorno.it':'testate in edicola',
'leggo.it':'testate in edicola',
'ilmattino.it':'testate in edicola',
'unita.it':'testate in edicola',
'ilmanifesto.it':'testate in edicola',
'gazzetta.it':'testate in edicola',
'tuttosport.com':'testate in edicola',
'corrieredellosport.it':'testate in edicola',
'rai.it':'portali web',
'virgilio.it':'portali web',
'mediaset.it':'portali web',
'libero.it':'portali web',
'tiscali.it':'portali web',
'newnotizie.it':'portali web',
'sky.it':'portali web',
'quotidiano.net':'portali web',
'voceditalia.it':'portali web',
'la7.it':'portali web'
}

top_n_words_topic = {1: set([u"monti", u"governo", u"berlusconi", u"crescita", u"ue", u"tasse", u"bis", u"merkel", u"premier", u"napolitano"]), 4: set([u"italia", u"coppa", u"spagna", u"ue", u"tutta", u"germania", u"italiani", u"europa", u"giro", u"prandelli"]), 6: set([u"lega", u"maroni", u"bossi", u"nord", u"formigoni", u"lombardia", u"pdl", u"soldi", u"tosi", u"belsito"]), 7: set([u"citt\\xe0", u"oggi", u"appuntamenti", u"cultura", u"gusto", u"arte", u"spettacoli", u"societ\\xe0", u"spettacolo", u"musica"]), 8: set([u"lavoro", u"riforma", u"senza", u"fornero", u"giovani", u"governo", u"18", u"posti", u"accordo", u"sindacati"]), 12: set([u"napoli", u"juve", u"milan", u"lazio", u"inter", u"de", u"solo", u"foto", u"video", u"ancora"]), 13: set([u"borsa", u"milano", u"chiude", u"apre", u"calo", u"rialzo", u"europa", u"madrid", u"londra", u"parigi"]), 14: set([u"pdl", u"pd", u"primarie", u"bersani", u"berlusconi", u"renzi", u"legge", u"alfano", u"elettorale", u"vendola"]), 15: set([u"no", u"tav", u"dice", u"governo", u"s\\xec", u"piazza", u"tagli", u"protesta", u"corteo", u"torino"]), 16: set([u"auto", u"muore", u"morto", u"morti", u"incidente", u"notte", u"feriti", u"scontro", u"strada", u"moto"]), 17: set([u"crisi", u"ue", u"grecia", u"spagna", u"europa", u"banche", u"crescita", u"rischio", u"merkel", u"imprese"]), 18: set([u"ora", u"usa", u"obama", u"2012", u"romney", u"elezioni", u"tasse", u"siria", u"europa", u"crescita"]), 19: set([u"spread", u"punti", u"btp", u"bund", u"sotto", u"piazza", u"borse", u"chiude", u"affari", u"quota"])}

with codecs.open(sys.argv[1], "r") as mr_output:
	with open("timeline.json", "w") as timeline_f:

			force_file = open("force.json", "w")
			te_file = open("force_testate.json", "w")
			pw_file = open("force_portali.json", "w")
			a_file = open("force_agenzie.json", "w")

			sources = {}
			source_word = {}
			source_word_topic = {}
			word_topic = {}
			words = {}
			#timeline = topic -> list of dict with month_id, weight 
			timeline = []
			for i in topics_ids:
				timeline.append(None)

			for line in mr_output:
				elems = line.split("\t")
				key_list = json.loads(elems[0])
				value = float(elems[1])

				if key_list[0] == 0:
					#source
					sources[key_list[1]] = value
				elif key_list[0] == 1:
					#source word
					source = key_list[1]
					word = key_list[2]
					if word in top_words:
						word_dict = source_word.get(source, {})
						word_dict[word] = value
						source_word[source] = word_dict
				elif key_list[0] == 2:
					#source word topic
					source = key_list[1]
					word = key_list[2]
					topic_id = key_list[3]
					int_topic_id = int(topic_id) 

					if int_topic_id in topics_ids:
						if word in top_words:
							word_topic_dict = source_word_topic.get(source, {})
							topic_dict = word_topic_dict.get(word, {})
							topic_dict[int_topic_id] = value
							word_topic_dict[word] = topic_dict
							source_word_topic[source] = word_topic_dict
				elif key_list[0] == 3:
					#word topic
					word = key_list[1]
					topic_id = key_list[2]
					int_topic_id = int(topic_id)
					if word in top_words:
						if int_topic_id in topics_ids:
							topic_dict = word_topic.get(word, {})
							topic_dict[int_topic_id] = value
							word_topic[word] = topic_dict
				elif key_list[0] == 4:
					#word
					word = key_list[1]
					if word in top_words:
						words[word] = value
				elif key_list[0] == 5:
					#month topic
					date = key_list[1]
					topic_id = key_list[2]
					int_topic_id = int(topic_id)
					if int_topic_id in topics_ids:
						if timeline[topics_ids.index(int_topic_id)] == None:
							#print value
							timeline[topics_ids.index(int_topic_id)] = {"cluster_id":int_topic_id, "months":[
																{"month_id":date, "weight":pow(value, 2)}]}
						else:
							#print value
							months = timeline[topics_ids.index(int_topic_id)]["months"]
							months.append({"month_id":date, "weight":pow(value, 2)})
				elif key_list[0] == 6:
					#source topic
					pass

			mr_output.close()

			#dump timeline json
			json.dump(timeline, timeline_f)
			timeline_f.close()

			#create source nodes
			nodes = []
			nodes_te = []
			nodes_pw = []
			nodes_a = []

			for source, value in sources.iteritems():
				node = {}
				node["type"] = "source"
				node["name"] = source
				node["weight"] = value
				# !!!! will be changed !!!!!
				clusters = []
				for i in topics_ids:
					clusters.append({"cluster_id":i, "weight":value})
				node["clusters"] = clusters
				nodes.append(node)
				if category[source] == "testate in edicola":
					nodes_te.append(node)
				elif category[source] == "portali web":
					nodes_pw.append(node)
				elif category[source] == "agenzie":
					nodes_a.append(node)

			#create word nodes
			for word, value in words.iteritems():
				node = {}
				node["type"] = "word"
				node["name"] = word
				node["weight"] = value
				clusters = []
				for i in topics_ids:
					word_topic_value = word_topic[word].get(i, None)
					if word_topic_value != None:
						clusters.append({"cluster_id":i, "weight":word_topic_value})
				node["clusters"] = clusters
				nodes.append(node)
				nodes_te.append(node)
				nodes_pw.append(node)
				nodes_a.append(node)

			#create edges
			edges = []
			edges_te = []
			edges_pw = []
			edges_a = []

			for source, word_dict in source_word.iteritems():
				for word, value in word_dict.iteritems():
					edge = {}
					edge["source"] = source
					edge["word"] = word
					force = value / sources[source]
					if force >= 0.0025:
						edge["force"] = log(force)
						edge_weights.append(force)
						clusters = []
						for i in topics_ids:
							num = source_word_topic[source][word].get(i, 0.0)
							den = word_topic[word].get(i, 0)
							if den > 0:
								t_force = num/den
								if t_force > 0.0:
									clusters.append({"cluster_id":i, "force":log(t_force)})
									edge_topic_weight.append(t_force)
						edge["clusters"] = clusters
						edges.append(edge)
						if category[source] == "testate in edicola":
							edges_te.append(edge)
						elif category[source] == "portali web":
							edges_pw.append(edge)
						elif category[source] == "agenzie":
							edges_a.append(edge)

			force = {"nodes":nodes, "edges":edges}
			force_te = {"nodes":nodes_te, "edges":edges_te}
			force_pw = {"nodes":nodes_pw, "edges":edges_pw}
			force_a = {"nodes":nodes_a, "edges":edges_a}

			#dump force json
			json.dump(force, force_file)
			force_file.close()
			json.dump(force_te, te_file)
			te_file.close()
			json.dump(force_pw, pw_file)
			pw_file.close()
			json.dump(force_a, a_file)
			a_file.close()

			print "Edge min " + str(log(min(edge_weights)))
			print "Edge avg " + str(log(sum(edge_weights)/len(edge_weights)))
			print "Edge max " + str(log(max(edge_weights)))
			print "Edge topic min " + str(log(min(edge_topic_weight)))
			print "Edge topic avg " + str(log(sum(edge_topic_weight)/len(edge_topic_weight)))
			print "Edge topic max " + str(log(max(edge_topic_weight)))
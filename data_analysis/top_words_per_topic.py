import codecs, sys, json

f_in = codecs.open(sys.argv[1], "r", "utf-8")
f_out = codecs.open(sys.argv[2], "w", "utf-8")

topics_ids = set([1,4,6,7,8,12,13,14,15,16,17,18,19])
top_n_words = 10

word_per_topic = {}
words = None
pervius_topic_id = None
for line in f_in:
	elems = line.split(",")
	selected_topic = False
	for idx, elem in enumerate(elems):
		if idx == 0:
			if int(elem) in topics_ids:
				if words != None and pervius_topic_id != None:
					word_per_topic[pervius_topic_id] = words
				selected_topic = True
				pervius_topic_id = int(elem)
				words = []
			else:
				selected_topic = False
		elif selected_topic == True and idx <= top_n_words:
			word = elem.split("=")[0].encode('unicode-escape')
			words.append(word)
	word_per_topic[pervius_topic_id] = words
f_in.close()
json.dump(word_per_topic, f_out)
f_out.close()
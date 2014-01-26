import codecs, sys, json

with codecs.open(sys.argv[1], "r") as topics_f:
	with open(sys.argv[2], "w") as json_f:
		topics_list = []
		for line in topics_f:
			topic_dict = {}
			words_list = []
			elems = line.split(",")
			for idx, elem in enumerate(elems):
				if idx == 0:
					topic_dict["cluster_id"] = int(elem)
				else:
					word_value = elem.split("=")
					words_list.append({"name": word_value[0], "weight": float(word_value[1])})
			topic_dict["words"] = words_list
			topics_list.append(topic_dict)
		topics_f.close()
		json.dump(topics_list, json_f)
		json_f.close()
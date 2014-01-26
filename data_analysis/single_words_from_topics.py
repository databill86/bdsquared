import codecs, sys

f_in = codecs.open(sys.argv[1], "r", "utf-8")
f_out = codecs.open(sys.argv[2], "w", "utf-8")

topics_ids = set([1,4,6,7,8,12,13,14,15,16,17,18,19])
top_n_words = 10

words = set()
for line in f_in:
	elems = line.split(",")
	selected_topic = False
	for idx, elem in enumerate(elems):
		if idx == 0:
			if int(elem) in topics_ids:
				selected_topic = True
			else:
				selected_topic = False
		elif selected_topic == True and idx <= top_n_words:
			print elem
			words.add(elem.split("=")[0])
f_in.close()
for idx, word in enumerate(words):
	if idx == 0:
		f_out.write('u"')
	else:
		f_out.write(', u"')
	f_out.write(word.encode('unicode-escape'))
	f_out.write('"')
f_out.close()
from contextlib import closing
from language_cleaning import LCleaner
import sys, codecs, pickle, time, resource

def main():
	cleaner = LCleaner()

	H_dump = open(sys.argv[2], "r")
	H = pickle.load(H_dump)
	H_dump.close()

	with closing(codecs.open(sys.argv[1], "r", "utf-8")) as f_in:
		with closing(codecs.open(sys.argv[3], "w", "utf-8")) as f_out:
			idx = 0
			for line in f_in:
				datapoint = line.replace('\|', '').split('|')
				datapoint[4] = cleaner.clean_string(datapoint[4])
				datapoint[-1] = datapoint[-1].replace("\n", "")
				f_out.write('|'.join(datapoint))
				f_out.write('|' + topics(H, idx) + '\n')
				idx += 1

def topics(H, title_num):
	topic_vals = []
	for topic_idx, topic_val in enumerate(H[title_num,:]):
		topic_vals.append('='.join([str(topic_idx + 1), str(topic_val)]))
	return ','.join(topic_vals)


if __name__ == '__main__':
	main()
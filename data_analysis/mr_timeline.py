from mrjob.job import MRJob
from mrjob.protocol import (
    JSONValueProtocol,
    JSONProtocol,
)
from collections import defaultdict 
import re
import string

class MRWordFrequencyCountJob(MRJob):

    #INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONProtocol

    def steps(self):
        return [self.mr(
            mapper=self.mapper,
            combiner=self.sum_values,
            reducer=self.sum_values
        )]

    def mapper(self, _, line):
        elems = line.replace('\|', ' ').split('|')
        date = elems[1][0:-3]
        print date
        topics_list = elems[-1].split(",")
        for topic in topics_list:
            word_value = topic.split("=")
            topic_id = word_value[0]
            topic_val = float(word_value[1])
            yield [date, topic_id], topic_val
 
    def sum_values(self, date_topic, vals):
        yield date_topic, sum(vals)

if __name__ == '__main__':
    MRWordFrequencyCountJob.run()
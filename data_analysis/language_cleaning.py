
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import re, string

class LCleaner:
    punct_re = re.compile('[%s]' % re.escape(string.punctuation))
    spaces_re = re.compile(" +")
    it_stopwords = [unicode(sw, "utf-8") for sw in stopwords.words('italian')]
    it_stopwords.extend([u'fa', u'due', u'tre', u"dopo", u"d\xa0", u"vent", u"aver", u"via", u"s\xac"])

    def clean_data(self, data_list):
        #element of the list = [id, title, source, timestamp]
        for data_point in data_list:
            data_point[1] = self.clean_string(data_point[1])
            yield data_point

    def clean_string(self, string):
        words = [w for w in wordpunct_tokenize(string.lower()) if not w in self.it_stopwords and len(w) > 1]
        return self.spaces_re.sub(' ', self.punct_re.sub(' ', ' '.join(words))).strip()

if __name__ == '__main__':
    cleaner = LCleaner()
    data = []
    data.append([1, u"Ciao, mi \xa8 chiamo Piero, il lo con la a i gli e le?", "ansa.it", "oggi"])
    data.append([2, u"Ciao, mi chiamo domani, il di lo a i gli e le! anche se non mi diverto", "repubblica.it", "ieri"])
    clean_data = cleaner.clean_data(data)
    for datapoint in clean_data:
        print datapoint
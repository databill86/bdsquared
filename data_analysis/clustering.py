from contextlib import closing
from sklearn.feature_extraction import text
from sklearn import decomposition
from sklearn.preprocessing import normalize
from language_cleaning import LCleaner
import sys, codecs, pickle, time, resource

def main():

    tot_time1 = time.time()

    cleaner = LCleaner()
    titles = []

    print "Loading titles"

    time1 = time.time()

    with closing(codecs.open(sys.argv[1], "r", "utf-8")) as f:
        for line in f:
            title = line.replace('\|', '').split('|')[4]
            title = cleaner.clean_string(title)
            #print title
            titles.append(title)

    time2 = time.time()
    print ' took %0.3f ms' % ((time2-time1)*1000.0)

    print "Building TfIdf matrix"

    time1 = time.time()

    vectorizer = text.TfidfVectorizer(max_df=0.95, max_features=20000)
    X = vectorizer.fit_transform(titles)

    time2 = time.time()
    print ' took %0.3f ms' % ((time2-time1)*1000.0)

    print "Decomposing with NNMF"

    time1 = time.time()

    nmf = decomposition.NMF(n_components=20)
    H = nmf.fit_transform(X)
    normalize(H, norm='l1', axis=1, copy=False)
    
    W = nmf.components_
    normalize(W, norm='l1', axis=1, copy=False)

    with closing(codecs.open("W.dump", "w", "utf-8")) as nnmf_dump:
        pickle.dump(nmf.components_, nnmf_dump)

    with closing(codecs.open("H.dump", "w", "utf-8")) as nnmf_dump:
        pickle.dump(H, nnmf_dump)

    time2 = time.time()
    print ' took %0.3f ms' % ((time2-time1)*1000.0)

    print "Printing topics"

    n_top_words = 20
    feature_names = vectorizer.get_feature_names()

    with closing(codecs.open("topics.txt", "w", "utf-8")) as out:
        for topic_idx, topic in enumerate(nmf.components_):
            out.write("%d," % (topic_idx + 1))
            words_values = []
            columns =  topic.argsort()[:-n_top_words - 1:-1]

            '''
            sum_val = 0.0
            for column in columns:
                sum_val += topic[column]

            for column in columns:
                topic[column] = topic[column] / sum_val
            '''

            for column in columns:
                if (topic[column] > 0.0):
                    words_values.append("=".join([feature_names[column], str(topic[column])]))
            out.write(",".join(words_values))
            out.write("\n")
    '''
    for i in xrange(0, 5):
        print titles[i]
        print H[i,:]
        print
    '''

    tot_time2 = time.time()
    print 'Total time %0.3f ms' % ((tot_time2-tot_time1)*1000.0)
    print 'Max ram usage %s Kb' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

if __name__ == '__main__':
    main()

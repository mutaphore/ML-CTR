#!/usr/local/bin/python
import os
import sys
import gc

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split

from clean import parse_data

if __name__ == '__main__':
    f_train = 'train10k'
    f_test = 'test'

    print "Parsing data..."
    YX = parse_data(f_train, combine=True)
    YX_train, YX_test = train_test_split(YX, test_size=0.1,
        random_state=42)
        # random_state=np.random.random_integers(100000))
    X_train = np.array(YX_train)[:,1:]
    Y_train = np.array(YX_train)[:,0]
    X_test = np.array(YX_test)[:,1:]
    Y_test = np.array(YX_test)[:,0]
    print "Training NB classifier..."
    clf = GaussianNB()
    clf.fit(X_train, Y_train)
    print "Cross validating..."
    score = clf.score(X_test, Y_test)
    print "CV score on test data %r " % score

    # Now predict real test data
    print "Parsing test data..."
    X_test = parse_data(f_test)[0]
    print "Predicting..."
    prob = clf.predict_proba(X_test)
    print "Writing probs..."
    f_out = open("nb_prob", 'w')
    for row in prob:
        f_out.write(str(row[0]) + '\n')
    f_out.close()

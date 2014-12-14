#!/usr/local/bin/python
import os
import sys
import gc

import numpy as np
from sklearn.naive_bayes import GaussianNB

from clean import parse_data

if __name__ == '__main__':
    f_train = 'train10k'
    f_test = 'test'

    print "Parsing train data..."
    X_train, Y_train = parse_data(f_train)
    print "Training NB classifier..."
    clf = GaussianNB()
    clf.fit(X_train, Y_train)
    score = clf.score(X_train, Y_train)
    print "Score on train data %r " % score

    # Free memory we don't use
    X_train = None
    Y_train = None
    gc.collect()

    print "Parsing test data..."
    X_test = parse_data(f_test)[0]
    print "Predicting..."
    prob = clf.predict_proba(X_test)
    print "Writing probs..."
    f_out = open("nb_prob", 'w')
    for row in prob:
        f_out.write(str(row[0]) + '\n')
    f_out.close()

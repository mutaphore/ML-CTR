#!/usr/local/bin/python

from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

from clean import parse_data

D = 2 ** 20             # number of weights to use

if __name__ == '__main__':
    f_train = 'train10k'
    f_test = 'test'

    print "Parsing train data..."
    X_train, Y_train = parse_data(f_train)
    print "Training Logistic Regression classifier..."
    clf = LogisticRegression()
    clf.fit(X_train, Y_train)
    print "Cross validating..."
    data = zip(x_train, Y_train)

    score = clf.score(X_train, Y_train)
    print "Score on train data %r " % score

    # print "Parsing test data..."
    # X_test = parse_data(f_test)[0]
    # print "Predicting..."
    # prob = clf.predict_proba(X_test)
    # print "Writing probs..."
    # f_out = open("lr_prob", 'w')
    # for row in prob:
    #     f_out.write(str(row[0]) + '\n')
    # f_out.close()

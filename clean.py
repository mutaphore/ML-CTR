#!/usr/local/bin/python

#  Data pre/post processing utility functions
#  By: Dewei Chen
#
#  Output filename convention: *c -> clean, *e -> encoded

import os
import sys
from csv import DictReader

#import numpy as np
#from sklearn.preprocessing import OneHotEncoder

nheader = 'click,day(0-6),hour(0-23),C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21\n'
sheader = 'id,click\n'

D = 2 ** 20             # number of weights to use

def data(path, D):
    ''' GENERATOR: Apply hash-trick to the original csv row
                   and for simplicity, we one-hot-encode everything

        INPUT:
            path: path to training or testing file
            D: the max index that we can hash to

        YIELDS:
            ID: id of the instance, mainly useless
            x: a list of hashed and one-hot-encoded 'indices'
               we only need the index since all values are either 0 or 1
            y: y = 1 if we have a click, else we have y = 0
    '''

    for t, row in enumerate(DictReader(open(path))):
        # process id
        ID = row['id']
        del row['id']

        # process clicks
        y = 0
        if 'click' in row:
            if row['click'] == '1':
                y = 1
            del row['click']

        time = int(row['hour'])
        day = ((time - 14100000) / 100 + 1) % 7     # Day Mon-Sun 0-6
        hour = time % 100                           # Hours: 0-23

        # build x
        x = []
        for key in row:
            value = row[key]

            # one-hot encode everything with hash trick
            index = abs(hash(key + '_' + value)) % D
            x.append(index)

        yield t, day, hour, ID, x, y


# Used for post processing nb.py output
def combine_testprob():
    f_in1 = open('test', 'r')
    f_in2 = open('nb_prob', 'r')
    f_out = open('submission_nb.csv', 'w')
    count = 0;

    f_in1.readline()   # Skip header
    f_out.write(sheader)
    line1 = f_in1.readline()
    line2 = f_in2.readline()
    while line1 and line2:
        f_out.write(line1.split(',')[0] + ',' + line2)
        sys.stdout.write("Line %d \r" % count)
        sys.stdout.flush()
        line1 = f_in1.readline()
        line2 = f_in2.readline()
        count += 1

    f_in1.close()
    f_in2.close()
    f_out.close()


# Read in the data file and outputs a file containing the encodings, we do
# this as a separate step because we can't read in all the values to memory
def one_hot_encode():
    f_in = open('train10kc', 'r')
    f_out = open('encoding', 'w')
    mat = []
    count = 0

    # Read in the matrix
    f_in.readline()   # Skip header
    line = f_in.readline()
    while line:
        row = [float(x)/100000 for x in line.split(',')]
        mat.append(row[5:14])
        line = f_in.readline()
        sys.stdout.write("Line %d \r" % count)
        sys.stdout.flush()
        count += 1

    print "Done generating matrix, encoding..."

    # Encode it and write to file
    enc = OneHotEncoder(dtype=np.integer)
    enc.fit(mat)

    print enc.n_values_
    print enc.feature_indices_

    enc_mat = enc.transform(mat).toarray()
    for i, row in enumerate(enc_mat):
        f_out.write(''.join(map(str, row)) + '\n')
        sys.stdout.write("Line %d \r" % i)
        sys.stdout.flush()


def clean_data(f_in, f_out, train=True):
    with open(f_out, 'w') as outfile:
        outfile.write(nheader)
        count = 0
        for t, day, hour, ID, x, y in data(f_in, D):  # data is a generator
            row =  [day, hour] + x
            if train:
                row.insert(0, y)
            outfile.write(','.join(map(str, row)) + '\n')
            sys.stdout.write("Line %d \r" % count)
            sys.stdout.flush()
            count += 1


if __name__ == '__main__':
    #one_hot_encode()
    train_in = 'train1M'
    train_out = 'train1Mc'
    test_in = 'test'
    test_out = 'testc'
    clean_data(train_in, train_out)

#!/usr/local/bin/python

# Subsample training/test dataset

import os
import sys
import random
import linecache

from clean import data

# Old Header:
# id,click,hour,C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21
# New Header:
nheader = 'click,day(0-6),hour(0-23),C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21\n'
m = 40428967            # Number of samples in train
D = 2 ** 20             # number of weights to use

def random_sample(file_in, file_out):
    f_in = open(file_in, 'r')
    f_out = open(file_out, 'w')
    samples = sorted(random.sample(xrange(m), 10000))

    print "Done randomizing, writing to output file..."

    # Write header
    header = f_in.readline()
    f_out.write(header)

    count = 0
    while count < m:
        if not samples:
            break
        line = f_in.readline()
        if count == samples[0]:
            del samples[0]
            f_out.write(line)
            sys.stdout.write("Line %d \r" % count)
            sys.stdout.flush()
        count += 1
    f_in.close()
    f_out.close()

# Since test data is only on Friday, we subsample only Friday data from train
def filter_day(file_in, file_out):
    f_out = open(file_out, 'w')
    for t, day, hour, ID, x, y in data(file_in, D):  # data is a generator
        if day == 4:
            line = linecache.getline(file_in, t + 1)
            f_out.write(line)
        sys.stdout.write("Line %d Day %d\r" % ((t + 1), day))
        sys.stdout.flush()


if __name__ == '__main__':
    # random_sample('train', 'train10k')
    filter_day('train', 'trainf4')

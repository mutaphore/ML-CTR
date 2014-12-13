#!/usr/local/bin/python

# Subsample training/test dataset

import os
import sys
import random

# Old Header:
# id,click,hour,C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21
# New Header:
nheader = 'click,day(0-6),hour(0-23),C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21\n'
m = 40428967

if __name__ == '__main__':
    f_in = open("train", 'r')
    f_out = open("train10k", 'w')
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

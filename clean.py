#!/usr/local/bin/python

#  Data pre/post processing utility functions
#  By: Dewei Chen
#
#  Output filename convention: *c -> clean, *e -> encoded

import os
import sys

from sklearn.preprocessing import OneHotEncoder

nheader = 'click,day(0-6),hour(0-23),C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21\n'
sheader = 'id,click\n'

# Given a line return an array of cleaned items
def clean_line(line, train=True):
   if train:
      shift = 0
   else:
      shift = -1  # Shift 1 for test data since we don't have the label column
   items = line.split(',')
   # Convert hex strings to integers indices 5-13
   for i in range(5, 14):
      items[i + shift] = int(items[i + shift], 16)
   # Remove useless ID field
   items.pop(0)
   # Split time field into Day and Hours fields
   time = int(items[1 + shift])
   items[1 + shift] = str(((time - 14100000) / 100 + 1) % 7) # Day Mon-Sun 0-6
   items.insert(2 + shift, str(time % 100))                  # Hours: 0-23

   return ",".join(items)


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


def one_hot_encode():
   f_in = open('trainsmall', 'r')
   f_out = open('trainsmalle', 'w')

   f_in.readline()   # Skip header
   line = f_in.readline()
   mat = []
   while line:
      mat.append([float(x) for x in line.split(',')])
      line = f_in.readline()

   enc = OneHotEncoder(categorical_features=[5,6,7,8,9,10,11,12,13])

def clean_test():
   f_in = open('test', 'r')
   f_out = open('testc', 'w')
   count = 0

   f_in.readline()
   f_out.write(nheader)
   line = f_in.readline()
   while line:
      line = clean_line(line, train=False)
      f_out.write(line)
      line = f_in.readline()
      sys.stdout.write("Line %d \r" % count)
      sys.stdout.flush()
      count += 1

if __name__ == '__main__':
   combine_testprob()

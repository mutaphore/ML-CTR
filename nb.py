#!/usr/local/bin/python
import os
import sys
import numpy as np
from sklearn.naive_bayes import GaussianNB

def parse_x(items):
   x = []
   for i, item in enumerate(items):
      if i > 3 and i < 13: 
         x.append(int(item, 16))
      else:
         x.append(int(item))    
   return x


def parse_data(fname, train=True):
   f_in = open(fname, 'r') 
   Y = []
   X = []
   f_in.readline()   # Skip header
   count = 0

   line = f_in.readline()   # Skip header
   while line:
      items = line.split(',')
      if train:
         Y.append(int(items[0]))
         X.append(parse_x(items[1:]))  
      else:
         X.append(parse_x(items))
      line = f_in.readline()
      sys.stdout.write("Line %d \r" % count)
      sys.stdout.flush()
      count += 1

   f_in.close()
   return X, Y
   
   
if __name__ == '__main__':
   f_train = 'trainsmall'
   f_test = 'testc'

   print "Parsing data..."   
   X_train, Y_train = parse_data(f_train)
   X_test = parse_data(f_test, train=False)[0]
      
   print "Training NB classifier..."
   clf = GaussianNB()
   clf.fit(X_train, Y_train)

   print "Predicting..."
   prob = clf.predict_proba(X_test)

   print "Writing probs..."
   f_out = open("nb_prob", 'w')
   for row in prob:
      f_out.write(str(row[0]) + '\n')
   f_out.close()

#!/usr/local/bin/python

import os
import sys
import random

from clean import clean_line

# Old Header:
# id,click,hour,C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21
# New Header:
nheader = 'click,day(0-6),hour(0-23),C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21\n'
m = 40428967

if __name__ == '__main__':
   f_in = open("train", 'r')
   f_out = open("train1Mc", 'w')
   samples = sorted(random.sample(xrange(m), 1000000))
   #samples = sorted(random.sample(xrange(m), 10000))
   
   print "Done randomizing, writing to file..."   

   # Write header
   oheader = f_in.readline()
   #f_out.write(oheader)
   f_out.write(nheader)

   count = 0
   while count < m:
      if not samples:
         break
      line = f_in.readline()
      if count == samples[0]:
         del samples[0]
         line = clean_line(line)
         f_out.write(line)
         sys.stdout.write("Line %d \r" % count)
         sys.stdout.flush()
      count += 1

   f_in.close()
   f_out.close()

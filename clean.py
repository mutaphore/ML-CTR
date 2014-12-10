#!/usr/local/bin/python
import os
import sys

nheader = 'click,day(0-6),hour(0-23),C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21\n'

def clean_line(line, train=True):
   if train:
      shift = 0
   else:
      shift = 1
   items = line.split(',')
   items.pop(0)   # Remove useless ID field
   time = int(items[1 - shift])
   items[1 - shift] = str(((time - 14100000) / 100 + 1) % 7)      # Day: Mon-Sun -> 0-6
   items.insert(2 - shift, str(time % 100))                       # Hours: 0-23
   return ",".join(items)


if __name__ == '__main__':
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

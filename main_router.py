#!/usr/bin/python

import threading
import time
from eqp import Eqp

class myThread (threading.Thread):
   """Uma classe para uma thread"""

   def __init__(self, threadID, name, obj):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.obj = obj
      
   def run(self):
      print ("Starting " + self.name)
      ponte(self.obj)


def ponte(obj):
   obj.auto_gen_msg()
   



equips = [Eqp() for i in range(666)]

threads = [myThread(equips.index(i), i.tag, i) for i in equips]

for thread in threads:
   thread.start()

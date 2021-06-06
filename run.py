from bot1 import*
import os, threading
#=========================================================
a1 = Bardiansyah1(_id="email",passwd="pasword",type=0)
A1 = threading.Thread(target=a1.run1, args=()).start()
#=========================================================
print("ALL BOTS RUNING")
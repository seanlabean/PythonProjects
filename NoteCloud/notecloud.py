import numpy as np
import matplotlib.pyplot as plt

f = open('./2022daily.txt', 'r')
l = f.readlines()
ratings = []
for w in l:
    w = w.strip()
    if w[-3:] == "/10":
        try:
            r = float(w[-6:-3].strip(": "))
        except:
            r = float(w[-5:-3].strip(": "))
        ratings.append(r)
f.close()
print(ratings)

score_counter = {"0.0" : 0, "0.5" : 0, "1.0" : 0, "1.5" : 0,
                 "2.0" : 0, "2.5" : 0, "3.0" : 0, "3.5" : 0,
                 "4.0" : 0, "4.5" : 0, "5.0" : 0, "5.5" : 0,
                 "6.0" : 0, "6.5" : 0, "7.0" : 0, "7.5" : 0,
                 "8.0" : 0, "8.5" : 0, "9.0" : 0, "9.5" : 0,
                 "10.0" : 0
                 }
for s in ratings:
    score_counter[str(s)] += 1
print(score_counter)

plt.figure(figsize=(8,6))
plt.hist(ratings)
plt.savefig("notecloud.jpeg")

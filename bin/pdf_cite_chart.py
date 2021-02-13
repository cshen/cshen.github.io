#!/usr/bin/env python2.7




import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import json

with open('../data/cs_cite.json') as jdata:
    d = json.load( jdata )
    # print (d)
    # print len(d["data"])

l = len( d["data"] )

xx=[]
yy=[]
for i in range(l):
    xx.append ( d["data"][i][0] )
    yy.append ( d["data"][i][1] )

ax1 = plt.axes(frameon=False)


bar_width = 0.64
opacity = 0.576

# plt.plot(xx, yy, 'ro')
plt.bar(xx, yy, bar_width, alpha=opacity, facecolor='#9999ff', edgecolor='red', align='center')

plt.xlim( xx[0] - 1 , xx[l-1] + 1 )

plt.xlabel('year')
plt.ylabel('citaions')
plt.grid(True)

# cur_axes = plt.gca()
# cur_axes.axes.get_xaxis().set_visible(False)
# cur_axes.axes.get_yaxis().set_visible(False)
# plt.show()


pp = PdfPages('cs_cite.pdf')
pp.savefig()
pp.close()
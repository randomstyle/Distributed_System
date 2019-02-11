"""
Question:
Pick one IP from each region, find network latency from via the below code snippet
(ping 3 times), and finally sort the average latency by region.
http://ec2-reachability.amazonaws.com/
Expected Output for all 15 regions:
1. us-west-1 [50.18.56.1] - 100ms (Smallest average latency)
2. xx-xxxx-x [xx.xx.xx.xx] - 200ms
3. xx-xxxx-x [xx.xx.xx.xx] - 300ms
...
15. xx-xxxx-x [xx.xx.xx.xx] - 1000ms (Largest average latency)
"""
from __future__ import print_function
import subprocess
import requests
from lxml import html

# get html contents, manipulate and extract meaningful data and append in dataList 
res = requests.get("http://ec2-reachability.amazonaws.com").text
doc = html.fromstring(res)
dataList = doc.xpath('//tr/td/text()')

myList = []
si = 0
i = 0
myList.append(dataList[0])
myList.append(dataList[2])

while i < len(dataList)-3:
    if dataList[i] != dataList[si]:
        myList.append(dataList[i])
        myList.append(dataList[i+2])
    si = i
    i += 3

# get ping the servers from dataList, store in a list of tuples
c = 0
myList1 = []
for temp in range(15):
    
    ping = subprocess.Popen(
        ["ping", "-c", "3", myList[c+1]],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    out, error = ping.communicate()
    tempList = out.decode().split("/")
    item = (myList[c], myList[c+1], float(tempList[4]))
    myList1.append(item)
    c += 2

# sort the list in increasing order base on ping
myList1.sort(key=lambda item:item[2])

# print out according to the format
for temp in range(15):
    print (temp+1, end='')
    print (". %s [%s] - %fms"  % myList1[temp])

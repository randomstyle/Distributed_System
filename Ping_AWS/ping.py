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
import urllib.request

# get html contents, manipulate and extract meaningful data and append in dataList 
link = "http://ec2-reachability.amazonaws.com"
f = urllib.request.urlopen(link)
loadHTML = f.read()
myString = loadHTML.decode().replace(' ', '').replace('\n', '').replace('\t', '')
dataList = []
begI = 0

for temp in range(15):
    tempBeginI = myString.index("<tr><th>Region</th><th>IPPrefix</th><th>IP</th><th>Test</th></tr>", begI)
    tempEndI = myString.index('</td><tdid="test"><imgsrc="', tempBeginI)
    dataList.append(myString[tempBeginI+len("<tr><th>Region</th><th>IPPrefix</th><th>IP</th><th>Test</th></tr>")+8:tempEndI]);
    begI = tempEndI

# get ping the servers from dataList, store in a list of tuples
myList = []
for temp in range(15):
    t = dataList[temp].split("</td><td>")
    host = t[0]
    hostIP = t[2]
    
    ping = subprocess.Popen(
        ["ping", "-c", "3", hostIP],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    out, error = ping.communicate()
    tempList = out.decode().split("/")
    item = (host, hostIP, float(tempList[4]))
    myList.append(item)

# sort the list in increasing order base on ping
myList.sort(key=lambda item:item[2])

# print out according to the format
for temp in range(15):
    print (temp+1, end='')
    print (". %s [%s] - %fms"  % myList[temp])

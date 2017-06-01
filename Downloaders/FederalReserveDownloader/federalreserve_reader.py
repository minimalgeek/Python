import urllib.request
from bs4 import BeautifulSoup

def readAllDatesAndWrite(data, file):
    dom = BeautifulSoup(data, 'html.parser')
    ths = dom.findAll("th", {"class":"year"})
    for thElement in ths:
        spans = thElement.findAll("span")
        left = spans[0].get_text()
        right = spans[1].get_text()
        file.write(right + ", " + left + "\n")
    
f = open('datas.txt', 'w')
for i in range(1936, 2011):
    u = urllib.request.urlopen('https://www.federalreserve.gov/monetarypolicy/fomchistorical' + str(i) + '.htm')
    data = u.read()
    readAllDatesAndWrite(data, f)
f.close()


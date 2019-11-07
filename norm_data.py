import csv
from urllib.parse import urlparse

f = open('model/dataset_out.csv', 'w',newline='', encoding='utf-8')
writer = csv.writer(f)
data = []
with open('model/dataset.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        url, label = row
        url = url.strip()
        o = urlparse(url)
        # print(o.scheme)
        if o.scheme == '' or o.scheme == None:
            url = "http://"+url
        data.append([url, label])

writer.writerows(data)

print('done')

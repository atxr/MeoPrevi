# Grab the prevision of important satellites
import wget 

previ = []
sat = {'lageos 1': 8820,
       'lageos 2': 22195,
       'etalon 1': 19751,
       'etalon 2': 20026,
       'starlette': 7646,
       'ajissai': 16908,
       'larets': 27944,
       'lares': 38077}

satid = sat['lageos 1']

# TODO find how to wget with the 'tous' instead of 'visible'
url = 'https://heavens-above.com/PassSummary.aspx?lat=43.751&lng=6.9164&loc=Caussol&alt=0&tz=CET'+'&satid='+str(satid)

filename = wget.download(url)
print(filename)
with open(filename, 'r') as page:
    lines = page.readlines()

line = ""
for x in lines:
    if 'clickableRow' in x:
        line = x

#clean the line
line=line.replace('\n', '')
line=line.replace('\t', '')

#split differents lines
line = line.split('</tr>')[:-1] # the last element is an empty string
line = [x[x.find('>')+1:] for x in line]      # the first <tr ... > balise isn't important

#split differents rows in each lines
line = [x.split('</td>')[:-1] for x in line][:-1] # the last element of each split is an empty string

id_day = 0
id_debut = 2
id_angle_culm = 6
id_fin = 8

for passage in line:
    print(passage[id_angle_culm][-3:-1])
    if int(passage[id_angle_culm][-3:-1]) > 20:
        previ.append(('test', passage[id_day], passage[id_debut], passage[id_fin]))

print(previ)


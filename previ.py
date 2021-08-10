# Grab the prevision of important satellites
import wget 

sat = {'lageos 1': 8820,
       'lageos 2': 22195,
       'etalon 1': 19751,
       'etalon 2': 20026,
       'starlette': 7646,
       'ajissai': 16908,
       'larets': 27944,
       'lares': 38077}

# TODO find how to wget with the 'tous' instead of 'visible'
link = 'https://heavens-above.com/PassSummary.aspx?lat=43.751&lng=6.9164&loc=Caussol&alt=0&tz=CET'+'&satid='+satid

filename = wget.download(url)
with open(filename, 'r') as page:
    lines = page.getlines()


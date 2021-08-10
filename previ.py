# Grab the prevision of important satellites
#import wget 
import os

previ = []
sats = {
       'lageos 1 ': 8820,
       'lageos 2 ': 22195,
       'etalon 1 ': 19751,
       'etalon 2 ': 20026,
       'starlette': 7646,
       'ajissai  ': 16908,
       'larets   ': 27944,
       'lares    ': 38077}

for sat in sats:
    
    satid = sats[sat]

    # TODO find how to wget with the 'tous' instead of 'visible'
    url = "'https://heavens-above.com/PassSummary.aspx?lat=43.7413&lng=6.9&loc=Caussol&alt=0&tz=CET&satid="+str(satid)+"'"

    curl = "curl -o 'curl.data' "+url+" \
  --data-raw '__EVENTTARGET=ctl00%24cph1%24radioAll&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=tTUlb35TLZNOOmzVp10Nt5zkI%2Fvwj3yWH%2FM%2Fp%2FxPdVj2qdfiTPHFrZUf6sqIAwWhLDQYVdNSPZyEZJC856lLx0sh0G1bEv6z9U3RccIOdi2EAu3Bj%2Fm2pMj4BYmhbh%2B5fnMhPhXdrei%2Bq4PPWN3GXTravZnbp3W6wxfm90VoSRO1sxHcvaPMFbjSz3kBesRrI2v7RVM5euO6SUYnSJB1I8RXehwOSRYv5PJgpXR7ou1GL0BfEmmiLKwkBVqiUKQ4UTKDIX2sFi11dLw%2B0TBkPPYX8saD2E0kC1ZxyClavXKf3FdK32%2F4%2F1pRZhzeBCTqyPBk4uObDnUr7PbtNul2kPPDvIA15Xcl6O%2FiEoPCQOXhbBbW05mR76btiv47g3PvLOVFMFj%2F3V%2FxXIv9zaqmCGBdvGgJqIGPqcevNf7gTL7pQPPb6oUGptSTllxK9TIn5qy3TiYHsPZ6q5ZtY%2FbaI7u3M5fNa5FYDOHuRYUxKW%2BhZj7X1wEOcE%2Bx7fExXDOOXwjWHZi4Wb4jr3BP%2BytFD05iWViMxXws6POOOgrbtCEztcLnVTztBwJBqYB252iw1JoA4LpaSwBI7BiV1k5clGqHZZHiNle9d1AiQuTzIvH72wawQ2s7gIfn7zNDYozpQ8dIPzR1%2BHFnSQaay9Ktb63C4zLVRs63G5%2BeqSVQXcfLc7ArJ%2BnZOqG9JBQzxJ0%2F0uMBaniD9XacU54xQtS%2FsgxRvm2fPQcwa%2BiI5bD%2FXqqRWLkkihgTKpb15%2F8cbAnKYAsq4lqKnPOrn7gSOXWPrIrDf6GMhsWwWobMaywyvW94WGbMelrZSav9Rdd1IYkTRanryqb541pdhx7Rc%2ByuMK32vjwkIwRJYUh3ociJELbPdol0o0L0nJ0o0%2Ft9DBsgvLdLvviqWvBgHafAB7Usvv34OJS87x9%2Fs%2B3%2FwvhdzSjzNGpyJgkilrvymSZBbNmlIv68mnou1LkSnO6Fj%2FRoT54GpzAoHJyOynlj1hcUIwRbJkdB50280eGzOGMBP3bQDyDJHVeuNck3ebNGqKo5A5TD7JgH4byIkoDtprr6rWqf%2BXpKHn%2BoF7heATSABjpOH2hBx%2FR9PhL%2Fj7bC%2FpN11oMTXhxU7DIJUe%2BpGFeGJ3ED%2B6I7aNBImxaIND69LQVK9rwOoHhB57vsHSVBDxgrXIZrOM05C%2BgAW6LPZYq7890HbosMEqHATniVSTdyKp7caaw9waLQAbPPzBrDzaOrPzRT2wEe998T%2F2eG8ueZYO6zs4tKRv75bJfRIngg0TV9i2ec%2BnpJUwF4ypxINM%2FtmnaM1j2Ono2IRBwBDyLh2%2FOzXSRN2hf5UZB9Nntc3Pi3qGTzP2zuqrl3rVmnA4xROUidpjVR%2FD%2BtpxHby3%2F4j%2F6oomWvRiXKezcbR%2FKgBGBk9mno821jZJ3hbTqhUcNFXAYUDSCRCLQhMrcLlcfuxj%2BFRmNVO3TKQfquqit%2B%2FJnVpB2BzXIRXTtiwHH%2BsHIosGSVltSkzHhwfc47iIrDlFL%2FcT1IeLw51sZnT0jKWaCyCEovfPjHCH4tG77%2BFN10%2FBBWxR4phCSfzR%2BWX0%2BOZo134OzRI5%2FpE1V%2BKo8uKFhSMtAtNyZ0EQzI33eCPlrrCTSzLZkeNFGUjVNsVoRfxJhZ0WIB37%2B2akke6Iln3pRU0IVgsKeuTNQkxIQdh%2F9Z1n%2B68%2BFEOA9vTktOIIBD%2BDHIcXuwOQeAQYHW%2B02YwpozYmVBrTCB%2FsmjsxhapcOJ4LKWf%2FgmB7hNMCBnvHPH1iIR2%2BspueF1lQjedvABjWpBaGZTtckNfQSdAHT7E5wq2nSlqmlfTGUaa50ae86QwNp3u7lZI4QZUsTgjXXN3YaZOgiZCQtch5jhc70mwcqZzrtiZe%2Fa8UU0Lv7%2BRkr9baNMyBt9AYfY2BO80WxhTOM5UWrKHCVOx6JB85EREXiUrOZapYL7QrJJomP%2FmGK%2FORjNO3xm1l7VDtoH9%2B4g4NwykziFhjHFt39gXd23%2FVe1z9jYqUP5JgBLtdHmHsDyrpkq2E%2Fvy%2FoHPPH3kS0e9%2F6izF17GObTGOmCs4U9D9dybrLK8K4AsOzxmGLeoN9vKpoQ8wOB7cQ4i%2FW1WY6PbRW9PjBy6baViFtXLdQ7Zk3QitwuIjlihdtFpJjSmJKLuSMwtClD7XSpkLVnV%2BUYPolod66sK4BaYlulQq%2BZe6fa5rWd6BElHRwlMf%2FWjvHa17OT0HX39ak3%2Fgtn5%2FrhFuREKh2LERF6xdXxo88fa2qNu%2FbUvMOCCAYUeKJkKCL%2FjW%2FbKnt4gA%2FjHbfQSEodQgYrvox1XY5K1JR4qIptdN%2FAqV85ckaCMj3bRxlApMk1Mjnjx7%2Bm5y4%2B%2Bm57dpJsmGJaCr%2Bj8W3g2DAM0GU3v155ktYh87sTSLBmaEPzd8a0h0RtVs39nUrt2v39tilyd9Y7%2F6zDWLbT1w8x66YJjm5YE0cf96QFhweX6USXtkxEJtvAa7s54PtiVJXl8YQMHAl8VDJLb0Cz8Eoi70nrMes%2BNy1QREx6wETd%2FVCBJyWnWMdU6iPAuRUIoHepeCzqfSHZ5tesKYIpVM4ZloK6aOVNZ2lfrRMOPigxnR4TBCxpGC%2Bonm%2F4TUAUsCuMZoxqGGmgSP8z2bNS4FNU1ZL4Kz14eTixOwpS3Zz1YhPm6l%2Bkd2WZNnOhrqT6bOAaeIdpJtL8ZipMizK4UDa3j1zSk8t7UcOPKe2jOs5L4Y4fLw9JBa7748uQtRqDSZJan46ahW9Oz3f2oibG31G4I2MixPpknuNB%2FxIHEFsYRworNeGFivJhwS3mtmMkkMU%2FyxqA0Bl3BujwvfT3az4VzJ6yeVzIPV1uNbl10xERa9A%2B9MH8W565NSAYaEoRo9IIQ31oj1CbbPR93oXHYfv7vzWchT4KT2Bn%2FEy1nnoEny%2F2uFRIB4Bp9sAg%2FYbRLU4hV1BHuWyIpB9%2FhSfeszLNPbJD7fhE7fMWgPqIjphzdbHlehdddKztJojCrANfII%2F%2B3%2FrPUdBpm0kQI57FZ6rLyK%2FXZTFaFGMu7knWH0j0GYfVW6BxoZphF%2B2L1cVpJ8rMmmiUhu61iZJYdJtKJC4ZNTQl%2Bete7oEEy10Po3FacShsOBUg3RNUTWhzo0849RcTIborN2D0EN0hZcYI%2BCzKCGYiliR0KcbHBhutiikkak1%2BCvE6u%2FCXnx96wR%2FLGXNU6UEBDYAiKXDj0Mt3DBRTVBZW%2BovIVBm1LDTERk5UzYAnugAC%2FVRVHhk6ysNukuQp27G7tDmJMhKNB5hDoKpmUvRdcbjSLkOduhmU8UkhJv3mnc00a%2F%2FB%2FqcHt%2B2XPg%2FYzid0G0%2BgyzA9xmP08BCBlQrA1H7h94zgLk5H%2BVnhyyzdR%2BBULiUrkDbqFoNwjwgvbL%2BePZ8eBPF6TefWuQiu5WAmF8C20rPKcaSW9CdrzoWFPADwauibXttVKWANhfEes4nq1IWQBN%2F%2Fsjs%2BmkXe8k7j61NlgeltrdjteoguchkSwgihZpeovV36G6u62FZZj4bDrtn9I%2B5JtSuBzS87p51KsyHzuz%2BzWp%2FO2vWKCGTmjyHRjqXfLPBDPc4rld9VYqjdqN%2F3wdRX0EPopHicxjsPmeLSdAiyg7Z3Jw4ZxPCLoZC8QmzyI26fdvBtieUY7%2BfsEqTxzicOckxtHVqpLN0N%2FOeIoTgxv8LoFLzbo9yCCtK3i5U65vlDPcabDxl6bCfZlhExxEqBYLPh9ExY1OpyfrbQph8F6DxRopqMo8d3AUkgqCOSoLY%2FcrCfcLiSsUK%2FERdatTE5QEq59imricYClKtlSobyyrNfbL89%2BgU2Yww197ASqlFzBhqGU3hI7HDaPCpDdr4ZdUfOTbLyhnOpk32CBD%2BA7srP8CrdsqiG9GbmftEcdH23Z%2BQG%2BpbFT3DHXm%2FSxKY%2BnGsA8e2D9Vv4nS5rUetDXhlCJLVzKbIhd%2BJbwKZAyDIdm26gVmJPF7CKriZH&__VIEWSTATEGENERATOR=A11B5251&utcOffset=7200000&ctl00%24ddlCulture=en&ctl00%24cph1%24hidStartUtc=637641856518797225&ctl00%24cph1%24visible=radioAll' \
  --compressed" 

    os.system(curl)

    #filename = wget.download(url)
    filename = 'curl.data'
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
    id_beg = 2
    id_angle_culm = 6
    id_end = 8

    days = [passage[id_day] for passage in line]
    #shape of day: "<td><a ...>DAY</a>"
    days = [day[day.find('>')+1:] for day in days]  # filter the first <td> balise
    days = [day[day.find('>')+1:] for day in days]  # filter the <a> balise
    days = [day[:-4] for day in days]

    begs = [passage[id_beg] for passage in line]
    begs = [beg[4:] for beg in begs]

    #shape of angle culm: "<td ......>ANGLE"
    angles_culm = [passage[id_angle_culm] for passage in line]
    angles_culm = [angle_culm[angle_culm.find('>')+1:] for angle_culm in angles_culm]

    ends = [passage[id_end] for passage in line]
    ends = [end[4:] for end in ends]

    for day, beg, end, angle_culm in zip(days, begs, ends, angles_culm):
        if int(angle_culm[:-1]) > 20:
            previ.append((sat, day, beg, end))


def rel(x):
    _,d,b,_ = x
    b = [int(x) for x in b.split(':')]
    return (int(d[:2]), b[0], b[1], b[2])

previ = sorted(previ, key=rel)

for sat in previ:
    print(sat)


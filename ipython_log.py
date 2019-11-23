
import re
s = """Test del bot;23-11-2019 15:00;23-11-2019 18:00;Via Tal dei Tali, nr 340 ....;La mia descrizione dell'evento
dojasofjaoifdjaosdsdoifjasoifj
adsfoiaofadjfoasjdfojasofijaosdfjoasifjoi

questa è l'ultima riga della descrizione"""
m = re.search(r, s)
r = "(.*?);(.*?);(.*?);(.*?);(.*)"
l = re.split(';',s)
l[1]
import datetime
datetime.datetime.strptime()
l[1]
dt = datetime.datetime.strptime(l[1], "%d-%m-%Y %H:%M")
dt_start = datetime.datetime.strptime(l[1], "%d-%m-%Y %H:%M")
dt_stop = datetime.datetime.strptime(l[2], "%d-%m-%Y %H:%M")
dt_stop.strftime("%Y-%m-%d %H:%M")

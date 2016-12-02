from DownloadCH import Cyanide

c = Cyanide()   #Downloads all of the comics
c1 = Cyanide(1, 0)   #Use comic names as file names

c2 = Cyanide(0, 0)
c2.downloadcomic("http://explosm.net/comics/489/")

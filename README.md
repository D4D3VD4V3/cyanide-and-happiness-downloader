
![Travis](https://travis-ci.org/D4D3VD4V3/cyanide-and-happiness-downloader.svg?branch=master)

**Usage:**
-  Download all comics to the script's directory with the date published as the filenames:<br>
`obj = Cyanide()`<br><br>
- Download all comics to a provided path with comic names as filenames:<br>
`obj = Cyanide(1, 0, PATH_TO_EMPTY_DIR)`<br><br>
- To provide individual comic links to download,
	first create a *Cyanide* object with the *download_all* parameter set to 0. Then you can give a C&H comic URL to the *downloadcomic()* method.<br>
    `obj = Cyanide(0)`<br>
    `obj.downloadcomic(LINK_TO_COMIC)`


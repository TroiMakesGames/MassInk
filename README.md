# MassInk
MassInk - an exporting tool Based on Inkscape vector graphics and Python

...initialy made for personal use...

Inkscape allows for amazing text customization - but its not great when you have a large set of text/strings and want to export them, as it has to be done manualy for every text/string ...

MassInk fixes that issue ...
The user can manualy create a single SVG file containing a text element with the desired style/look (color, width, stroke...) while MassInk applies that style to the large set of text/strings automaticaly and exports the result

HOW TO USE:<br>
in main.py replace `inkscapePath` with the path to your inkscape.exe installation<br>
in main.py replace `contentsJsonPath` with the path to the JSON file with the correct data format<br>
-by default the contentsJsonPath is set to the already existing contents.json with example data

json data format:<br>
contents - an array of strings where each string is an individual asset
-since inkscape doesnt support `\n` newline whitespace the `|` substitue is used

dpi - integer of "dots per inch" setting for the image export resolution

style - inkscapes/CSS/svg style format for styling text
-note that this hould include only text inside the quotation marks (use existing contents.json as an example)

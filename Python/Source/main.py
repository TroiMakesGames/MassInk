inkscapePath = r"C:\Program Files\Inkscape\bin\inkscape.exe"
contentsJsonpath = "Source/contents.json"

import shutil
import pathlib
import subprocess
import json

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#returns json string array as python string array
def readJsonContents(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data.get("contents", [])

def readJsonStyle(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data.get("style", [])

def readJsonDPI(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data.get("dpi", [])

def moveFile(filePath, destinationPath):
    #convert string path to lib path
    filePath = pathlib.Path(filePath)
    destinationPath = pathlib.Path(destinationPath)

    #generate if doesnt exist
    destinationPath.mkdir(exist_ok=True)

    destination = destinationPath / filePath.name
    shutil.move(str(filePath), str(destination))

def exportSVGasPNG(inkscapePath, svgPath, pngPath, dpi):
    svg_path = pathlib.Path(svgPath)
    png_path = pathlib.Path(pngPath)
    inkscape_path = pathlib.Path(inkscapePath)


    command = f'"{inkscape_path}" "{svg_path}" ' \
          f'--export-type=png ' \
          f'--export-filename="{png_path}" ' \
          f'--export-id=text1 ' \
          f'--export-id-only ' \
          f'--export-dpi={dpi}'

    subprocess.run(command, shell=True, check=True)

#get style code
def getStyleCodeAsString(stylePath):
    with open(stylePath, "r", encoding="utf-8") as f:
        svg = f.read()
    return svg

def generateTspans(outputString):
    #generate correct svg fromat code
    outputString = outputString
    lines = outputString.split("|")
    tspanString = ""

    codeSegment = '<tspan sodipodi:role="line" x="0" y="Yem" id="tspan2">PLACEHOLDER</tspan>'
    for i in range(len(lines)):
        linesCodeSegment = codeSegment
        Y = str(1.1 * i)
        linesCodeSegment = linesCodeSegment.replace("Y", Y)
        linesCodeSegment = linesCodeSegment.replace("PLACEHOLDER", lines[i])
        tspanString += linesCodeSegment
    
    return tspanString

def generateNewSVG(svgCode, tspanString, outputSVGname, styleString):
    #replace style placeholder with correct svg format code
    svgCode = svgCode.replace("stylePLACEHOLDER", styleString)
    #replace placeholder with the correct svg fromat code
    svgCode = svgCode.replace("tspanPLACEHOLDER", tspanString)

    #generate a new svg with the right output text
    with open(outputSVGname, "w", encoding="utf-8") as f:
        f.write(svgCode)

def singleAssetPipeline(svgPath, outputString, outputSVGdestination, outputSVGname, inkscapePath, outputPNGdestination, outputPNGname, styleString, dpi):
    """
    -duplicate style svg code for replacing and svg format style
    -generate tspan svg code from the python string
    -generate new svg (replace PLACEHOLDER in duplicated svg code with the generated tspan code)
    -export duplicate svg contents as png (moves png to destination by default)
    -move svg to destination folder
    """

    svg = getStyleCodeAsString(svgPath)

    tspanString = generateTspans(outputString)

    generateNewSVG(svg, tspanString, outputSVGname, styleString)

    #export the new svg as png
    pngPaths = outputPNGdestination + "/" + outputPNGname
    exportSVGasPNG(inkscapePath, outputSVGname, pngPaths, dpi)

    #move new svg to SVGs
    moveFile(outputSVGname, outputSVGdestination)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#multiple assets pipeline:

"""
the user should be required to enter:
-inkscape path                  (Hardcoded)
-project contents.json path     (Hardcoded)

contents.json should contain:
-string array with corret seperators for newline whitespace ("|")
-style string                   (inkscape svg format as string but only whats inside " ")
-output DPI                     (int)
"""

contentStrings = readJsonContents(contentsJsonpath)
contentStyle = readJsonStyle(contentsJsonpath)
dpi = readJsonDPI(contentsJsonpath)

for i in range(len(contentStrings)):
    svgName = "output" + str(i) + ".svg"
    pngName = "output" + str(i) + ".png"

    singleAssetPipeline("Source/style.svg", contentStrings[i], "Source/SVGs", svgName, inkscapePath, "Source/PNGs", pngName, contentStyle, dpi)

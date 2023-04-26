from urllib.request import urlopen
from bs4 import BeautifulSoup

def func(ob):
    html = urlopen(ob)
    bsObj = BeautifulSoup(html.read(), features="html.parser")
    printed = str(bsObj.prettify)
    subPrinted = printed[printed.find(
        "Front camera"):printed.find("Connectivity")]

    subPrinted = subPrinted[(subPrinted.find("MP")-5):]
    n_pix = subPrinted[0: subPrinted.find("MP")]

    while (n_pix[0].isdigit() == False):
        n_pix = n_pix[1:]

    list = [float(n_pix)*1000000]

    if "f/" in subPrinted:
        subPrinted = subPrinted[subPrinted.find("f/")+2:]

    if "f</i>/" in subPrinted:
        subPrinted = subPrinted[subPrinted.find("f</i>/")+6:]
    apperature = ""

    while subPrinted[0].isdigit() or subPrinted[0] == ".":
        apperature = apperature + subPrinted[0]
        subPrinted = subPrinted[1:]
    list.append(float(apperature))

    if "1/" in subPrinted:
        subPrinted = subPrinted[subPrinted.find("1/")+2:]
        image_sensor = 1 / float(subPrinted[0:subPrinted.find('"')])
        list.append(image_sensor)

    if "µm" in subPrinted:
        subPrinted = subPrinted[subPrinted.find("µm")-5:]
        pxl_size = subPrinted[0:subPrinted.find("µm")]
        while pxl_size[0].isdigit() == False:
            pxl_size = pxl_size[1:]
        list.append((float(pxl_size))/1000000)
    return list

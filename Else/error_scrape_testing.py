from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

try:
    html = urlopen("https://www.walmart.com/ip/Used-OnePlus-8-5G-GSM-Unlocked-128GB-Interstellar-Glow-Black/589716447")
except HTTPError as e:
    print(e)
except URLError as e:
    print("The server couldn't be found!")
else:
    print("It worked!")

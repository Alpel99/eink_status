import json
import requests
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne

# Initialize the Inky pHAT display
inky_display = InkyPHAT("black")

# URL to make the HTTP request to
url = "http://glasergasse:8080"

def writeState(value):
    with open('/tmp/boolean_state.txt', 'w') as file:
        file.write(str(int(value)))

def checkState():
    try:
        with open('/tmp/boolean_state.txt', 'r') as file:
            return bool(int(file.read()))
    except FileNotFoundError:
        value = False
        writeState(False)
        # Return a default value (False) if the file doesn't exist
        return value

def drawOffline():
    if(not checkState()):
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FredokaOne, 30)
    
        m1 = "Glasergasse"
        # m1 = url
        m2 = "is offline"
        w1, h1 = font.getsize(m1)
        w2, h2 = font.getsize(m2)
        o = h1/2
        x1 = (inky_display.WIDTH / 2) - (w1 / 2)
        x2 = (inky_display.WIDTH / 2) - (w2 / 2)
        y1 = (inky_display.HEIGHT / 2) - (h1 / 2) - o
        y2 = (inky_display.HEIGHT / 2) + (h2 / 2) - o
            
        draw.text((x1, y1), m1, inky_display.BLACK, font)
        draw.text((x2, y2), m2, inky_display.BLACK, font)
        inky_display.set_image(img)
        inky_display.show()
        writeState(True)

try:
    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the message from the JSON response (adjust the key as needed)
        uptime = data.get("uptime", "No message received")
        users = data.get("users")
        load = data.get("load")
        reslist = data.get("reslist")
        cpu = data.get("cpu_percent")
        ram = data.get("ram_percent")

        Fcse = reslist[1]
        FA = reslist[2]
        MC = reslist[3]

        # Create an image with the message
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
        # font = ImageFont.load_default()
        
        ol = 20
        font = ImageFont.truetype(FredokaOne, ol-2)
        ox = 0
        oy = 0
        # Write the message to the image
        draw.text((ox, oy), uptime, inky_display.BLACK, font)
        draw.text((ox, oy+ol), users + ", " + load, inky_display.BLACK, font)
        draw.text((ox, oy+2*ol), "CPU: " + str(cpu) + "%", inky_display.BLACK, font)
        draw.text((ox+inky_display.WIDTH/2, oy+2*ol), "RAM: " + str(ram) + "%", inky_display.BLACK, font)
        draw.text((ox, oy+3*ol), "MC: " + str(MC), inky_display.BLACK, font)
        draw.text((ox, oy+4*ol), "FCSE: " + str(Fcse), inky_display.BLACK, font)
        draw.text((ox+inky_display.WIDTH/2, oy+4*ol), "FA: " + str(FA), inky_display.BLACK, font)

        # Display the image on the Inky pHAT
        inky_display.set_image(img)
        inky_display.show()
        writeState(False)

    else:
        print(f"HTTP request failed with status code {response.status_code}")
        drawOffline()

except Exception as e:
    print(f"Error: {str(e)}")
    drawOffline()


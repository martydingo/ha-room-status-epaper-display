import libs.ha_api_lib as ha
import libs.epd7in5_V2.epd7in5_V2 as epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import os 

def crawlRoomLights(roomName):
    haStates = ha.entities.all()
    roomLights = []
    for entities in haStates:
        if('light' in entities['entity_id']):
            if((str(roomName).replace(' ','_').lower() + '_') in entities['entity_id']):
                roomLights.append(entities['entity_id'])
                #roomLights.append(entities['attributes']['friendly_name'])
    return roomLights

dispWidth = 800
dispHeight = 480

roomFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),72)
lightsTitleFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),48)
lightsFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),24)
roomName = "Living Room"


haStates = ha.entities.all()


try:
    disp = epd7in5_V2.EPD()
    dispInitRC = disp.init()
    disp.Clear()
except:
    print("Error initialising display")

image = Image.new(mode='1', size=(dispWidth, dispHeight), color=255)
draw = ImageDraw.Draw(image)

## Name of Room w/ Lines
draw.line(((0,dispHeight/40),(dispWidth,dispHeight/40)))
draw.line(((0,((dispHeight/40)+72)),(dispWidth,((dispHeight/40)+72))))
draw.text((dispWidth/3, dispHeight/40), roomName,
          font=roomFont, fill=0, anchor='ms')

## List of Lights
draw.text((0, dispHeight/4), "Lights",
          font=lightsTitleFont, fill=0, anchor='ls')
draw.line(((0,((dispHeight/4)+48)),(dispWidth/6,((dispHeight/4)+48))))
Lights = crawlRoomLights(roomName)
for light in Lights:
    lightDict = ha.entities.entity_id(light)
    draw.text((0, ((dispHeight/4+72)+(Lights.index(light)*26))), lightDict['attributes']['friendly_name'] + "is switched " + lightDict['state'],
              font=lightsFont, fill=0, anchor='ls')

## Push to Display
try:
    disp.display(disp.getbuffer(image))
except:
    print("Error pushing to display")

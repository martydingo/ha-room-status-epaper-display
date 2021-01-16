import libs.ha_api_lib as ha
import libs.epd7in5_V2.epd7in5_V2 as epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import os 

roomFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),72)
mediaFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),24)
climateFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),24)
lightsTitleFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),48)
lightsFont = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),24)
roomName = "Living Room"
dispWidth = 800
dispHeight = 480

def crawlRoomLights(roomName):
    haStates = ha.entities.all()
    roomLights = []
    for entities in haStates:
        if('light' in entities['entity_id']):
            if((str(roomName).replace(' ','_').lower() + '_') in entities['entity_id']):
                roomLights.append(entities['entity_id'])
    return roomLights

def crawlRoomClimate(roomName):
    haStates = ha.entities.all()
    roomClimate = []
    for entities in haStates:
        if('climate' in entities['entity_id']):
            if((str(roomName).replace(' ','_').lower() + '_') in entities['entity_id']):
                roomClimate.append(entities['entity_id'])
    return roomLights

def crawlRoomMedia(roomName):
    haStates = ha.entities.all()
    roomMedia = []
    for entities in haStates:
        if('media_player' in entities['entity_id']):
            if('unavailable' not in entities['state']):
                if('off' not in entities['state']):
                    if('unknown' not in entities['state']):
                        if('idle' not in entities['state']):
                            if('Lounge Room' not in entities['attributes']['friendly_name']):
                                roomMedia.append(entities['entity_id'])
    return roomMedia

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
draw.text((10, dispHeight/4), "Lights",
          font=lightsTitleFont, fill=0, anchor='ls')
draw.line(((10,((dispHeight/4)+48)),(dispWidth/6,((dispHeight/4)+48))))
Lights = crawlRoomLights(roomName)
for light in Lights:
    lightDict = ha.entities.entity_id(light)
    draw.text((10, ((dispHeight/4+72)+(Lights.index(light)*26))), lightDict['attributes']['friendly_name'] + " is switched " + lightDict['state'],
              font=lightsFont, fill=0, anchor='ls')

## List of Media
draw.text((10, dispHeight/1.75), "Media",
          font=lightsTitleFont, fill=0, anchor='ls')
draw.line(((10,((dispHeight/1.75)+48)),(dispWidth/6,((dispHeight/1.75)+48))))
Media = crawlRoomMedia(roomName)
for media in Media:
    mediaDict = ha.entities.entity_id(media)
    draw.text((10, ((dispHeight/1.75+72)+(Media.index(media)*52))), mediaDict['attributes']['friendly_name'] + " is currently " + mediaDict['state'],
              font=mediaFont, fill=0, anchor='ls')
    try:
        if(mediaDict['attributes']['media_title']):
            currentlyPlaying=('--- ' + mediaDict['attributes']['media_title'] + ' - ' + mediaDict['attributes']['media_artist']+' ---')
            draw.text((10, ((dispHeight/1.75+72)+((Media.index(media)*52)+26))), currentlyPlaying,
                      font=mediaFont, fill=0, anchor='ls')
    except KeyError:
        continue

## Climate
draw.text((dispWidth-10, dispHeight/4), "Climate",
          font=LightsTitleFont, fill=0, anchor='rs')
draw.line(((dispWidth-90,((dispHeight/4)+48)),(dispWidth,((dispHeight/4)+48))))
Climate = crawlRoomClimate(roomName)
for climate in Climate:
    climateDict = ha.entities.entity_id(climate)
    draw.text((dispWidth-10, ((dispHeight/4+72)+(Climate.index(climate)*52))), climateDict['attributes']['friendly_name'] + " is currently at " + climateDict['attributes']['current_temperature']+"°C",
              font=climateFont, fill=0, anchor='rs')
    draw.text((dispWidth-10, ((dispHeight/4+72)+((Climate.index(climate)*52)+26))), "Humidity at "+ climateDict['attributes']['current_humdity']+"%",
              font=climateFont, fill=0, anchor='rs')
    
## Push to Display
try:
    disp.display(disp.getbuffer(image))
except:
    print("Error pushing to display")

import libs.ha_api_lib as ha
import libs.epd7in5_V2.epd7in5_V2 as epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import os 
import time

roomFont = ImageFont.truetype((os.getcwd()+"/fonts/RobotoSlab-Regular.ttf"),72)
mediaFont = ImageFont.truetype((os.getcwd()+"/fonts/Comfortaa-VariableFont_wght.ttf"),24)
climateFont = ImageFont.truetype((os.getcwd()+"/fonts/Comfortaa-VariableFont_wght.ttf"),24)
lightsTitleFont = ImageFont.truetype((os.getcwd()+"/fonts/Comfortaa-VariableFont_wght.ttf"),48)
lightsFont = ImageFont.truetype((os.getcwd()+"/fonts/Comfortaa-VariableFont_wght.ttf"),24)
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
            if((str(roomName).replace(' ','_').lower()) in entities['entity_id']):
                roomClimate.append(entities['entity_id'])
    return roomClimate

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
    while True:
        image = Image.new(mode='1', size=(dispWidth, dispHeight), color=255)
        draw = ImageDraw.Draw(image)
        
        ## Name of Room w/ Lines
        draw.line(((0,dispHeight/40),(dispWidth,dispHeight/40)))
        draw.line(((0,((dispHeight/40)+72)),(dispWidth,((dispHeight/40)+72))))
        draw.text((dispWidth/4, dispHeight/40), roomName,
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
        draw.text(((dispWidth/3)*2, dispHeight/4), "Climate",
                  font=lightsTitleFont, fill=0, anchor='ls')
        draw.line((((dispWidth/3)*2,((dispHeight/4)+48)),(((dispWidth/3)*2)+80,((dispHeight/4)+48))))
        Climate = crawlRoomClimate(roomName)
        for climate in Climate:
            climateDict = ha.entities.entity_id(climate)
            draw.text(((dispWidth/3)*2, ((dispHeight/4+72)+(Climate.index(climate)*52))), climateDict['attributes']['friendly_name'] + " is currently at " + str(climateDict['attributes']['current_temperature'])+"°C",
                      font=climateFont, fill=0, anchor='ls')
            draw.text(((dispWidth/3)*2, ((dispHeight/4+72)+((Climate.index(climate)*52)+26))), "Humidity at "+ str(climateDict['attributes']['current_humidity'])+"%",
                      font=climateFont, fill=0, anchor='ls')
            draw.text(((dispWidth/3)*2, ((dispHeight/4+72)+((Climate.index(climate)*52)+52))), "and currently set to "+ str(climateDict['attributes']['hvac_action']) + ",",
                      font=climateFont, fill=0, anchor='ls')            
            draw.text(((dispWidth/3)*2, ((dispHeight/4+72)+((Climate.index(climate)*52)+78))), "targeting " + str(climateDict['attributes']['temperature'])+"°C",
                      font=climateFont, fill=0, anchor='ls')
            
        ## Push to Display
        try:
            disp = epd7in5_V2.EPD()
            dispInitRC = disp.init()
            disp.Clear()
            disp.display(disp.getbuffer(image))
        except:
            print("Error pushing to display")
        
        time.sleep(60)
except KeyboardInterrupt:
    exit()
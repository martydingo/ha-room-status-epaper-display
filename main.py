import libs.ha_api_lib as ha
import libs.epd7in5_V2.epd7in5_V2 as epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import os 

dispWidth = 800
dispHeight = 480

font = ImageFont.truetype((os.getcwd()+"/fonts/BebasNeue-Regular.ttf"),72)
Text = "Living Room"

def dispStatus(room=None):
    try:
        disp = epd7in5_V2.EPD()
        dispInitRC = disp.init()
        disp.Clear()
    except:
        print("Error initialising display")
    
    image = Image.new(mode='1', size=(dispWidth, dispHeight), color=255)
    draw = ImageDraw.Draw(image)
    
    draw.line((0,dispHeight/40),(dispWidth,dispHeight/40))
    draw.text((dispWidth/3, dispHeight/40), Text,
              font=font, fill=0, anchor='ms')
    try:
        disp.display(disp.getbuffer(image))
    except:
        print("Error pushing to display")
    #print(ha.entities.entity_id("light.living_room_desk_lamp"))

dispStatus()
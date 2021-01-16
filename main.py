import libs.ha_api_lib as ha
import libs.epd7in5_V2.epd7in5_V2 as epd7in5_V2
import PIL
import os 

dispWidth = 800
dispHeight = 480

font = ImageFont.truetype((os.getcwd()+"fonts/BebasNeue-Regular.ttf"),size=40)
Text = "Living Room"

try:
    disp = epd7in5_V2.EPD()
    dispInitRC = disp.init()
    disp.Clear()
except:
    print("Error initialising display")


image = PIL.Image.new(mode=‘1’, size=(dispWidth, dispHeight), color=255)
draw = PIL.ImageDraw.Draw(image)

draw.text((0, 0), Text,
          font=font, fill=0, align='left')
try:
    disp.display(disp.getbuffer(image))
except:
    print("Error pushing to display")
#print(ha.entities.entity_id("light.living_room_desk_lamp"))
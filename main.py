import libs.ha_api_lib as ha
import libs.epd7in5_V2.epd7in5_V2 as epd7in5_V2

disp = epd7in5_V2.EPD()

disp.clear()

print(ha.entities.entity_id("light.living_room_desk_lamp"))
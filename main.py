# from user import settings
from callAI import *

while True:
    try:
        # socket.CallOherAI().callByhttpx()
        spark.CallSparkAI("lite").callByhttpx()
    except KeyboardInterrupt:
        break

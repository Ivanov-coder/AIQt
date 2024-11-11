# from user import settings
from callAI import *

while True:
    try:
        # socket.CallOherAI().callByhttpx()
        spark.callSparkAI()
    except KeyboardInterrupt:
        break
    
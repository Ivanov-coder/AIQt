# from user import settings
from callAI import *

while True:
    try:
        httpSocket.CallOherAI().callByhttpx()
    except KeyboardInterrupt:
        break
    
import sys
import os
import platform

def Check():

    def Win():
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    try:
        import g_python
    except:
        os.system("python -m pip install g_python")
        Win()

Check()

###############################################################

from time import sleep
from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.hpacket import HPacket
from g_python.hparsers import HEntity, HEntityType
from g_python.hunityparsers import HUnityEntity, HEntityType

extension_info = {
    "title": "LFriends",
    "description": "Application to add friends",
    "author": "Luizin",
    "version": "1.1"
}

ext = Extension(extension_info, args=sys.argv)
ext.start()

def client_type():
    sleep(0.30)
    return ext.connection_info["client_type"]

client_type = client_type()

isFlash = None

if str(client_type).startswith("FLASH"):
    client_type = "FLASH"
else:
    client_type = "UNITY"

print(f'[LFriender] ~ Application Started. Client Type: {client_type}\n\n')

headers = {}

if client_type == "FLASH":
    headers = {
        "RoomUsers": 812,
        "RequestFriend": 3639,
        "MessengerError": 2095
    }
else:
    headers = {
        "RoomUsers": 28,
        "RequestFriend": 39,
        "MessengerError": 260
    }

counter = -1

def DetectUsers(message):
    global counter
    packet = message.packet
    if client_type == "FLASH":
        entity = HEntity.parse(packet)
        for user in entity:
            if user.entity_type == HEntityType.HABBO:
                counter += 1
                ext.send_to_server(HPacket(headers["RequestFriend"], str(user.name).strip()))
                print(f"[LFriender] ~ Request sent to: {counter} users.", end='\r')
    else:
        entity = HUnityEntity.parse(packet)
        for user in entity:
            if user.entity_type == HEntityType.HABBO:
                counter += 1
                ext.send_to_server(HPacket(headers["RequestFriend"], str(user.name).strip()))
                print(f"[LFriender] ~ Request sent to: {counter} users.", end='\r')

def BlockMessageError(msg):
    msg.is_blocked = True

ext.intercept(Direction.TO_CLIENT, DetectUsers, headers["RoomUsers"])
ext.intercept(Direction.TO_CLIENT, BlockMessageError, headers["MessengerError"])

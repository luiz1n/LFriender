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

from g_python.gextension import Extension
from g_python.hunitytools import UnityRoomUsers
from g_python.hdirection import Direction
from g_python.hpacket import HPacket

RequestFriend = 39
RequestRoomLoad = 391
UsersInRoom = 28

global r_Users

ext_info = {"title": "LFriender", "description": "Up your friendship achievements", "author": "Luizin", "version": "1.0"}

extension = Extension(ext_info, sys.argv)
print('Press Ctrl + C to stop the application.\n')
Users = UnityRoomUsers(extension)
extension.start()
print('[LFriender] -> Application started. \n\n')

def send_request(friend):
    extension.send_to_server(HPacket(39, friend))

def Friender(message):
    global Users
    invited = 0
    for user in Users.room_users.values():
        invited += 1
        _nickname = user.name.strip()
        send_request(_nickname)
        print(f'[LFriender] -> I sent a friend request to : {_nickname}')
    print(f'\n\n[LFriender] -> I sent a friend request to {invited} people.\n\n')

extension.intercept(Direction.TO_CLIENT, Friender, UsersInRoom)
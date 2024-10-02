import json
from player import Player, Movie
player = Player()
player.loadFromJson("base_data.json")
player.playForward()
print("_______________________________")
player.removeMedia(5)
player.playForward()
print("_______________________________")

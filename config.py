################################################################################
# Filename: config.py                                                          #
# Created by: Venceslas Duet                                                   #
# Created at: 04-05-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: Manage configuration into program                               #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import json


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Config:
    expand = False
    use_song = True
    song_volume = 1.0

    @staticmethod
    def load(config_path="resource/config.json"):
        file = open(config_path, 'r')
        lines = file.read().split('\n')
        line = ""
        for i in lines:
            line = line + i
        try:
            data = json.loads(line)
        except:
            return
        if "expand" in data:
            if isinstance(data["expand"], bool):
                Config.expand = data["expand"]
        if "use_song" in data:
            if isinstance(data["use_song"], bool):
                Config.use_song = data["use_song"]
        if "song_volume" in data:
            if isinstance(data["song_volume"], int) or isinstance(data["song_volume"], float):
                if 0 <= data["song_volume"] <= 1:
                    Config.song_volume = float(data["song_volume"])

    @staticmethod
    def save(config_path="resource/config.json"):
        to_save = Object()
        to_save.use_song = Config.use_song
        to_save.song_volume = Config.song_volume
        file = open(config_path, 'w')
        file.write(to_save.toJSON())

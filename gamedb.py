from __future__ import annotations

import enum
import json

import pygame

from resource import Resource

class CardInfo:
    thumbnail : pygame.Surface
    title : str

    def __init__(self, title : str, thumbnail : pygame.Surface):
        self.title = title
        self.thumbnail = thumbnail

    @staticmethod
    def generate_random() -> CardInfo:
        from random import randint

        title_length = randint(5,10)
        thumbnail_size = int(Resource.getMetric(Resource.METRIC_CARD_ICON_SIZE))

        title = chr(randint(ord('A'), ord('Z')))

        for i in range(title_length):
            title += chr(randint(ord('a'), ord('z')))

        surf = pygame.Surface((thumbnail_size, thumbnail_size))

        for col in range(thumbnail_size):
            for row in range(thumbnail_size):
                surf.set_at((col, row), (randint(0,255),randint(0,255),randint(0,255)))

        return CardInfo(title, surf)

class GameType(enum.Enum):
    NATIVE = 0
    MAME = 1

    @staticmethod
    def from_text(text: str) -> GameType:
        match text:
            case "native": return GameType.NATIVE
            case "mame": return GameType.MAME

        raise ValueError("{} is not a valid game type".format(text))

    def gen_command(self, path: str, name: str, executor: str) -> str:
        match self:
            case GameType.NATIVE:
                return "./{}/{}/{}".format(path, name, executor)
            case GameType.MAME:
                return "mame -rp {} {} -nofilter -skip_gameinfo".format(path, executor)
class GameInfo:
    _name: str
    _copyright: str
    _type: GameType
    _thumbnail: pygame.Surface
    _executor: str

    def __init__(self, name: str, game_copyright: str, game_type: GameType, thumbnail: pygame.Surface, executor: str):
        self._name = name
        self._copyright = game_copyright
        self._type = game_type
        self._thumbnail = thumbnail
        self._executor = executor

    @property
    def name(self) -> str:
        return self._name

    @property
    def copyright(self) -> str:
        return self._copyright

    @property
    def executor(self) -> str:
        return self._executor

    @property
    def thumbnail(self) -> pygame.Surface:
        return self._thumbnail

    @property
    def type(self) -> GameType:
        return self._type

class GameDB:
    _db_path: str
    _mame_path: str
    _loaded: bool = False

    _games: list[GameInfo]

    @staticmethod
    def load(path: str):
        GameDB._db_path = path
        GameDB._loaded = False

        data = GameDB.readJSON(path + "/index.json")

        GameDB.parse_data(data)

    @staticmethod
    def parse_data(data):
        GameDB._mame_path = data["mame-path"]

        game_number = len(data["games"])

        games = [None] * game_number

        for i in range(game_number):
            games[i] = GameDB.parse_game(data["games"][i])

        GameDB._games = games

    @staticmethod
    def parse_game(game) -> GameInfo:
        return GameInfo(
            game["name"],
            game["copyright"],
            GameType.from_text(game["type"]),
            pygame.image.load("{}/thumbnails/{}".format(GameDB._db_path, game["card-thumbnail"])),
            game["exec"]
        )

    @staticmethod
    def readJSON(file):
        lines = open(file, 'r').read().split('\n')
        line = ""
        for i in lines:
            line += i
        return json.loads(line)

    @staticmethod
    def reload():
        GameDB.load(GameDB._db_path)

    @staticmethod
    def get_cards() -> list[CardInfo]:
        ret = [None] * len(GameDB._games)

        for i in range(len(GameDB._games)):
            ret[i] = CardInfo(
                GameDB._games[i].name,
                GameDB._games[i].thumbnail
            )

        return ret

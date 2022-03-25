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

class MameGameInfo:
    _executor: str
    _scale_effect: bool
    _game_path: str

    def __init__(self, executor: str, scale_effect: bool, game_path: str):
        self._executor = executor
        self._scale_effect = scale_effect
        self._game_path = game_path

    @staticmethod
    def from_data(data, game_path: str) -> MameGameInfo:
        return MameGameInfo(
            str(data["exec"]),
            bool(data["scale-filter"]),
            str(game_path)
        )

    @property
    def exec_args(self) -> list[str]:
        return [
            "mame",
            "-rp",
            self._game_path,
            "-skip_gameinfo",
            "-nofilter" if self._scale_effect else "-filter",
            self._executor
        ]

class NativeGameInfo:
    _args: list[str]

    def __init__(self, args: list[str]):
        self._args = args

    @staticmethod
    def from_data(data) -> NativeGameInfo:
        tmp = data["args"]
        size = len(tmp)
        ret = [""] * size

        for i in range(size):
            ret[i] = str(tmp[i])

        return NativeGameInfo(ret)

class GameInfo:
    _name: str
    _copyright: str
    _thumbnail: pygame.Surface

    _type: GameType
    _game_info: NativeGameInfo | MameGameInfo

    def __init__(
            self,
            name: str,
            game_copyright: str,
            game_type: GameType,
            thumbnail: pygame.Surface,
            game_info: MameGameInfo | NativeGameInfo
    ):
        self._name = name
        self._copyright = game_copyright
        self._thumbnail = thumbnail

        self._type = game_type
        self._game_info = game_info

    @property
    def name(self) -> str:
        return self._name

    @property
    def copyright(self) -> str:
        return self._copyright

    @property
    def exec_args(self) -> list[str]:
        return self._game_info.exec_args

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
    def get_game_info(game, game_type: GameType) -> NativeGameInfo | MameGameInfo:
        match game_type:
            case GameType.NATIVE: return NativeGameInfo.from_data(game)
            case GameType.MAME: return MameGameInfo.from_data(game, GameDB._mame_path)

    @staticmethod
    def parse_game(game) -> GameInfo:
        game_type = GameType.from_text(game["type"])

        return GameInfo(
            game["name"],
            game["copyright"],
            game_type,
            pygame.image.load("{}/thumbnails/{}".format(GameDB._db_path, game["card-thumbnail"])),
            GameDB.get_game_info(game, game_type)
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

    @staticmethod
    def launch_game(game_id: int) -> bool:
        from subprocess import Popen
        from pynput.keyboard import Key, Listener

        proc = Popen(GameDB._games[game_id].exec_args)

        with Listener(on_release=GameDB.on_key_release) as listener:
            listener.join()

        proc.terminate()

        return proc.returncode == 0

    @staticmethod
    def on_key_release(key):
        from pynput.keyboard import Key

        return key == Key.alt

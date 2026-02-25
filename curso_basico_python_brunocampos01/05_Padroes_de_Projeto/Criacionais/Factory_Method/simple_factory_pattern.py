from abc import ABC, abstractmethod


class Music(ABC):
    @abstractmethod
    def do_play(self):
        pass


class Mp3(Music):
    def do_play(self):
        print("Playing .mp3 music!")


class Ogg(Music):
    def do_play(self):
        print("Playing .ogg music!")


class MusicFactory:
    _music_types = {
        "Mp3": Mp3,
        "Ogg": Ogg,
    }

    def play_sound(self, object_type):
        music_cls = self._music_types.get(object_type)
        if music_cls is None:
            raise ValueError(f"Unknown music type: {object_type}")
        return music_cls().do_play()


if __name__ == "__main__":
    mf = MusicFactory()
    music = input("Which music you want to play Mp3 or Ogg: ")
    mf.play_sound(music)

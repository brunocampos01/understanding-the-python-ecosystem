from abc import ABCMeta, abstractmethod

class Music():
  __metaclass__ = ABCMeta
  @abstractmethod
  def do_play(self):
    pass


class Mp3(Music):
  def do_play(self):
    print("Playing .mp3 music!")

class Ogg(Music):
  def do_play(self):
    print("Playing .ogg music!")

class MusicFactory(object):
  def play_sound(self, object_type):
  return eval(object_type)().do_play()


if __name__ == "__main__":
  mf = MusicFactory()
  music = input("Which music you want to play Mp3 or Ogg")
  mf.play_sound(music)

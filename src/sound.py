import pygame, os

if os.name == "nt":
    SCRIPT_PATH = os.getcwd()

class sound:
    _instance = None  # Stores the only instance of the class
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(sound, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 1024)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(7)

        #ALL SOUND VARIABLES    
        self.channel_backgound = pygame.mixer.Channel(6)

        self.snd_pellet = {
            0: pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "pellet1.wav")),
            1: pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "pellet2.wav"))}                   #usado
        self.snd_levelintro = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "levelintro.wav"))
        self.snd_default = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "default.wav"))
        self.snd_extrapac = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "extrapac.wav"))
        self.snd_gh2gohome = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "gh2gohome.wav"))
        self.snd_death = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "death.wav"))            #usado
        self.snd_powerpellet = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "powerpellet.wav"))#usado
        self.snd_powerpellet.set_volume(2)
        self.snd_eatgh = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "eatgh2.wav"))
        self.snd_fruitbounce = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "fruitbounce.wav"))
        self.snd_eatfruit = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "eatfruit.wav"))      #usado
        self.snd_extralife = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "extralife.wav"))

    
    def PlayBackgoundSound(self,snd):
        self.channel_backgound.stop()
        self.channel_backgound.play(snd, loops=-1)

    def SetMode(self, newMode):
        if newMode == 0:
            self.PlayBackgoundSound(self.snd_levelintro)
        elif newMode == 1:
            self.PlayBackgoundSound(self.snd_default)
        elif newMode == 2:
            self.PlayBackgoundSound(self.snd_death)
        elif newMode == 8:
            self.PlayBackgoundSound(self.snd_gh2gohome)
        elif newMode == 9:
            self.PlayBackgoundSound(self.snd_extrapac)
        else:
            self.channel_backgound.stop()

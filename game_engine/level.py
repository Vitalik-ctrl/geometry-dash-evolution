from .stereo_madness import create_stereo_madness_data

class Level:
    def __init__(self):
        self.obstacles = create_stereo_madness_data()

    def get_obstacles(self):
        return self.obstacles
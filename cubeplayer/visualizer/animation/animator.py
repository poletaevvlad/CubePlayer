from typing import List
from .animations import Animation


class Animator:
    def __init__(self):
        self.running_animations: List[Animation] = list()
        self.current_time: float = 0.0

    def add(self, animation: Animation, duration: float) -> None:
        animation.start_time = self.current_time
        animation.end_time = self.current_time + duration
        self.running_animations.append(animation)

    def run(self, delta_time: float) -> None:
        self.current_time += delta_time
        self.running_animations = [animation for animation in self.running_animations
                                   if animation.run(self.current_time)]

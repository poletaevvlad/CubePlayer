import math
import sys
from collections import deque
from typing import Deque

from libcube.actions import Action, Turn
from libcube.orientation import Side
from .animation import Animator, FloatAnimation, Animation
from .animation.easing import linear
from .cube import Cube
from .engine.camera import Camera


class CubeAnimationManager:
    def __init__(self, cube: Cube, animator: Animator, camera: Camera):
        self.queue: Deque[Action] = deque()
        self.cube: Cube = cube
        self.animator: Animator = animator
        self.camera: Camera = camera
        self.is_played: bool = False

    def enqueue(self, action: Action) -> None:
        self.queue.append(action)
        if not self.is_played:
            self._run_animation()

    def _create_turn_animation(self, action: Turn) -> Animation:
        turns = action.turns
        if action.side in {Side.FRONT, Side.RIGHT, Side.TOP}:
            turns = 4 - turns
        angle = math.radians(min(turns * 90, 360 - turns * 90))

        if action.side in {Side.LEFT, Side.RIGHT}:
            axis = "x"
            components_list = self.cube.layers_left
            if action.side == Side.RIGHT:
                components_list = components_list[::-1]
        elif action.side in {Side.TOP, Side.BOTTOM}:
            axis = "y"
            components_list = self.cube.layers_top
            if action.side == Side.BOTTOM:
                components_list = components_list[::-1]
        else:
            axis = "z"
            components_list = self.cube.layers_front
            if action.side == Side.BACK:
                components_list = components_list[::-1]
        components = [component for row in action.sides for component in components_list[row - 1]]

        def execution_callback(value: float) -> None:
            for component in components:
                component.set_temp_rotation(**{axis: value})

        def completion_callback() -> None:
            self._run_animation()
            for component in components:
                component.apply_temp_rotation()

        return FloatAnimation(0.0, angle, execution_callback, linear, completion_callback)

    def _run_animation(self) -> None:
        self.is_played = True
        animation = None
        while len(self.queue) > 0:
            action = self.queue.pop()
            if isinstance(action, Turn):
                animation = self._create_turn_animation(action)
                break
            else:
                print("Unknown action", file=sys.stderr)

        if animation is None:
            self.is_played = False
        else:
            self.animator.add(animation, 1)

import math
import sys
from collections import deque
from typing import Deque, Set, Callable, Optional

from libcube.actions import Action, Turn
from libcube.orientation import Side, Orientation
from .animation import Animator, FloatAnimation, Animation
from .animation.easing import ease_in_out_quad
from .cube import Cube, CubePart
from .engine.camera import Camera


class CubeAnimationManager:
    def __init__(self, cube: Cube, animator: Animator, camera: Camera,
                 position_callback: Optional[Callable[[float], None]] = None):
        self.queue: Deque[Action] = deque()
        self.cube: Cube = cube
        self.orientation: Orientation = Orientation()
        self.animator: Animator = animator
        self.camera: Camera = camera
        self.is_played: bool = False
        self.position_callback = position_callback
        self.completed_count = 0

    def enqueue(self, action: Action) -> None:
        self.queue.append(action)
        if not self.is_played:
            self._run_animation()

    def _get_parts_front(self, orientation: Orientation) -> Set[CubePart]:
        components = set()
        side = self.cube.cube.get_side(orientation)
        for i in range(1, side.rows - 1):
            for j in range(1, side.columns - 1):
                if side[i, j].data is not None:
                    components.add(side[i, j].data)
        return components

    def _get_parts_slice(self, orientation: Orientation, index: int) -> Set[CubePart]:
        components = set()
        for _ in range(4):
            side = self.cube.cube.get_side(orientation)
            components.update(x.data for x in side.get_column(index) if x.data is not None)
            orientation = orientation.to_top
        return components

    def _create_turn_animation(self, action: Turn) -> Animation:
        turns = action.turns
        if turns == 3:
            turns = -1
        if action.side in {Side.TOP, Side.BOTTOM}:
            turns = -turns
        angle = math.radians(90 * turns)

        if action.side in {Side.FRONT, Side.BACK}:
            axis = "z"
        elif action.side in {Side.LEFT, Side.RIGHT}:
            axis = "x"
        else:
            axis = "y"

        orientation = Orientation.regular(action.side)
        width = self.cube.cube.get_side(orientation).columns
        components = set()
        for index in action.sides:
            index -= 1
            if index == 0:
                components.update(self._get_parts_front(orientation))
            elif index == width - 1:
                components.update(self._get_parts_front(orientation.to_right.to_right))
            components.update(self._get_parts_slice(orientation.to_right, index))

        def execution_callback(value: float) -> None:
            for component in components:
                component.set_temp_rotation(**{axis: value})

        def completion_callback() -> None:
            for component in components:
                component.apply_temp_rotation()
            self._run_animation()
            self.completed_count += 1

        def fraction_callback(fraction):
            if self.position_callback is not None:
                self.position_callback(self.completed_count + fraction)

        return FloatAnimation(0.0, angle, execution_callback, ease_in_out_quad, completion_callback,
                              fraction_callback=fraction_callback)

    def _run_animation(self) -> None:
        self.is_played = True
        animation = None
        while len(self.queue) > 0 and animation is None:
            action = self.queue.pop()
            if isinstance(action, Turn):
                animation = self._create_turn_animation(action)
            else:
                print("Unknown action", file=sys.stderr)
            self.orientation = action.perform(self.cube.cube, self.orientation)

        if animation is None:
            self.is_played = False
        else:
            self.animator.add(animation, 0.3)

import math
import sys
from collections import deque
from typing import Deque, Set, Callable, Optional

from libcube.actions import Action, Turn, Rotate, TurningType
from libcube.orientation import Side, Orientation
from .animation import Animator, FloatAnimation, Animation, IdleAnimation
from .animation.easing import ease_in_out_quad
from .cube import Cube, CubePart
from .engine.camera import Camera


class WaitAction(Action):
    def __init__(self, duration: float):
        super(WaitAction, self).__init__()
        self.duration = duration

    def perform(self, cube: Cube, orientation: Orientation) -> Orientation:
        return orientation


class CubeAnimationManager:
    def __init__(self, cube: Cube, orientation: Orientation, animator: Animator, camera: Camera,
                 position_callback: Optional[Callable[[float], None]] = None):
        self.queue: Deque[Action] = deque()
        self.cube: Cube = cube
        self.orientation: Orientation = orientation
        self.animator: Animator = animator
        self.camera: Camera = camera
        self.is_played: bool = False
        self.position_callback = position_callback
        self.completed_count = 0
        self.finish_callback: Callable[[], None] = None

        self.turn_duration = [0.2, 0.3]
        self.rotation_duration = [0.2, 0.3]

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

    def _fraction_callback(self, fraction):
        if self.position_callback is not None:
            self.position_callback(self.completed_count + fraction)

    def _create_turn_animation(self, action: Turn) -> Animation:
        turns = action.turns
        if turns == 3:
            turns = -1
        if action.type == TurningType.HORIZONTAL:
            turns = -turns
        angle = math.radians(90 * turns)

        if action.type == TurningType.SLICE:
            axis = "z"
            side = Side.FRONT
        elif action.type == TurningType.VERTICAL:
            axis = "x"
            side = Side.LEFT
        else:
            axis = "y"
            side = Side.TOP

        orientation = Orientation.regular(side)
        width = self.cube.cube.get_side(orientation).columns
        components = set()
        for index in action.sides:
            if index > 0:
                index -= 1
            else:
                index = width + index

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

        return FloatAnimation(0.0, angle, execution_callback, ease_in_out_quad,
                              completion_callback,
                              fraction_callback=self._fraction_callback)

    def _create_rotate_animation(self, action: Rotate):
        if action.twice:
            delta_angle = math.pi
        elif action.axis_side in {Side.BACK, Side.LEFT, Side.BOTTOM}:
            delta_angle = -math.pi / 2
        else:
            delta_angle = math.pi / 2
        if action.axis_side in {Side.FRONT, Side.BACK}:
            axis_index = 2
        elif action.axis_side in {Side.LEFT, Side.RIGHT}:
            axis_index = 0
        else:
            axis_index = 1

        def execution_callback(value):
            self.cube.temp_rotation[axis_index] = value

        def completion_callback():
            self.cube.apply_rotation()
            self._run_animation()
            self.completed_count += 1

        current_rotation = self.cube.temp_rotation[axis_index]
        return FloatAnimation(current_rotation, current_rotation + delta_angle,
                              execution_callback, ease_in_out_quad,
                              completion_callback, self._fraction_callback)

    def _run_animation(self) -> None:
        self.is_played = True
        animation = None
        duration = 0
        while len(self.queue) > 0 and animation is None:
            action = self.queue.popleft()
            if isinstance(action, Turn):
                animation = self._create_turn_animation(action.from_orientation(self.orientation))
                duration = self.turn_duration[1 if action.turns == 2 else 0]
            elif isinstance(action, Rotate):
                animation = self._create_rotate_animation(action)
                duration = self.rotation_duration[1 if action.twice else 0]
            elif isinstance(action, WaitAction):
                animation = IdleAnimation(self._run_animation)
                duration = action.duration
            else:
                print("Unknown action", file=sys.stderr)
            self.orientation = action.perform(self.cube.cube, self.orientation)

        if animation is None:
            self.is_played = False
            if self.finish_callback is not None:
                self.finish_callback()
        else:
            self.animator.add(animation, duration)

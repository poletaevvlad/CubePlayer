from abc import abstractmethod, ABC
from typing import Callable, TypeVar, Generic, Optional

EasingFunction = Callable[[float], float]
CompletionCallback = Callable[[], None]
T = TypeVar("T")
ExecutionCallback = Callable[[T], None]


class Animation(Generic[T], ABC):
    def __init__(self, value_from: T, value_to: T, execution_callback: ExecutionCallback,
                 easing: EasingFunction, completion_callback: Optional[CompletionCallback] = None):
        self.value_from: T = value_from
        self.value_to: T = value_to
        self.easing: EasingFunction = easing
        self.completion_callback: Optional[CompletionCallback] = completion_callback
        self.execution_callback: ExecutionCallback = execution_callback
        self.start_time: float = 0
        self.end_time: float = 0

    @abstractmethod
    def interpolate(self, fraction: float) -> T:
        pass

    def run(self, current_time: float) -> bool:
        if self.end_time <= current_time:
            self.execution_callback(self.interpolate(self.easing(1.0)))
            if self.completion_callback is not None:
                self.completion_callback()
            return False

        fraction = (current_time - self.start_time) / (self.end_time - self.start_time)
        self.execution_callback(self.interpolate(self.easing(fraction)))
        return True


class FloatAnimation(Animation[float]):
    def interpolate(self, fraction: float) -> float:
        print(fraction)
        return self.value_to * fraction + self.value_from * (1 - fraction)

from abc import abstractmethod, ABC
from typing import Callable, TypeVar, Generic, Optional
from .easing import linear

EasingFunction = Callable[[float], float]
CompletionCallback = Callable[[], None]
T = TypeVar("T")
ExecutionCallback = Callable[[T], None]
FractionCallback = Callable[[float], None]


class Animation(Generic[T], ABC):
    def __init__(self, value_from: T, value_to: T, execution_callback: ExecutionCallback,
                 easing: EasingFunction, completion_callback: Optional[CompletionCallback] = None,
                 fraction_callback: Optional[FractionCallback] = None):
        self.value_from: T = value_from
        self.value_to: T = value_to
        self.easing: EasingFunction = easing
        self.completion_callback: Optional[CompletionCallback] = completion_callback
        self.execution_callback: ExecutionCallback = execution_callback
        self.start_time: float = 0
        self.end_time: float = 0
        self.fraction_callback = fraction_callback

    @abstractmethod
    def interpolate(self, fraction: float) -> T:
        pass

    def run(self, current_time: float) -> bool:
        if self.end_time <= current_time:
            fraction = self.easing(1.0)
            if self.fraction_callback is not None:
                self.fraction_callback(fraction)
            self.execution_callback(self.interpolate(fraction))
            if self.completion_callback is not None:
                self.completion_callback()
            return False

        fraction = self.easing((current_time - self.start_time) / (self.end_time - self.start_time))
        if self.fraction_callback is not None:
            self.fraction_callback(fraction)
        self.execution_callback(self.interpolate(fraction))
        return True


class FloatAnimation(Animation[float]):
    def interpolate(self, fraction: float) -> float:
        return self.value_to * fraction + self.value_from * (1 - fraction)


class IdleAnimation(Animation[None]):
    def __init__(self, completion_callback: CompletionCallback):
        super().__init__(None, None, lambda v: None, linear, completion_callback, None)

    def interpolate(self, fraction: float) -> T:
        return None

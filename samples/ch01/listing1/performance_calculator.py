import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

from samples.ch01.listing1.typings import Performance, Play


@dataclass
class PerformanceCalculatorMixin:
    perf: Performance
    play: Play


class PerformanceCalculator(ABC, PerformanceCalculatorMixin):
    @abstractmethod
    def get_amount(self) -> int:
        ...

    def get_volume_credits(self) -> int:
        return max(self.perf.audience - 30, 0)


@dataclass
class TragedyCalculator(PerformanceCalculator):
    def get_amount(self) -> int:
        result = 40000
        if self.perf.audience > 30:
            result += 1000 * (self.perf.audience - 30)
        return result


@dataclass
class ComedyCalculator(PerformanceCalculator):
    def get_amount(self) -> int:
        result = 30000
        if self.perf.audience > 20:
            result += 10000 + 500 * (self.perf.audience - 20)
        result += 300 * self.perf.audience
        return result

    def get_volume_credits(self) -> int:
        result = super().get_volume_credits()
        result += math.floor(self.perf.audience / 5)
        return result


def create_performance_calculator(
    perf: Performance, play: Play
) -> PerformanceCalculator:
    if play.type == "tragedy":
        return TragedyCalculator(perf, play)
    elif play.type == "comedy":
        return ComedyCalculator(perf, play)
    else:
        raise ValueError(f'Unknown genre: {play["type"]}')

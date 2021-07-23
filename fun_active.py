import math
from typing import List


class FunActive:

    @staticmethod
    def sumDendrite(arrDendrite: List[float], arrInputSignal: List[float]) -> float:
        try:
            return sum(dendrite * signal for dendrite, signal in zip(arrDendrite, arrInputSignal))
        except IndexError:
            raise IndexError("Колличество входных сиглалов привышает колличветсов в слое нейронов")

    @staticmethod
    def Extremes(inPutSum: float) -> int:
        return 1 if inPutSum >= 0.5 else 0

    ################################
    @staticmethod
    def Logistics(inPutSum: float) -> float:
        # -10 ... 1
        return 1 / (1 + pow(math.e, -inPutSum))

    @staticmethod
    def LogisticsDerivative(outPut: float) -> float:
        return outPut * (1 - outPut)

    ################################
    @staticmethod
    def HyperbolicTangent(inPutSum: float) -> float:
        # -1 ... 1
        return (pow(math.e, inPutSum) - pow(math.e, -inPutSum)) / (
                pow(math.e, inPutSum) + pow(math.e, -inPutSum))

    @staticmethod
    def HyperbolicTangentDerivative(outPut: float) -> float:
        return (1 + outPut) * (1 - outPut)

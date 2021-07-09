import math
from typing import List


class FunActive:

    @staticmethod
    def sumDendrite(arrDendrite: List[float], arrInputSignal: List[float]) -> float:
        if len(arrDendrite) != len(arrInputSignal):
            raise IndexError("Колличество входных сиглалов привышает колличветсов в слое нейронов")
        resSum: float = 0.0
        for dendrite, signal in zip(arrDendrite, arrInputSignal):
            resSum += dendrite * signal
        return resSum

    @staticmethod
    def Extremes(inPutSum: float) -> int:
        outPut = 1 if inPutSum >= 0.5 else 0
        return outPut

    ################################
    @staticmethod
    def Logistics(inPutSum: float) -> float:
        # -10 ... 1
        outPut = 1 / (1 + pow(math.e, -inPutSum))
        return outPut

    @staticmethod
    def LogisticsDerivative(outPut: float) -> float:
        return outPut * (1 - outPut)

    ################################
    @staticmethod
    def HyperbolicTangent(inPutSum: float) -> float:
        # -1 ... 1
        outPut = (pow(math.e, inPutSum) - pow(math.e, -inPutSum)) / (
                pow(math.e, inPutSum) + pow(math.e, -inPutSum))
        return outPut

    @staticmethod
    def HyperbolicTangentDerivative(outPut: float) -> float:
        return (1 + outPut) * (1 - outPut)

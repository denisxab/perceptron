import math
from typing import List


class FunActive:

    def __init__(self):
        # # Выходной сигнал нейрона
        # self.outPut: Optional[float] = None  # F ij
        # self.inPut: Optional[float] = None  # V ij
        pass

    @staticmethod
    def sumDendrite(arrDendrite: List[float], arrInputSignal: List[int]) -> float:
        if len(arrDendrite) != len(arrInputSignal):
            raise IndexError("Колличество входных сиглалов привышает колличветсов в слое нейронов")
        resSum: float = 0.0
        for dendrite, signal in zip(arrDendrite, arrInputSignal):
            resSum += dendrite * signal
        return resSum

    @staticmethod
    def Extremes(neuron, arrInputSignal: List[int]) -> int:
        inPut = FunActive.sumDendrite(neuron.arrLastWeight, arrInputSignal)
        outPut = 1 if inPut >= 0.5 else 0
        return outPut

    ################################
    def Logistics(self, arrDendrite: List, arrInputSignal: List[int]) -> float:
        # -10 ... 1
        self.inPut = FunActive.sumDendrite(arrDendrite, arrInputSignal)
        self.outPut = 1 / (1 + pow(math.e, -self.inPut))
        return self.outPut

    @staticmethod
    def LogisticsDerivative(outPut: float) -> float:
        return outPut * (1 - outPut)

    ################################
    def HyperbolicTangent(self, arrDendrite: List, arrInputSignal: List[int]) -> float:
        # -1 ... 1
        self.inPut = FunActive.sumDendrite(arrDendrite, arrInputSignal)
        self.outPut = (pow(math.e, self.inPut) - pow(math.e, -self.inPut)) / (
                pow(math.e, self.inPut) + pow(math.e, -self.inPut))
        return self.outPut

    @staticmethod
    def HyperbolicTangentDerivative(outPut: float) -> float:
        return (1 + outPut) * (1 - outPut)

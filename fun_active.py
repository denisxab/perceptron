from typing import List

from perceptron import Dendrite


class FunActive:

    @staticmethod
    def sumDendrite(arrDendrite: List[Dendrite], arrInputSignal: List[int]) -> float:
        if len(arrDendrite) != len(arrInputSignal):
            raise IndexError()

        resSum: float = 0.0
        for itemD in range(len(arrDendrite)):
            resSum += arrDendrite[itemD].weight * arrInputSignal[itemD]
        return resSum

    @staticmethod
    def Extremes(arrDendrite: List[Dendrite], arrInputSignal: List[int]) -> int:
        resSum = FunActive.sumDendrite(arrDendrite, arrInputSignal)
        if resSum >= 0.5:
            return 1
        elif resSum < 0.5:
            return 0

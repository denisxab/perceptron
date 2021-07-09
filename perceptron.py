import random
from typing import List, Optional

from structure_neuron import Neuron


class LayerNeuron:
    def __init__(self, CountInputDendrite: int):
        self.Layer: List[List[Optional[Neuron]]] = [[Neuron() for _ in range(CountInputDendrite)]]
        self.CountLayer: int = 1

    def addNeuronInLayer(self, CountNeuron, weight: List[List[float]]):  # -!

        if len(weight) != len(self.Layer[-1]):
            raise IndexError("Колличество weight не совподает с колличеством нейронов на прошлом слое")

        tmpArrNeuron: List[Neuron] = []
        for item in range(CountNeuron):
            tmpArrNeuron.append(Neuron(weight))

        self.Layer.append(tmpArrNeuron)
        self.CountLayer += 1

    def addCountNeuronInLayer(self, countNeuronInLayer: int):  # +
        tmpArrNeuron: List[Neuron] = []
        for item in range(countNeuronInLayer):
            tmpArrWeight: List[float] = [random.uniform(-0.5, 0.5) for _ in self.Layer[-1]]
            tmpArrNeuron.append(Neuron(tmpArrWeight))

        self.Layer.append(tmpArrNeuron)
        self.CountLayer += 1

    def CalculateSignal(self, signal: List[int], FunCalc) -> List[float]:
        selectSignal: List[int] = signal.copy()
        for layer in self.Layer[1:]:  # Пропускам входной слой
            tmpSignal: List[int] = []
            for neuron in layer:
                tmpSignal.append(FunCalc(neuron, selectSignal))
            selectSignal = tmpSignal
        return selectSignal

    def Train(self, signalList: List[List[int]], requiredValueList: List[int], *,
              ConvergenceStep: float,  # L
              DerivativeFun  # D
              ):

        if len(signalList) != len(requiredValueList):
            raise IndexError()

        for itemSignal, itemRequired in zip(signalList, requiredValueList):  # +

            ReversIndexLayer: int = -1
            for Y, SelectTraineeNeuron in zip(self.CalculateSignal(itemSignal),
                                              self.Layer[ReversIndexLayer]):  # Выходной результат
                E = Y - itemRequired  # Ошибка выходного нейрона
                SelectTraineeNeuron.Delta = E * DerivativeFun(SelectTraineeNeuron.outPut)
                for selectDendrite in SelectTraineeNeuron.arrLastNeuron:
                    selectDendrite.weight = selectDendrite.weight - (
                            ConvergenceStep * SelectTraineeNeuron.Delta * selectDendrite.neuron.outPut)

    def __repr__(self) -> str:
        res: str = ""
        for item in self.Layer:
            res += f"{len(item)}:"
        res = res[:-1:]
        return res


if __name__ == '__main__':
    pass

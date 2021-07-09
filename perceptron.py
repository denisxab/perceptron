import random
from typing import List, Union

from fun_active import FunActive
from structure_neuron import Neuron, TraineeNeuron


class Layer:

    def __init__(self, CountInputDendrite: int, TypeNeuron,
                 FunCalc: Union[FunActive.Extremes,
                                FunActive.Logistics,
                                FunActive.HyperbolicTangent]):
        self.Layer: List[List[Union[Neuron, TraineeNeuron]]] = [[TypeNeuron() for _ in range(CountInputDendrite)]]
        self.FunActive: Union[FunActive.Extremes,
                              FunActive.Logistics,
                              FunActive.HyperbolicTangent] = FunCalc
        self.CountLayer: int = 1

    def addNeuronInLayer(self, weight: List[List[float]], CheckLen: bool = True):  # +
        raise AttributeError

    def addCountNeuronInLayer(self, countNeuronInLayer: int):  # +
        raise AttributeError

    def CalculateSignal(self, signal: List[int]) -> List[float]:  # +
        raise AttributeError

    def __repr__(self) -> str:  # +
        res: str = ""
        for item in self.Layer:
            res += f"{len(item)}:"
        res = res[:-1:]
        return res


class LayerNeuron(Layer):
    def __init__(self, CountInputDendrite: int, FunCalc: Union[FunActive.Extremes,
                                                               FunActive.Logistics,
                                                               FunActive.HyperbolicTangent]):
        super().__init__(CountInputDendrite, Neuron, FunCalc)

    def addNeuronInLayer(self, weight: List[List[float]], CheckLen: bool = True):  # +
        """
        :param weight: [Колличество Нейрон][Вес для прошлых нейронов]
        :param CheckLen: Провертять входные данные на коректность
        """
        if CheckLen:
            for item in weight:
                if len(item) != len(self.Layer[-1]):
                    raise IndexError("Колличество weight не совподает с колличеством нейронов на прошлом слое")

        tmpArrNeuron: List[Neuron] = []
        for item in weight:
            tmpArrNeuron.append(Neuron(item))

        self.Layer.append(tmpArrNeuron)
        self.CountLayer += 1

    def addCountNeuronInLayer(self, countNeuronInLayer: int):  # +
        tmpArrNeuron: List[Neuron] = []
        for item in range(countNeuronInLayer):
            tmpArrWeight: List[float] = [random.uniform(-0.5, 0.5) for _ in self.Layer[-1]]
            tmpArrNeuron.append(Neuron(tmpArrWeight))

        self.Layer.append(tmpArrNeuron)
        self.CountLayer += 1

    def CalculateSignal(self, signal: List[int]) -> List[float]:  # +
        selectSignal: List[float] = signal.copy()
        for layer in self.Layer[1:]:  # Пропускам входной слой
            tmpSignal: List[float] = []
            for neuron in layer:
                # Находим сумму  E(w*x)
                inPut = FunActive.sumDendrite(neuron.arrLastWeight, selectSignal)
                # Проверяем ее черезф ункцию активации
                tmpSignal.append(self.FunActive(inPut))
            selectSignal = tmpSignal
        return selectSignal


class LayerTraineeNeuron(Layer):
    def __init__(self, CountInputDendrite: int, FunCalc: Union[FunActive.Extremes,
                                                               FunActive.Logistics,
                                                               FunActive.HyperbolicTangent]):
        super().__init__(CountInputDendrite, TraineeNeuron, FunCalc)

    def addNeuronInLayer(self, weight: List[List[float]], CheckLen: bool = True):  # +
        pass

    def addCountNeuronInLayer(self, countNeuronInLayer: int):  # +
        tmpArrNeuron: List[TraineeNeuron] = []
        for item in range(countNeuronInLayer):
            tmpArrWeight: List[float] = [random.uniform(-0.5, 0.5) for _ in self.Layer[-1]]
            tmpArrNeuron.append(TraineeNeuron(arrLastWeight=tmpArrWeight))

        self.Layer.append(tmpArrNeuron)
        self.CountLayer += 1

    def CalculateSignal(self, signal: List[int]) -> List[float]:  # +
        """
        Эта функция должна заполнить Входные и Выходные заняения у нейронов
        """

        selectSignal: List[float] = signal.copy()

        # Заполняем Выходные заняениу нейронов первого(входного) Слоя
        for neuron, signal in zip(self.Layer[0], selectSignal):
            neuron.FOutputSignal = signal

        for layer in self.Layer[1:]:  # Пропускам входной слой
            tmpSignal: List[float] = []
            for neuron in layer:
                neuron.VInputSignal = FunActive.sumDendrite(neuron.arrLastWeight, selectSignal)
                neuron.FOutputSignal = self.FunActive(neuron.VInputSignal)
                tmpSignal.append(neuron.FOutputSignal)
            selectSignal = tmpSignal
        return selectSignal


class TraineeNetwork:
    def __init__(self, ObjectLayerNeuron: LayerTraineeNeuron):
        self.LayerNeuron = ObjectLayerNeuron

    def TraineeBackPropagation(self, signalList: List[List[int]], requiredValueList: List[int], *,
                               ConvergenceStep: float,  # L
                               DerivativeFun: Union[
                                   FunActive.LogisticsDerivative,
                                   FunActive.HyperbolicTangentDerivative
                               ]  # D
                               ):

        if len(signalList) != len(requiredValueList):
            raise IndexError()

        for itemSignal, itemRequired in zip(signalList, requiredValueList):  # +

            # Высчитваем и устанавиваем всем Тренеровачным Нейронам входыне и выходные значения
            self.LayerNeuron.CalculateSignal(itemSignal)

            ReversIndexLayer: int = -1
            for Y, SelectTraineeNeuron in zip(self.LayerNeuron.CalculateSignal(itemSignal),
                                              self.Layer[ReversIndexLayer]):  # Выходной результат
                E = Y - itemRequired  # Ошибка выходного нейрона
                SelectTraineeNeuron.Delta = E * DerivativeFun(SelectTraineeNeuron.outPut)
                for selectDendrite in SelectTraineeNeuron.arrLastNeuron:
                    selectDendrite.weight = selectDendrite.weight - (
                            ConvergenceStep * SelectTraineeNeuron.Delta * selectDendrite.neuron.outPut)


if __name__ == '__main__':
    pass

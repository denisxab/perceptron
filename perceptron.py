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

    def TraineeBackPropagation(self, signalList: List[List[int]], requiredValueList: List[List[int]], *,
                               ConvergenceStep: float,  # L 0.1 .. 0.001
                               DerivativeFun: Union[
                                   FunActive.LogisticsDerivative,
                                   FunActive.HyperbolicTangentDerivative
                               ]  # D
                               ):

        # Проверка того что колличетсво входных сигланов и колличетсов нужных ответов совподают по длинне
        if len(signalList) != len(requiredValueList):
            raise IndexError()

        # Провекра того что Массив с нужными ответами соответсвует по длинне с колличеством выходных нейронов
        if len(requiredValueList) != len(self.Layer[-1]):
            raise IndexError()

        # Тестовый счетсчик
        Count: float = 1

        for itemSignal, itemRequired in zip(signalList, requiredValueList):
            """
            W = Веса меняються независимо
            Delta = меняться только когда известны все нейроны
            """
            # Кратектеровка весов выходного слоя #
            IndexRequired: int = 0  # Ошибка выходного нейрона должна высчитываться для каждого нужного результата
            for N, Y in zip(self.Layer[-1], self.CalculateSignal(itemSignal)):
                E = Y - itemRequired[IndexRequired]  # Ошибка выходного нейрона
                N.Delta = E * DerivativeFun(N.VInputSignal)  # Вычисляем локальыней градиент для выходного нейронеа
                # Коректируем веса у выходного нейрона
                for index, W in enumerate(N.arrLastWeight):
                    N.arrLastWeight[
                        index] = Count  # W - (ConvergenceStep * N.Delta * self.Layer[-2][index].FOutputSignal)
                    Count += 1
                IndexRequired += 1

            # Кратектеровка весов скрытого слоя #
            for indexLayer in range(-2, -self.CountLayer, -1):
                for index2, N2 in enumerate(self.Layer[indexLayer]):
                    Q: float = 0.0
                    for x in self.Layer[-1]:
                        Q += x.Delta * x.arrLastWeight[index2]
                    N2.Delta = Q * DerivativeFun(N2.VInputSignal)
                    # Коректируем веса
                    for index, W in enumerate(N2.arrLastWeight):
                        N2.arrLastWeight[index] = W - (
                                ConvergenceStep * N2.Delta * self.Layer[-2][index].FOutputSignal)
            # Вычисляем локальыней градиент для нейронов скрытого слоя
            #
            # for N in self.Layer[-2]:
            #     N.Delta = Q * DerivativeFun(N.VInputSignal)
            #     # Устанавливаем локальынй градиент для нового сктырого слоя
            #     self.Layer[-2][index].Delta = N.Delta * W * self.Layer[-2][index].VInputSignal
            # Высчитывать Delta
            #
            # # Коректировать Весса
            #
            # ReversIndexLayer: int = -1
            # for Y, SelectTraineeNeuron in zip(self.LayerNeuron.CalculateSignal(itemSignal),
            #                                   self.Layer[ReversIndexLayer]):  # Выходной результат
            #     E = Y - itemRequired  # Ошибка выходного нейрона
            #     SelectTraineeNeuron.Delta = E * DerivativeFun(SelectTraineeNeuron.outPut)
            #     for selectDendrite in SelectTraineeNeuron.arrLastNeuron:
            #         selectDendrite.weight = selectDendrite.weight - (
            #                 ConvergenceStep * SelectTraineeNeuron.Delta * selectDendrite.neuron.outPut)


if __name__ == '__main__':
    pass

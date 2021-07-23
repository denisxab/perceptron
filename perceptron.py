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
                                                               FunActive.HyperbolicTangent],
                 DerivativeFun: Union[FunActive.LogisticsDerivative, FunActive.HyperbolicTangentDerivative]):
        """
        :param CountInputDendrite:  Колличество входных слоев
        :param FunCalc: Функция активации
        :param DerivativeFun: Произвлодная функции активации
        """
        super().__init__(CountInputDendrite, TraineeNeuron, FunCalc)
        self.DerivativeFun = DerivativeFun

    def addNeuronInLayer(self, weight: List[List[float]], CheckLen: bool = True):  # +
        pass

    def addCountNeuronInLayer(self, countNeuronInLayer: int):  # +
        tmpArrNeuron: List[TraineeNeuron] = []
        for item in range(countNeuronInLayer):
            tmpArrWeight: List[float] = [0 for _ in self.Layer[-1]]
            # [random.uniform(-0.5, 0.5) for _ in self.Layer[-1]]
            tmpArrNeuron.append(TraineeNeuron(arrLastWeight=tmpArrWeight))

        self.Layer.append(tmpArrNeuron)
        self.CountLayer += 1

    def CalculateSignal(self, signal: List[int]) -> List[float]:  # +
        """
        Эта функция должна заполнить Входные и Выходные значения у всех нейронов
        а также вернть результат работы Персептрона
        """
        selectSignal: List[float] = signal.copy()
        # Заполняем Выходные значения нейронов первого(входного) Слоя
        for neuron, signal in zip(self.Layer[0], selectSignal):
            neuron.FOutputSignal = signal
        # Заполняем Выходные и Выходные значения у всех нейронов кроме первого слоя
        for layer in self.Layer[1:]:
            tmpSignal: List[float] = []
            for neuron in layer:
                neuron.VInputSignal = FunActive.sumDendrite(neuron.arrLastWeight, selectSignal)
                neuron.FOutputSignal = self.FunActive(neuron.VInputSignal)
                tmpSignal.append(neuron.FOutputSignal)
            selectSignal = tmpSignal
        return selectSignal

    def TraineeBackPropagation(self, signalList: List[List[int]], requiredValueList: List[List[int]], *,
                               ConvergenceStep: float, Epochs: int, StopSum: float
                               ):
        """
        :param signalList: Массив с входными сигналами
        :param requiredValueList: Массив с требуемыми овтетами сети
        :param ConvergenceStep: Шаг обучения. чем меньше тем точнее но дольше настройка (0.1 ... 0.001)
        :param Epochs: Колличество циклов обучения(корекции весов)
        """

        # Проверка того что колличетсво входных сигланов и колличетсов требуемых ответов совподают по длинне
        if len(signalList) != len(requiredValueList):
            raise IndexError()

        # Провекра того что массив с требуемыми ответами соответсвует по длинне с колличеством выходных нейронов
        for R in requiredValueList:
            if len(R) != len(self.Layer[-1]):
                raise IndexError()
        del R
        """
        W = Веса меняються независимо
        Delta = Зависима и меняться только когда известны все W и Delta на преидущем слое
        """
        SumE: float = 0.0
        for indexEpoch in range(Epochs):
            for itemSignal, itemRequired in zip(signalList, requiredValueList):
                # Кратектеровка весов и усатвновка Delta дял нейронов выходного слоя #
                IndexRequired: int = 0  # Индекс для связи Номера ответа нейрона и Требуемого ответа для этого нйерона
                for N, Y in zip(self.Layer[-1], self.CalculateSignal(itemSignal)):
                    E = Y - itemRequired[IndexRequired]  # Ошибка для нейрона выходного слоя
                    SumE += E  # Общая сумма ошибки сети - нужня для статистики
                    N.Delta = E * self.DerivativeFun(
                        N.VInputSignal)  # Вычисляем локальыней градиент для нейрона выходного нейронеа
                    # Коректировка весов у нейрона выходного нейрона
                    for index, W in enumerate(N.arrLastWeight):
                        N.arrLastWeight[
                            index] = W - (ConvergenceStep * N.Delta * self.Layer[-2][index].FOutputSignal)
                    IndexRequired += 1

                del E, IndexRequired, Y, W, N, index
                # Навигация по слоям, начало от пердвыходного слоя до входного слоя
                for indexLayer in range(-2, -self.CountLayer, -1):
                    # Кратектеровка весов и установка Delta для нейронов скрытого и входного слоя#
                    for index2, N2 in enumerate(self.Layer[indexLayer]):
                        # Суммирования градиентов локальных ошибок
                        Q = sum(x.Delta * x.arrLastWeight[indexLayer + 1] for x in self.Layer[-1])

                        N2.Delta = Q * self.DerivativeFun(N2.VInputSignal)
                        # Коректируем веса
                        for index, W in enumerate(N2.arrLastWeight):
                            N2.arrLastWeight[
                                index] = W - (
                                    ConvergenceStep * N2.Delta * self.Layer[indexLayer - 1][index].FOutputSignal)

            print(f"{indexEpoch}:\t\t{SumE}")
            if SumE < 0.0:
                break
            SumE = 0.0

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

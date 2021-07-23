import unittest

from fun_active import FunActive
from perceptron import LayerNeuron, LayerTraineeNeuron


class Test_Perceptron(unittest.TestCase):

    @unittest.skip('1')
    def test_addCountNeuronInLayer(self):
        # Проверка создания слоев через указания колличества нейронов
        # И произвольным вессом
        # Input
        TmpLayer = LayerNeuron(CountInputDendrite=3, FunCalc=FunActive.Extremes)
        # Hide 1
        TmpLayer.addCountNeuronInLayer(3)
        # Hide 2
        TmpLayer.addCountNeuronInLayer(2)
        # Output
        TmpLayer.addCountNeuronInLayer(2)
        self.assertEqual(len(TmpLayer.Layer), 4)
        self.assertEqual(TmpLayer.CountLayer, 4)
        testArr = [3, 3, 2, 2]
        for Tmp, Tes in zip(TmpLayer.Layer, testArr):
            self.assertEqual(len(Tmp), Tes)

    def test_LayerNeuron_CalculateSignal(self):
        # Input
        TmpLayer = LayerNeuron(CountInputDendrite=3, FunCalc=FunActive.Extremes)
        # Hide 1
        TmpLayer.addCountNeuronInLayer(3)
        # Hide 2
        TmpLayer.addCountNeuronInLayer(2)
        # Output
        TmpLayer.addCountNeuronInLayer(2)

        хорошая_погода = 0
        дождь = 1
        усаталось = 0

        Signal = [
            хорошая_погода,
            дождь,
            усаталось,
        ]
        self.assertEqual(len(TmpLayer.CalculateSignal(Signal)), 2)

    @unittest.skip('1')
    def test_addNeuronInLayer(self):
        # Проверка создания слоев с указанием в ручную вессов
        # Input
        TmpLayer = LayerNeuron(CountInputDendrite=3, FunCalc=FunActive.Extremes)

        # Hide 1
        TmpLayer.addNeuronInLayer(
            [[1,
              -1,
              -1, ],  # только в хорошую

             [1,
              -0.3,
              -1, ]]  # либо в хорошую и ветеренную погоду
        )

        # Output
        TmpLayer.addNeuronInLayer(
            [[0.5,
              0.5, ]]
        )

        Signal = [
            1,  # Хорошая погода
            1,  # Ветер
            0  # Дождь
        ]

        # Проверка подсчета
        self.assertEqual(TmpLayer.CalculateSignal(Signal)[0], 1)
        # Проверка обработки ошибки при работе CheckLen
        self.assertRaises(IndexError, TmpLayer.addNeuronInLayer,
                          [[0.5,
                            -0.5,
                            -0.5, ],
                           [0.5,
                            -0.5,
                            -0.5, 0.1111]], CheckLen=True)

    @unittest.skip('1')
    def test_LayerTraineeNeuron(self):
        # Input
        TmpLayer = LayerTraineeNeuron(CountInputDendrite=3, FunCalc=FunActive.Extremes, DerivativeFun=None)
        # Hide 1
        TmpLayer.addCountNeuronInLayer(3)
        # Hide 2
        TmpLayer.addCountNeuronInLayer(2)
        # Output
        TmpLayer.addCountNeuronInLayer(2)
        self.assertEqual(len(TmpLayer.Layer), 4)
        self.assertEqual(TmpLayer.CountLayer, 4)
        testArr = [3, 3, 2, 2]
        for Tmp, Tes in zip(TmpLayer.Layer, testArr):
            self.assertEqual(len(Tmp), Tes)

    @unittest.skip('1')
    def test_LayerTraineeNeuron_CalculateSignal(self):

        # Input
        TmpLayer = LayerTraineeNeuron(CountInputDendrite=3, FunCalc=FunActive.Extremes, DerivativeFun=None)
        # Hide 1
        TmpLayer.addCountNeuronInLayer(3)
        # Hide 2
        TmpLayer.addCountNeuronInLayer(2)
        # Output
        TmpLayer.addCountNeuronInLayer(2)

        хорошая_погода = 0
        дождь = 1
        усаталось = 0

        Signal = [
            хорошая_погода,
            дождь,
            усаталось,
        ]
        TmpLayer.CalculateSignal(Signal)
        self.assertEqual(len(TmpLayer.CalculateSignal(Signal)), 2)
        self.assertNotEqual(type(TmpLayer.Layer[0][0].VInputSignal), int)
        self.assertNotEqual(TmpLayer.Layer[0][0].FOutputSignal, None)

    def test_Train(self):

        # # Hide 1
        # TmpLayer.addCountNeuronInLayer(3)
        # # Hide 2
        # TmpLayer.addCountNeuronInLayer(2)
        # # Output
        # TmpLayer.addCountNeuronInLayer(2)

        # SignalList = [
        #     [1, 1, 1],
        #     [0, 0, 0],
        # ]

        # RequiredList = [[1], [0]]
        # RequiredList = [
        #     [1, 0],
        #     [0, 1],
        # ]

        # # Проверка подсчета
        # self.assertEqual(TmpLayer.CalculateSignal(Signal)[0], 1)

        t = [
            1,  # Хорошая погода
            1,  # Ветер
            0  # Дождь
        ]

        SignalList = [
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 0],

            [0, 1, 0],
            [0, 0, 1],
            [0, 1, 1],

        ]
        RequiredList = [
            [1],
            [1],
            [1],

            [0],
            [0],
            [0],
        ]

        # Input
        TmpLayer = LayerTraineeNeuron(CountInputDendrite=3, FunCalc=FunActive.Logistics,
                                      DerivativeFun=FunActive.LogisticsDerivative)

        TmpLayer.addCountNeuronInLayer(2)
        TmpLayer.addCountNeuronInLayer(1)

        # Обучение
        TmpLayer.TraineeBackPropagation(SignalList,
                                        RequiredList,
                                        ConvergenceStep=0.01,
                                        Epochs=100, StopSum=0.01)
        print("*" * 40)
        for s, r in zip(SignalList, RequiredList):
            print(f"{s} : {TmpLayer.CalculateSignal(s)} : {r}")

        print()


if __name__ == '__main__':
    unittest.main()

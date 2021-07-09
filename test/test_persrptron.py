import unittest

from fun_active import FunActive
from perceptron import LayerNeuron, LayerTraineeNeuron


class Test_Perceptron(unittest.TestCase):

    # @unittest.skip("-")
    # def test_Example1(self):
    #     TmpLayer = LayerNeuron()
    #
    #     ######################
    #     TmpNeuron = Neuron()
    #     ArrInput = [
    #         Dendrite(weight=0.5),
    #         Dendrite(weight=-0.5),
    #         Dendrite(weight=-0.5),
    #         Dendrite(weight=1),
    #     ]
    #     for item in ArrInput:
    #         TmpNeuron.addDendriteOrHideNeuron(item)
    #     ######################
    #
    #     ######################
    #     TmpLayer.addNeuronInLayer(TmpNeuron)
    #     ######################
    #
    #     ######################
    #     хорошая_погода = 0
    #     дождь = 1
    #     усаталось = 0
    #     позвали_гулять = 1
    #     Signal = [
    #         хорошая_погода,
    #         дождь,
    #         усаталось,
    #         позвали_гулять,
    #     ]
    #     # print(TmpLayer.CalculateSignal(Signal))
    #     self.assertEqual(TmpLayer.CalculateSignal(Signal), 1)
    #     ######################
    #
    # @unittest.skip("-")
    # def test_Example2(self):
    #     TmpLayer = LayerNeuron()
    #
    #     ######################
    #     # Layer 1
    #     ######################
    #     # Neuron 1
    #     ArrInput1 = [
    #         Dendrite(weight=0.5),
    #         Dendrite(weight=-0.5),
    #         Dendrite(weight=-0.5),
    #         Dendrite(weight=1),
    #     ]
    #     TmpNeuron1 = Neuron()
    #     for item1 in ArrInput1:
    #         TmpNeuron1.addDendriteOrHideNeuron(item1)
    #     TmpLayer.addNeuronInLayer(TmpNeuron1)
    #     ######################
    #
    #     ######################
    #     # Neuron 2
    #     ArrInput2 = [
    #         Dendrite(weight=0.3),
    #         Dendrite(weight=-0.2),
    #         Dendrite(weight=0.3),
    #         Dendrite(weight=0.8),
    #     ]
    #     TmpNeuron2 = Neuron()
    #     for item2 in ArrInput2:
    #         TmpNeuron2.addDendriteOrHideNeuron(item2)
    #     TmpLayer.addNeuronInLayer(TmpNeuron2)
    #     ######################
    #
    #     ######################
    #     TmpLayer.NewLayer()
    #     ######################
    #
    #     ######################
    #     # Layer 2
    #     TmpNeuron3 = Neuron()
    #     ArrHideNeron = [
    #         HediNeron(TmpNeuron1, weight=0.5),
    #         HediNeron(TmpNeuron2, weight=-0.4)
    #     ]
    #     for item3 in ArrHideNeron:
    #         TmpNeuron3.addDendriteOrHideNeuron(item3)
    #     TmpLayer.addNeuronInLayer(TmpNeuron3)
    #     ######################
    #
    #     ######################
    #     хорошая_погода = 0
    #     дождь = 1
    #     усаталось = 0
    #     позвали_гулять = 1
    #     Signal = [
    #         хорошая_погода,
    #         дождь,
    #         усаталось,
    #         позвали_гулять,
    #     ]
    #     print(TmpLayer.CalculateSignal(Signal))
    #     ######################
    #     self.assertEqual(TmpLayer.CalculateSignal(Signal), 0)

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
        # Проверка обравботки ошибки при работе CheckLen
        self.assertRaises(IndexError, TmpLayer.addNeuronInLayer,
                          [[0.5,
                            -0.5,
                            -0.5, ],
                           [0.5,
                            -0.5,
                            -0.5, 0.1111]], CheckLen=True)

    def test_LayerTraineeNeuron(self):
        # Input
        TmpLayer = LayerTraineeNeuron(CountInputDendrite=3, FunCalc=FunActive.Extremes)
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

    def test_LayerTraineeNeuron_CalculateSignal(self):

        # Input
        TmpLayer = LayerTraineeNeuron(CountInputDendrite=3, FunCalc=FunActive.Extremes)
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
        self.assertNotEqual(TmpLayer.Layer[0][0].VInputSignal, None)
        self.assertNotEqual(TmpLayer.Layer[0][0].FOutputSignal, None)

    def test_Train(self):
        # Input
        TmpLayer = LayerTraineeNeuron(CountInputDendrite=3, FunCalc=FunActive.Logistics)
        # Hide 1
        TmpLayer.addCountNeuronInLayer(3)
        # Hide 2
        TmpLayer.addCountNeuronInLayer(2)
        # Output
        TmpLayer.addCountNeuronInLayer(2)

        SignalList = [
            1, 1, 1,
            0, 0, 0,
            1, 0, 1,
            0, 1, 1,
        ]

        RequiredList = [
            1,
            0,
            1,
            0,
        ]

        cls = TraineeNetwork(TmpLayer)
        cls.TraineeBackPropagation(SignalList,
                                   RequiredList,
                                   ConvergenceStep=0.1,
                                   DerivativeFun=FunActive.LogisticsDerivative)


if __name__ == '__main__':
    unittest.main()

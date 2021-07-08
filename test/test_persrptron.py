import unittest

from perceptron import *


class Test_Perceptron(unittest.TestCase):

    def test_Example1(self):
        TmpLayer = LayerNeuron()

        ######################
        TmpNeuron = Neuron()
        ArrInput = [
            Dendrite(weight=0.5),
            Dendrite(weight=-0.5),
            Dendrite(weight=-0.5),
            Dendrite(weight=1),
        ]
        for item in ArrInput:
            TmpNeuron.addDendriteOrHideNeuron(item)
        ######################

        ######################
        TmpLayer.addNeuronInLayer(TmpNeuron)
        ######################

        ######################
        хорошая_погода = 0
        дождь = 1
        усаталось = 0
        позвали_гулять = 1
        Signal = [
            хорошая_погода,
            дождь,
            усаталось,
            позвали_гулять,
        ]
        # print(TmpLayer.CalculateSignal(Signal))
        self.assertEqual(TmpLayer.CalculateSignal(Signal), 1)
        ######################

    def test_Example2(self):
        TmpLayer = LayerNeuron()

        ######################
        # Layer 1
        ######################
        # Neuron 1
        ArrInput1 = [
            Dendrite(weight=0.5),
            Dendrite(weight=-0.5),
            Dendrite(weight=-0.5),
            Dendrite(weight=1),
        ]
        TmpNeuron1 = Neuron()
        for item1 in ArrInput1:
            TmpNeuron1.addDendriteOrHideNeuron(item1)
        TmpLayer.addNeuronInLayer(TmpNeuron1)
        ######################

        ######################
        # Neuron 2
        ArrInput2 = [
            Dendrite(weight=0.3),
            Dendrite(weight=-0.2),
            Dendrite(weight=0.3),
            Dendrite(weight=0.8),
        ]
        TmpNeuron2 = Neuron()
        for item2 in ArrInput2:
            TmpNeuron2.addDendriteOrHideNeuron(item2)
        TmpLayer.addNeuronInLayer(TmpNeuron2)
        ######################

        ######################
        TmpLayer.NewLayer()
        ######################

        ######################
        # Layer 2
        TmpNeuron3 = Neuron()
        ArrHideNeron = [
            HediNeron(TmpNeuron1, weight=0.5),
            HediNeron(TmpNeuron2, weight=-0.4)
        ]
        for item3 in ArrHideNeron:
            TmpNeuron3.addDendriteOrHideNeuron(item3)
        TmpLayer.addNeuronInLayer(TmpNeuron3)
        ######################

        ######################
        хорошая_погода = 0
        дождь = 1
        усаталось = 0
        позвали_гулять = 1
        Signal = [
            хорошая_погода,
            дождь,
            усаталось,
            позвали_гулять,
        ]
        print(TmpLayer.CalculateSignal(Signal))
        ######################
        self.assertEqual(TmpLayer.CalculateSignal(Signal), 0)


if __name__ == '__main__':
    unittest.main()

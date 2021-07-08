from typing import Union, List

from structure_neuron import Dendrite, Neuron, HediNeron


class LayerNeuron:
    def __init__(self):
        self.Layer: List[List[Neuron]] = [[]]
        self.CountLayer: int = 0

    def addNeuronInLayer(self, neuron: Neuron):
        self.Layer[self.CountLayer].append(neuron)

    def NewLayer(self):
        self.Layer.append([])
        self.CountLayer += 1

    def CalculateSignal(self, signal: List[int]) -> Union[int, float]:

        selectSignal: List[int] = signal.copy()
        for layer in self.Layer:
            tmpSignal: List[int] = []
            for neuron in layer:
                tmpSignal.append(neuron.Extremes(neuron.arrDendrite, selectSignal))
            selectSignal = tmpSignal
        return selectSignal[0]






if __name__ == '__main__':
    # Example1()
    Example2()

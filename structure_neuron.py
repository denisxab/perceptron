from typing import List

from fun_active import FunActive


class Dendrite:
    def __init__(self, weight: float) -> None:
        self.weight = weight


class HediNeron:
    def __init__(self, neuron, weight: float) -> None:
        self.neuron = neuron
        self.weight = weight


class Neuron(FunActive):
    def __init__(self):
        self.arrDendrite: List[Dendrite] = []

    def addDendriteOrHideNeuron(self, dendrite: Union[Dendrite, HediNeron]):
        self.arrDendrite.append(dendrite)

from typing import List

from fun_active import FunActive


#
# class Dendrite:
#     def __init__(self, weight: float) -> None:
#         self.weight = weight
#
#
# class HediNeron:
#     def __init__(self, weight: float,neuron = None) -> None:
#         self.neuron = neuron
#         self.weight = weight


class Neuron(FunActive):
    def __init__(self, arrLastWeight: List = None):
        self.arrLastWeight = arrLastWeight


class TraineeNeuron(FunActive):
    def __init__(self,
                 arrLastWeight: List = None,
                 VInputSignal: float = None,
                 Delta: float = None,
                 FOutputSignal: float = None,
                 ):
        self.arrLastWeight = arrLastWeight
        self.VInputSignal = VInputSignal
        self.Delta = Delta
        self.FOutputSignal = FOutputSignal

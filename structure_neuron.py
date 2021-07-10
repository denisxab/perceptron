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


Tid: int = 0


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
        global Tid
        self.id = str(Tid)
        Tid += 1

    def __repr__(self) -> str:
        return self.id

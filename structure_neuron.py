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
        super().__init__()
        self.arrLastWeight = arrLastWeight

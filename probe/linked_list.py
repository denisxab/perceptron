from typing import Any, Optional


class Node:
    def __init__(self, data: Any, nextNode=None, lastNode=None):
        self.data: Any = data
        self.nextNode = nextNode
        self.lastNode = lastNode


class LinkedList:
    def __init__(self, data: tuple) -> None:
        self.Start: Optional[Node] = None
        self.End: Optional[Node] = None
        self.CountNode: int = 0
        if type(data) == tuple:
            for item in data:
                self.append(item)

    def append(self, data: Any):
        if self.End is None:
            self.End = Node(data, None, None)
            self.Start = self.End
        else:
            self.End.nextNode = Node(data, None, self.End)
            self.End = self.End.nextNode
        self.CountNode += 1

    def pop(self, index: int):
        tmpNode: Optional[Node] = self.__iterObject(index)

        tmpNextNode: Optional[Node] = tmpNode.nextNode
        tmpLastNode: Optional[Node] = tmpNode.lastNode

        if tmpNextNode:
            tmpNextNode.lastNode = tmpLastNode
        tmpLastNode.nextNode = tmpNextNode

        del tmpNode

        self.CountNode -= 1

    def insert(self, index: int, data: Any):

        tmpNode: Optional[Node] = self.__iterObject(index)

        tmpNewNode = Node(data, tmpNode.nextNode, tmpNode)

        tmpNextNode: Optional[Node] = tmpNode.nextNode
        tmpLastNode: Optional[Node] = tmpNode

        tmpNextNode.lastNode = tmpNewNode
        tmpLastNode.nextNode = tmpNewNode

        self.CountNode += 1

    def __iterObject(self, index: int) -> Node:
        if self.CountNode == 0:
            raise IndexError("Список Пустой")

        if index > self.CountNode:
            raise IndexError("Указазанный индекс больше колличества жэлементов")

        tmpNode: Optional[Node] = self.Start
        for _ in range(index):
            tmpNode = tmpNode.nextNode
        return tmpNode

    def __repr__(self):
        res: str = "["
        tmpNode: Optional[Node] = self.Start
        while tmpNode:
            res += f"{str(tmpNode.data)}, "
            tmpNode = tmpNode.nextNode
        res = res[:-2:]
        res += "]"
        return res


if __name__ == '__main__':
    testNode = LinkedList((1, 2, 3, 4, 5))

    print(testNode)
    testNode.pop(4)
    print(testNode)
    testNode.insert(2, 111)
    print(testNode)

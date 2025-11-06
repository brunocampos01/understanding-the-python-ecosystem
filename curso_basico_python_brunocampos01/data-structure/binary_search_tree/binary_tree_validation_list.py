# Global variable
elements = []


class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i = None


def initializeTreeA():
    """"
     2
   /   \
   1    3
   """
    root = Tree()
    root.i = 2

    node1 = Tree()
    node1.i = 1

    node2 = Tree()
    node2.i = 3

    root.left = node1
    root.right = node2

    return root


def initializeTreeB():
    """"
    Is this a binary tree, or a binary search tree?
    B: Is not a BST (7 > 6)
                    6
                    / \
                  4   10
                 / \    \
                1   7    12
    """
    root = Tree()
    root.i = 6
    elements.append(root.i)

    node1 = Tree()
    node1.i = 4
    elements.append(node1.i)

    node2 = Tree()
    node2.i = 10
    elements.append(node2.i)

    node3 = Tree()
    node3.i = 1
    elements.append(node3.i)

    node4 = Tree()
    node4.i = 7
    elements.append(node4.i)

    node5 = Tree()
    node5.i = 12
    elements.append(node5.i)

    root.left = node1
    root.right = node2

    node1.left = node3
    node1.right = node4

    node2.right = node5

    return root


def printTree(node, level):
    print(str(node.i) + "| level " + str(level))
    if node.left is not None:
        printTree(node.left, level + 1)
    if node.right is not None:
        printTree(node.right, level + 1)


def find(node, value, level):
    """
    Function to find in mode recursion.
    (node.left) and (node.right) it´s new Trees objects
    """
    if node is None:
        print("Not found")
        return False
    if value == node.i:
        return print("found = {}, level = {}".format(node.i, level))
    if value < node.i:
        return find(node.left, value, level + 1)
    if value > node.i:
        return find(node.right, value, level + 1)


def validation_tree(node):
    print("\n---validation_tree---")
    stack = [node.right]

    while stack is not None:
        stack.pop(0)
        stack.append(node.left)
        stack.append(node.right)

        for element in stack:
            print(element)

    # stack pop(node auxiliar)
    # node.left push
    # node.right push


def main():
    print("arvore A")
    printTree(initializeTreeA(), 0)
    validation_tree(initializeTreeA())

    print("\narvore B")
    printTree(initializeTreeB(), 0)
    validation_tree(initializeTreeB())


# run
if __name__ == "__main__":
    main()

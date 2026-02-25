MIN = -999
MAX = 999


class Tree:
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

    node1 = Tree()
    node1.i = 4

    node2 = Tree()
    node2.i = 10

    node3 = Tree()
    node3.i = 1

    node4 = Tree()
    node4.i = 7

    node5 = Tree()
    node5.i = 12

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


def validation_tree(node, mini, maxi):
    """
    Function to validate if tree is a valid BST.

    - First, walk the left edge of the tree until reaching a leaf
    - If going left, the max must be the parent node
    - If going right, the min must be the parent node
    """
    if node is None:
        return True

    print("Validation node:", node.i)

    if node.i <= mini:
        print("Tree not valid in node =", node.i)
        return False

    if node.i > maxi:
        print("Tree not valid in node =", node.i)
        return False

    left_valid = validation_tree(node.left, mini, node.i)
    right_valid = validation_tree(node.right, node.i, maxi)

    return left_valid and right_valid


def main():
    print("Tree A")
    printTree(initializeTreeA(), 0)
    result_a = validation_tree(initializeTreeA(), MIN, MAX)
    print(f"Tree A valid: {result_a}")

    print("\nTree B")
    printTree(initializeTreeB(), 0)
    result_b = validation_tree(initializeTreeB(), MIN, MAX)
    print(f"Tree B valid: {result_b}")


if __name__ == "__main__":
    main()

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


def find(node, value, level):
    """
    Recursively find a value in the tree.
    (node.left) and (node.right) are child Tree objects.
    """
    if node is None:
        print("Not found")
        return False
    if value == node.i:
        print("found = {}, level = {}".format(node.i, level))
        return True
    if value < node.i:
        return find(node.left, value, level + 1)
    return find(node.right, value, level + 1)


def validation_tree(node):
    """Validate BST using in-order traversal (should yield sorted order)."""
    print("\n---validation_tree---")
    elements = []
    stack = []
    current = node

    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.left

        current = stack.pop()
        elements.append(current.i)
        current = current.right

    is_valid = all(
        elements[i] < elements[i + 1]
        for i in range(len(elements) - 1)
    )
    print(f"In-order traversal: {elements}")
    print(f"Valid BST: {is_valid}")
    return is_valid


def main():
    print("Tree A")
    printTree(initializeTreeA(), 0)
    validation_tree(initializeTreeA())

    print("\nTree B")
    printTree(initializeTreeB(), 0)
    validation_tree(initializeTreeB())


if __name__ == "__main__":
    main()

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i = None


def initializeTreeA():
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
                     4  10
                    / \  \
                   1  7  12
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


def validation_tree(node):
    """
    Function to validation if tree its valid

    - First, walk tree in edge left until leaf 
    - Stack must have largest element in the background
    """
    print("\n---validation tree with stack---")

    stack = []
    cont = 0
    root = node

    while cont < 1:

        # walk left until leaf
        if root is not None:
            stack.append(root)
            print("push =", root.i)
            root = root.left

        else:
            if (len(stack) > 0):
                root = stack.pop()
                print('pop= ', root.i)
                root = root.right
            else:
                cont = 1


def main():
    print("arvore A")
    validation_tree(initializeTreeA())


    print("\narvore B")
    validation_tree(initializeTreeB())


# run
if __name__ == "__main__":
    main()

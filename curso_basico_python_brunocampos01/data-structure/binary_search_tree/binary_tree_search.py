## Incomplete


def generate_levels (tree, tree_levels):
    """
    Walk the tree in order [root -> left -> right]
    and generate the levels correctly.
    """
    stack = []
    stack_levels = []
    level = 0

    # empty tree
    if tree is None:
        print("null")

    for node in tree:
        stack.append(node)
        print(f"node = [{node}]")
        level = 1
        for element in stack:
            # left
            if node < element:
                level += 1
            # right
            elif node > element:
                level += 1
                break
        stack_levels.append(level)
        print(f"level = {level}")
    
    validate_tree(stack_levels, tree_levels)


def validate_tree(stack_levels, tree_levels):
    """"
    Validate whether the computed levels match the expected levels.
    """
    if stack_levels == tree_levels:
        print(True)
    else:
        print(False)


def main():
    # tests
    tree_0 = ()
    tree_0_levels = ()
    tree_1 = (2, 1, 3)
    tree_1_levels = (1, 2, 3)
    tree_2 = (30, 15, 10, 25, 50)
    tree_2_levels = (1, 2, 3, 3, 2)
    tree_3 = (8, 5, 3, 6, 9, 10, 13) # invalid
    tree_3_levels = (1, 2, 3, 3, 4, 2, 3)

    generate_levels(tree_2, tree_2_levels)


# run
if __name__ == "__main__":
    main()

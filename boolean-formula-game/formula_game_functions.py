from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree


# Add your functions here.
def build_tree(formula):
    ''' (str) -> FormulaTree or None
    Returns a formula tree that represents the given string <formula>. If the
    formula is not valid returns None
    >>> build_tree('(x+y*z)') == None
    True
    >>> build_tree('(a*b)')
    AndTree(Leaf('a'), Leaf('b'))
    >>> build_tree('(((a*b)+c)+-(d*a))')
    OrTree(OrTree(AndTree(Leaf('a'), Leaf('b')), Leaf('c')), \
NotTree(AndTree(Leaf('d'), Leaf('a'))))
    '''
    # Obtains the tree and length of equation using a helper function. Length
    # of the formula at the beginning is 0
    tree, length = build_tree_helper(formula, 0)
    # If there are extra characters, the formula is invalid.
    if length != len(formula):
        tree = None
    return tree


def build_tree_helper(s, length):
    # This string contains all valid leaf formulas
    lower_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    # Base Case 1: Formula doesn't contain anything, so invalid
    if s == '':
        tree = None
    # Base Case 2: Formula is just a leaf and length increases by 1
    elif s[0] in lower_alphabet:
        tree = Leaf(s[0])
        length += 1
    # Recursive Case: If the formula is valid, it now must consist of a NOT
    # tree and/or an AND/OR tree
    else:
        # NOT tree
        if s[0] == '-':
            # First create the tree after the not symbol
            tree, length = build_tree_helper(s[1:], length)
            # Then if the tree exists, apply the not
            if tree is not None:
                tree = NotTree(tree)
            length += 1
        # AND/OR tree
        elif s[0] == '(':
            # First find the formula before the operator
            formula1, length1 = build_tree_helper(s[1:], 0)
            # Then using the length of the first formula, find the operator
            # Need to add 1 because of the parentheses
            operator = s[length1+1]
            # Next find the formula after the operator. Need to add 2 because
            # of the parentheses and the operator
            formula2, length2 = build_tree_helper(s[length1+2:], 0)
            # Now we create the specified AND/OR trees based on what operator
            # we found and if both formulas were valid
            if formula1 is not None and formula2 is not None:
                if operator == '+':
                    tree = OrTree(formula1, formula2)
                elif operator == '*':
                    tree = AndTree(formula1, formula2)
                # If the operator is not AND or OR the formula is invalid
                else:
                    tree = None
            else:
                tree = None
            # First parentheses + lengths of formulas + length of operator +
            # closing parenteheses gives us the total length of the formula
            length = 1+length1+1+length2+1
        # Not a NOT tree or AND/OR tree so invalid
        else:
            tree = None
    return tree, length


def draw_formula_tree(root):
    ''' (FormulaTree) -> str
    Returns a string representation of a formula tree given its root <root>
    >>> draw_formula_tree(build_tree('--(-(a+b)+c)'))
    '- - + c\\n      - + b\\n          a'
    >>> draw_formula_tree(build_tree('--(a+b)'))
    '- - + b\\n      a'
    >>> draw_formula_tree(build_tree('a'))
    'a'
    >>> draw_formula_tree(build_tree(''))
    ''
    '''
    # Height of the root is 0
    return draw_formula_tree_helper(root, 0, False)


def draw_formula_tree_helper(root, height, is_right):
    ''' (FormulaTree, int, bool) -> str
    Returns a string representation of a formula tree given its root <root> and
    it's height <height> and whether it is a right child <is_right>. <height>
    and <is_right> are used for knowing where to use space adjustments
    >>> draw_formula_tree_helper(build_tree('--(-(a+b)+c)'), 0, False)
    '- - + c\\n      - + b\\n          a'
    >>> draw_formula_tree_helper(build_tree('--(a+b)'), 0, False)
    '- - + b\\n      a'
    '''
    output = ""
    # Base Case 1: Root is an empty formula tree
    if root is None:
        output = ""
    # Base Case 2: Root is a leaf, so we've hit the end of the tree
    elif isinstance(root, Leaf):
        # If root is a right child, then we need to adjust the spaces
        if is_right:
            output += "  "*height
        output += root.get_symbol()
    # Recursive Case: Now we know root is either a NOT tree or an AND/OR tree
    else:
        # If root is a NotTree, we need to first adjust if it's a right child.
        # Then we add the not symbol to output and call the function again for
        # it's only child
        if isinstance(root, NotTree):
            if is_right:
                output += "  "*height
            output += (root.get_symbol() + " " +
                       draw_formula_tree_helper(root.get_children()[0],
                                                height+1, False))
        # If root is an AndTree/OrTree, we need to adjust if it's a right child
        # like before. Then we add the and/or symbol to the output and call
        # the function for all the right children, and then the left children
        else:
            if is_right:
                output += "  "*height
            output += (root.get_symbol() + " " +
                       draw_formula_tree_helper(root.get_children()[1],
                                                height+1, False) + '\n' +
                       draw_formula_tree_helper(root.get_children()[0],
                                                height+1, True))
    return output


def evaluate(root, variables, values):
    ''' (FormulaTree, str, str) -> int
    Returns 1 or 0 corresponding to the formula given by the root of the
    formula tree <root, a string of its corresponding variables <variables> and
    values <values>
    REQ: length of <variables> and <values> must be the same
    >>> evaluate(build_tree('(-(a+(a+b))*d)'), 'abd', '011')
    0
    >>> evaluate(build_tree('(x*y)'), 'xy', '11')
    1
    >>> evaluate(build_tree('a'), 'a', '0')
    0
    '''
    # Base Case: Root is a leaf, so we just find the corresponding truth value
    if isinstance(root, Leaf):
        # First we find the needed index in variables, then we search values
        index = variables.find(root.get_symbol())
        output = int(values[index])
    # Recursive Case: Root is a NotTree or AndTree/OrTree
    else:
        # If root is a NotTree we need to find the truth value of the child
        # and then apply the NOT operator to that value
        if isinstance(root, NotTree):
            value_child = int(evaluate(
                root.get_children()[0], variables, values))
            # 1-value acts as the NOT operator
            output = 1 - value_child
        # If root is an AndTree/OrTree we need to find the truth values of the
        # children then apply the corrsponding operator
        else:
            value_left = evaluate(root.get_children()[0], variables, values)
            value_right = evaluate(root.get_children()[1], variables, values)
            if root.get_symbol() == '+':
                # Max acts as the OR operator
                output = max(value_left, value_right)
            else:
                # Min acts as the AND operator
                output = min(value_left, value_right)
    return output


def play2win(root, turns, variables, values):
    ''' (FormulaTree, str, str, str) -> int
    Returns the best next move for the player given the root of a formula tree
    <root>, the turns <turns>, variables <variables>, and a string of the
    existing values played <values>. If there is no best move for the player or
    either 0 or 1 will guaranteed win, the move defaults to 0 for A and 1 for E
    REQ: len(turns) > len(values)
    >>> play2win(build_tree('(a+b)'), 'EE', 'ab', '1')
    1
    >>> play2win(build_tree('((a+b)*-c)'), 'EAE', 'abc', '')
    1
    >>> play2win(build_tree('(-(a+b)+-c)'), 'AAE', 'abc', '')
    0
    >>> play2win(build_tree('-c'), 'A', 'c', '')
    1
    '''
    # Just want the variable that will let us win the game. We won't use
    # the other variable
    output, temp = play2win_helper(root, turns, variables, values)
    return output


def play2win_helper(root, turns, variables, values):
    '''(FormulaTree, str, str, str) -> (int, int)
    Returns the best next move and what this will evaluate to in the long run
    for the player given the root of a formula tree <root>, the turns <turns>,
    variables <variables>, and a string of the existing values played <values>.
    If there is no best move for the player or either 0 or 1 will guaranteed
    win, the move defaults to 0 for A and 1 for E.
    REQ: len(turns) > len(values)
    >>> play2win_helper(build_tree('(a+b)'), 'EE', 'ab', '1')
    (1, 1)
    >>> play2win_helper(build_tree('((a+b)*-c)'), 'EAE', 'abc', '')
    (1, 1)
    >>> play2win_helper(build_tree('(-(a+b)+-c)'), 'AAE', 'abc', '')
    (0, 1)
    >>> play2win_helper(build_tree('-c'), 'A', 'c', '')
    (1, 0)
    '''
    # Base Case: There is only one turn left to take
    if len(turns) - len(values) == 1:
        # First we want to evaluate what happens when we use a 0 or a 1
        evaluated_0 = evaluate(root, variables, values+'0')
        evaluated_1 = evaluate(root, variables, values+'1')
        # Next turn is E
        if turns[len(values)] == 'E':
            # E wins with 1, so we check if playing a 0 or 1 makes E win. Note
            # it is extremely important that we check the evaluation of 1 first
            # because if either 0 or 1 lead to a win we want to default to 1
            if evaluated_1 == 1:
                # Playing a 1 resolves to a 1
                eva = 1
                # E wins by playing 1
                output = 1
            elif evaluated_0 == 1:
                # Playing a 0 resolves to a 1
                eva = 1
                # E wins by playing 0
                output = 0
            # E cannot win by playing either 0 or 1
            else:
                # Playing a 1 resolves to a 0
                eva = 0
                # By default E plays 1
                output = 1
        # Next turn is A
        else:
            # A wins with 0, so we check if 0 or 1 makes A win like before.
            # This time we check the evaluation of 0 first. The rest is the
            # same as before
            if evaluated_0 == 0:
                eva = 0
                output = 0
            elif evaluated_1 == 0:
                eva = 0
                output = 1
            # A cannot win by playing either 1 or 0
            else:
                eva = 1
                # By default A plays 0
                output = 0
    # Recursive Case: More than one turn needs to be played
    else:
        # Next turn is E
        if turns[len(values)] == 'E':
            # Obtain what playing 0 or 1 resolves to. These are <eval_1> and
            # <eval_2>
            temp, eval_0 = play2win_helper(root, turns, variables, values+'0')
            temp, eval_1 = play2win_helper(root, turns, variables, values+'1')
            if eval_1 == 1:
                # Playing a 1 resolves to a 1 if only best moves are played
                eva = 1
                # E wins by playing a 1
                output = 1
            elif eval_0 == 1:
                # Playing a 0 resolves to a 1 if only best moves are played
                eva = 1
                # E wins by playing a 0
                output = 0
            # E cannot win by playing a 1 or 0
            else:
                # If the best moves are played, the formula will always resolve
                # to 0
                eva = 0
                # By default E plays 1
                output = 1
        # Next turn is A
        else:
            # Same as turn E
            temp, eval_0 = play2win_helper(root, turns, variables, values+'0')
            temp, eval_1 = play2win_helper(root, turns, variables, values+'1')
            if eval_0 == 0:
                eva = 0
                output = 0
            elif eval_1 == 0:
                eva = 0
                output = 1
            # A cannot win by playing a 1 or 0
            else:
                eva = 1
                # By default A plays 0
                output = 0
    return output, eva

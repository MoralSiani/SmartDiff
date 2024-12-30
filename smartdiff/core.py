import ast
from typing import List, Union, Optional


def build_ast(code: str, func_name: str) -> Union[ast.Module, bool]:
    """
    Parses the given code into an Abstract Syntax Tree (AST).

    Args:
        code (str): The source code to parse.
        func_name (str): The name of the function (not used in this function but kept for consistency).

    Returns:
        ast.Module: The parsed AST representation of the code.
        bool: Returns False if the code cannot be parsed.
    """
    try:
        # Parse the line of code into an Abstract Syntax Tree (AST)
        return ast.parse(code)
    except SyntaxError:
        # Return False if the line cannot be parsed as Python code
        print("Cannot parse the file")
        return False


def get_functions_from_tree(tree: Optional[ast.AST], lst: List[str]) -> List[str]:
    """
    Extracts function calls from an AST tree.

    Args:
        tree (Optional[ast.AST]): The AST tree to analyze.
        lst (List[str]): A list to store the names of function calls.

    Returns:
        List[str]: A list of function names found in the AST.
    """
    if tree is not None:
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Call):
                # Get the function name
                if isinstance(node.func, ast.Name):
                    # Simple function name
                    function_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    # Attribute function (e.g., math.sqrt)
                    function_name = f"{ast.unparse(node.func)}"
                else:
                    function_name = None
                lst.append(function_name)
            # Recursive call to handle nested function calls
            get_functions_from_tree(node, lst)
    return lst


def get_function_scope_from_source(lines: List[str], func_name: str) -> str:
    """
    Extracts the scope of a function from the source code.

    Args:
        lines (List[str]): The source code as a list of lines.
        func_name (str): The name of the function to extract.

    Returns:
        str: The function's source code as a string.

    Raises:
        ValueError: If the function is not found in the source code.
    """
    function_scope = []
    in_function = False
    base_indent = None

    for line in lines:
        stripped_line = line.strip()

        # Check if this line is the start of the function
        if stripped_line.startswith(f"def {func_name}("):
            in_function = True
            base_indent = len(line) - len(stripped_line)
            function_scope.append(line)
            continue

        # If inside the function, collect lines with appropriate indentation
        if in_function:
            current_indent = len(line) - len(line.lstrip())
            if stripped_line and current_indent <= base_indent:  # Function ends
                break
            function_scope.append(line)
    if function_scope:
        return ''.join(function_scope)
    else:
        raise ValueError(f"Function '{func_name}' not found in the file.")


def is_func_changed(path: str, func_name: str) -> bool:
    """
    Determines if the specified function has changed.

    Args:
        path (str): The path to the Python source file.
        func_name (str): The name of the function to check.

    Returns:
        bool: Returns True if the function has changed.
    """
    with open(path, "r") as file:
        code = file.readlines()
        func_scope = get_function_scope_from_source(code, func_name)
        ast_subtree = build_ast(func_scope, func_name)
        if ast_subtree:
            print(get_functions_from_tree(ast_subtree, []))
    # TODO: Replace with actual logic to compare function changes.
    return True

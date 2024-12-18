import ast


def build_ast(code, func_name):
    try:
        # Parse the line of code into an Abstract Syntax Tree (AST)
        ast_code = ast.parse(code)
        return ast_code
    except SyntaxError:
        # Return False if the line cannot be parsed as Python code
        print('Cannot parse the file')
        return False


def get_functions_from_tree(tree, lst):
    # Walk through the AST nodes to check for function calls
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
            # TODO: Remove, not needed since only calls are interesting and not definitions.
            if isinstance(node, ast.FunctionDef):
                lst.append(node.name)
            get_functions_from_tree(node, lst)
    return lst


def get_function_scope_from_source(lines, func_name):
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


def main(path, func_name):
    with open(path, "r") as file:
        code = file.readlines()
        func_scope = get_function_scope_from_source(code, func_name)
        ast_subtree = build_ast(func_scope, func_name)
        print(get_functions_from_tree(ast_subtree, []))


if __name__ == '__main__':
    main("example.py", "foo2")


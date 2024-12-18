# SmartDiff

SmartDiff is a Python module designed to efficiently manage the execution of functions in codebases with complex dependency trees. It helps determine whether a function needs to be re-executed by checking if its dependencies have changed since the last run. This is particularly useful for projects where certain functions are computationally expensive to execute.

## Features

- **Dependency Scanning**: Automatically identifies the dependency tree of any function.
- **Change Detection**: Tracks changes in dependencies to determine whether a function requires re-execution.
- **Efficiency**: Saves computation time by running only the functions that need to be updated.
- **Seamless Integration**: Easy to integrate into existing Python projects.

## Installation

You can install SmartDiff via pip:

```bash
#TODO ADD PYPY
pip install smartdiff
```

## Usage

Here is a basic example of how to use SmartDiff:

```python
#TODO ADD EXAMPLE
```

## How It Works

1. **Dependency Tracking**: SmartDiff inspects the inputs and internal variables of a function to build its dependency tree.
2. **Change Detection**: Using lightweight hashing and caching mechanisms, it detects changes in the dependency tree.
3. **Selective Execution**: Only functions with modified dependencies are flagged for re-execution.

## Use Cases

- Data pipelines where steps depend on each other.
- Scientific computations with long-running processes.
- Machine learning workflows to avoid redundant model training.

## Contributing

Contributions are welcome! If you have ideas or find issues, please feel free to submit a pull request or create an issue in the GitHub repository.

## License

SmartDiff is licensed under the MIT License. See [LICENSE](./LICENSE) for more details.

## Acknowledgments

Thanks to all contributors and users who inspire the development of this project.

## Contact

For questions or feedback, please open an issue on GitHub or contact the maintainer directly.

import subprocess
from pathlib import Path
import tempfile
import shutil

# File paths
REQUIREMENTS_PATH = Path("requirements.txt")
VERSION = "0.1rc0"


# Install required packages
def ensure_dependencies_installed():
    try:
        import toml
        import build
    except ImportError:
        print("Required packages not found. Installing 'toml' and 'build'...")
        subprocess.run(["pip", "install", "toml", "build"], check=True)
        print("Dependencies installed successfully.")


# Helper function to read dependencies from requirements.txt
def read_requirements():
    if REQUIREMENTS_PATH.exists():
        with open(REQUIREMENTS_PATH, "r") as req_file:
            return [line.strip() for line in req_file if line.strip() and not line.startswith("#")]
    return []


# Function to build the project using a temporary pyproject.toml
def build_project(dependencies):
    # Create a temporary directory for the build
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Generate pyproject.toml content
        pyproject_content = {
            "build-system": {
                "requires": ["setuptools>=61.0", "wheel"],
                "build-backend": "setuptools.build_meta"
            },
            "project": {
                "name": "SmartDiff",
                "version": VERSION,
                "description": "A Python module for dependency-aware function execution tracking.",
                "readme": "README.md",
                "license": {"file": "LICENSE"},
                "authors": [{"name": "Your Name", "email": "your.email@example.com"}],
                "classifiers": [
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent"
                ],
                "keywords": ["dependencies", "optimization", "performance"],
                "dependencies": dependencies
            },
            "tool.setuptools.packages.find": {"where": ["smartdiff"]}
        }

        # Write the pyproject.toml in the temporary directory
        import toml
        pyproject_path = temp_path / "pyproject.toml"
        with open(pyproject_path, "w") as pyproject_file:
            toml.dump(pyproject_content, pyproject_file)

        # Copy project files into the temporary directory
        for item in Path(".").iterdir():
            if item.name not in ["dist", "__pycache__"]:
                dest = temp_path / item.name
                if item.is_dir():
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)

        # Run the build command in the temporary directory
        try:
            print("Building the project...")
            subprocess.run(["python", "-m", "build"], cwd=temp_path, check=True)

            # Copy the built distribution back to the original directory
            dist_path = temp_path / "dist"
            if dist_path.exists():
                shutil.copytree(dist_path, Path("dist"), dirs_exist_ok=True)
            print("Build completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during build: {e}")


# Main function
def main():
    ensure_dependencies_installed()
    dependencies = read_requirements()
    build_project(dependencies)


if __name__ == "__main__":
    main()

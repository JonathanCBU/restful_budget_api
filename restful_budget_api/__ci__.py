import argparse
import os

import toml


def main() -> None:
    """check version in toml and branch match and bubble variables up to github
    actions
    """
    args = get_args()
    with open(args.pyproject, "r", encoding="utf-8") as toml_file:
        pyproject = toml.load(toml_file)
    version_num = pyproject["tool"]["poetry"]["version"]
    assert f"v{version_num}" == args.tag.split("/")[1]
    print(version_num)


def get_args() -> argparse.Namespace:
    """get abspath to toml and branch name from stdin"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pyproject",
        required=True,
        help="absolute path to pyproject.toml file",
    )
    parser.add_argument("--tag", required=True, help="git branch name")

    args = parser.parse_args()

    # error check
    if not os.path.exists(args.pyproject):
        raise ValueError(f"could not find pyproject.toml at {args.pyproject}")

    return args

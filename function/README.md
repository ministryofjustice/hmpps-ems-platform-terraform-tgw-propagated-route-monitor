# Function

Function dependencies are managed with [Poetry](https://python-poetry.org/docs/). The [terraform-aws-lambda](https://github.com/terraform-aws-modules/terraform-aws-lambda) moddule is able to build a lambda package using the information stored within `pyproject.toml` file.

All of the below steps assume your working directy is `function`.

## Install dependencies

Development dependencies (e.g pytest, black, isort) are managed in the `dev` group.

```shell
poetry install --with dev
```

## Running tests

```shell
poetry run pytest
```

## Linting

This project uses black and isort to ensure a consistent styling in the python files.

```shell
poetry run black .
poetry run isort .
```

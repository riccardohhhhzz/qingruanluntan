# TODO: add autopep8 here.
autopep8 --recursive --in-place --aggressive --exclude venv,.git,__pycache__ .

# TODO: add autoflake here.
autoflake --recursive --in-place --exclude venv,.git,__pycache__ .

# TODO: add isort here.
isort .

# TODO: add flake8 here.
flake8 .

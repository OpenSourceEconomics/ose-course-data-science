import subprocess as sp

extensions = [
    "@ijmbarr/jupyterlab_spellchecker",
    "@jupyterlab/toc",
    "jupyterlab-flake8",
]


for extension in extensions:
    sp.check_call(f"jupyter labextension install {extension}", shell=True)

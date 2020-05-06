import subprocess as sp

extensions = ["@ijmbarr/jupyterlab_spellchecker", "@jupyterlab/toc"]


for extension in extensions:
    sp.check_call(f"jupyter labextension install {extension}", shell=True)

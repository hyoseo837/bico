import cx_Freeze

executables = [cx_Freeze.Executable("bico.py")]

cx_Freeze.setup(
    name = "bico",
    options = {"build_exe": {"packages":["pygame"], "include_files":["image"]}},
    
    executables = executables

    )
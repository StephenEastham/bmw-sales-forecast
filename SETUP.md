Windows PowerShell Setup (non-venv)
=================================

These commands install project dependencies into the system Python (no virtual environment).
Run PowerShell as an Administrator if you need system-wide installs; otherwise add `--user` to install to your user site-packages.

1) Confirm Python executable (use the project's Python if needed):

```powershell
"C:/Program Files/Python312/python.exe" --version
```

2) Upgrade pip (optional but recommended):

```powershell
"C:/Program Files/Python312/python.exe" -m pip install --upgrade pip
```

3) Install the pinned requirements into system Python:

```powershell
"C:/Program Files/Python312/python.exe" -m pip install -r requirements.txt
```

If you do not have admin privileges, install to your user site-packages:

```powershell
"C:/Program Files/Python312/python.exe" -m pip install --user -r requirements.txt
```

4) Run the project (example):

```powershell
"C:/Program Files/Python312/python.exe" .\main.py
```

Notes:
- Installing system-wide may affect other Python projects on the machine. Consider using a venv or Conda for isolation.
- If you later decide to switch to a virtual environment, recreate the environment and install the same `requirements.txt` inside it.

# Depth camera manager

This repo is in charge of pulling depth data from a Azure Kinect DK camera, turning it into a gray-scale normalized image and then feed it to child processes, using shared memory.

## Development setup

The Azure SDK is already included in the repo. You will need to download:

- Python 3
- You might need to download some additional build tools, more in the setup steps below

Clone the repo, open a terminal window in the root of the repo then run:

1. (Optional but highly suggested) - `python3 -m venv venv` to create a virtual environment, then to activate it:

- `source venv/bin/activate` for OSX users
- `venv/bin/activate.bat` for Windows CMD users
- `venv/bin/Activate.ps1` for Windows PowerShell users

2. `pip install -r requirements.txt` to install dependencies. You might get an error, saying you need additional build tools. If so, follow the instructions from [this thread's top answer](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst).

3. Run python test.py
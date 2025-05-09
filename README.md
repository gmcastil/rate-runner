# Rate Runner
[![Ubuntu](https://github.com/gmcastil/rate-runner/actions/workflows/test-ubuntu.yml/badge.svg)](https://github.com/gmcastil/rate-runner/actions/workflows/test-ubuntu.yml)
[![Windows](https://github.com/gmcastil/rate-runner/actions/workflows/test-windows.yml/badge.svg)](https://github.com/gmcastil/rate-runner/actions/workflows/test-windows.yml)
[![macOS](https://github.com/gmcastil/rate-runner/actions/workflows/test-macos.yml/badge.svg)](https://github.com/gmcastil/rate-runner/actions/workflows/test-macos.yml)
[![Package](https://github.com/gmcastil/rate-runner/actions/workflows/package-ci.yml/badge.svg)](https://github.com/gmcastil/rate-runner/actions/workflows/package-ci.yml)

Tools for performing bulk SEE rate calculations using CREME96

# Workflow
Clone the repository
```bash
git clone git@github.com:gmcastil/rate-runner.git
```
Then, from the repository, create the virtual environment used for development
(this only needs to be done once after cloning the repository or if you have
deleted the `venv` directory).
```bash
make venv
```
This creates the `venv` directory, installs dependancies from
`requirements.txt` and sets up the environment.  From that point on, any new
shell that is being used for development should source the `venv/bin/activate`
script. This will cause `python3` and `pip` to point to those installed in
`.venv` rather than whatever the system happens to be using.

# Tests
To run the test suite, just run
```bash
make test
```


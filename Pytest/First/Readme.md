conventions to fallow for creating test script:
1. Filename must start with prefix "test"
2. testing function must also start with prefix "test"
3. command to run tests "pytest -v"
4. To generate coverage report we can make use pytest-cov
 steps: pip install pytest-cov
 run file with fallowing command, coverage run -m pytest
 to display coverage report coverage report -m
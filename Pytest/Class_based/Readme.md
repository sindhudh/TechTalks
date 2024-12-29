1. run the file with testcase name prefixed with some name "py.test -k Prefixname -v"
2. To mark the testcases we need to impost pytest and mark it with decorator @pytest.mark."markername"
2. run the file with testcases marked with some name "py.test -m "markername" -v"
3. You can group the testcases as class is shown in the code
4. Test Class Naming: It's a good practice to name the class starting with Test (e.g., TestCases) so that pytest identifies it as a test case container.
5. When we want to resue some of the attributes in some of the testcases we can define it as fixtures by wrapping it under pytest.fixtures decorator
6. for testing it is not proper to hardcode values, If you want to run testcases with parameters we need to wrape it around parametrize decorator as shown in parameterized.py file
7. If we want to skip any of the test cases using @pytest.mark.skip and skipif if we want add some condition for skipping the test cases.
8. 

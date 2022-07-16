<h2>0x03-Unittests_and_integration_tests</h2>
<p>Unit testing is the process of testing that a particular function returns expected results for different set of inputs. A unit test is supposed to test standard inputs and corner cases. A unit test should only test the logic defined inside the tested function. Most calls to additional functions should be mocked, especially if they make network or database calls.

<p>The goal of a unit test is to answer the question: if everything defined outside this function works as expected, does this function work as expected?

<p>Integration tests aim to test a code path end-to-end. In general, only low level functions that make external calls such as HTTP requests, file I/O, database I/O, etc. are mocked.

<p>Integration tests will test interactions between every part of your code.

<h3>Execute your tests with</h3>

python -m unittest path/to/test_file.py

<h3><b>Resources</b>
Read or watch:

<li>unittest — Unit testing framework
<li>unittest.mock — mock object library
<li>How to mock a readonly property with mock?
<li>parameterized
<li>Memoization
<h2>Learning Objectives
<p>At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

<li>The difference between unit and integration tests.
<li>Common testing patterns such as mocking, parametrizations and fixtures
<h2>Requirements</h2>
<li>All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
<li>All your files should end with a new line
<li>The first line of all your files should be exactly #!/usr/bin/env python3
<li>A README.md file, at the root of the folder of the project, is mandatory
<li>Your code should use the pycodestyle style (version 2.5)
<li>All your files must be executable
<li>All your modules should have a documentation (python3 -c 'print(__import__("my_module").__doc__)')
<li>All your classes should have a documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)')
<li>All your functions (inside and outside a class) should have a documentation (python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')
<li>A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
<li>All your functions and coroutines must be type-annotated.
Required Files
utils.py (or download)
Click to show/hide file contents
client.py (or download)
Click to show/hide file contents
fixtures.py (or download)
Click to show/hide file contents
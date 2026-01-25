## Personal Message 1:

./week02 Lab phase one:

You are a senior Python developer helping me debug code. I have a function called sum_of_evens that is supposed to calculate the sum of all even numbers in a list, but it's currently returning incorrect results.

Here's the buggy code:

python
def sum_of_evens(numbers):
    """Calculate the sum of all even numbers in a list.

    Parameters
    ----------
    numbers : list of int
        A list of integers.

    Returns
    -------
    int
        The sum of all even numbers in the list.
    """
    total = 0
    for num in numbers:
        if num % 2 == 1:  # This line has a bug!
            total += num
    return total


For example, when I call sum_of_evens([2, 4, 5]), I expect 6 (since 2 + 4 = 6), but the function is giving me the wrong result.

Can you identify the logical error in the conditional statement and provide the corrected version in a Python code block? Please also explain what the bug was and why the fix works.

## Message 1 response:

The bug is that the conditional checks for odd numbers (num % 2 == 1), so it sums the wrong values. Even numbers have a remainder of 0 when divided by 2, so the condition should be num % 2 == 0.

def sum_of_evens(numbers):
    """Calculate the sum of all even numbers in a list.

    Parameters
    ----------
    numbers : list of int
        A list of integers.

    Returns
    -------
    int
        The sum of all even numbers in the list.
    """
    total = 0
    for num in numbers:
        if num % 2 == 0:  # Check for even numbers
            total += num
    return total
This fix works because only numbers divisible by 2 (remainder 0) are included in the sum, so sum_of_evens([2, 4, 5]) correctly returns 6.

## Personal Message 2:

./week02 Lab phase two:

Refactoring the get_names_of_adults function**

You are an expert Python developer who specializes in writing clean, Pythonic code. I have a function that works correctly but is written in an unreadable, non-Pythonic way.

Here's the current code:

def get_names_of_adults(users):
    """Given a list of user dictionaries, returns a list of names of users
    who are 18 or older.

    Parameters
    ----------
    users : list of dict
        List of user dictionaries with 'name' and 'age' keys.

    Returns
    -------
    list of str
        Names of users who are 18 or older.
    """
    results = []
    for i in range(len(users)):
        if users[i]['age'] >= 18:
            results.append(users[i]['name'])
    return results

Please refactor this function to be more clear, concise, and idiomatic Python. Consider improvements like list comprehensions, better iteration patterns, and more Pythonic approaches. Provide the refactored code in a Python code block and explain what makes the new version better.

## Message 2 response:

diff --git a/x:\work\university-of-cincinnati\spring-25\is4010-course\week02/lab02.py b/x:\work\university-of-cincinnati\spring-25\is4010-course\week02/lab02.py
@@ -18 +18,18 @@
     return total
+
+
+def get_names_of_adults(users):
+    """Given a list of user dictionaries, returns a list of names of users
+    who are 18 or older.
+
+    Parameters
+    ----------
+    users : list of dict
+        List of user dictionaries with 'name' and 'age' keys.
+
+    Returns
+    -------
+    list of str
+        Names of users who are 18 or older.
+    """
+    return [user["name"] for user in users if user["age"] >= 18]

Added a Pythonic refactor of get_names_of_adults using a list comprehension in lab02.py, which reads clearer and avoids index-based looping.

## Personal Message 3:

./week02 Lab phase three:

Documenting the calculate_area function**
You are a professional Python developer with expertise in writing documentation. I have a function that works correctly but has no documentation, and I need a professional NumPy-style docstring for it.

Here's the undocumented code:
def calculate_area(length, width):
    if length <= 0 or width <= 0:
        raise ValueError("Length and width must be positive numbers.")
    return length * width

Please write a comprehensive NumPy-style docstring for this function. The docstring should include:

A brief description of what the function does
A Parameters section describing both inputs
A Returns section describing the output
A Raises section mentioning the ValueError for invalid inputs
An Examples section with at least two usage examples
Provide the complete function with the docstring in a Python code block.

## Message 3 response:

diff --git a/x:\work\university-of-cincinnati\spring-25\is4010-course\week02/lab02.py b/x:\work\university-of-cincinnati\spring-25\is4010-course\week02/lab02.py
@@ -35 +35,33 @@
     return [user["name"] for user in users if user["age"] >= 18]
+
+
+def calculate_area(length, width):
+    """Calculate the area of a rectangle.
+
+    Parameters
+    ----------
+    length : float or int
+        The length of the rectangle. Must be a positive number.
+    width : float or int
+        The width of the rectangle. Must be a positive number.
+
+    Returns
+    -------
+    float or int
+        The area of the rectangle computed as ``length * width``.
+
+    Raises
+    ------
+    ValueError
+        If ``length`` or ``width`` is less than or equal to zero.
+
+    Examples
+    --------
+    >>> calculate_area(5, 3)
+    15
+    >>> calculate_area(2.5, 4)
+    10.0
+    """
+    if length <= 0 or width <= 0:
+        raise ValueError("Length and width must be positive numbers.")
+    return length * width

Added a full NumPy-style docstring and the calculate_area function to lab02.py with parameters, returns, raises, and examples.

If you want, I can also paste the same content into week02_prompts.md for the lab submission.
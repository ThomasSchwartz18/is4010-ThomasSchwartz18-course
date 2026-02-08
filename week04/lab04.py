"""Lab 04: Data Structures

This module implements three functions that demonstrate choosing appropriate
Python data structures for different scenarios:
1. Sets for finding common elements efficiently
2. Dictionaries for fast user lookups
3. List comprehensions for filtering while preserving order

Author: IS4010 Student
Course: IS4010 - AI-Enhanced Application Development
Lab: Week 04 - Data Structures
"""


def find_common_elements(list1, list2):
    """Find the common elements between two lists.

    This function takes two lists and returns a new list containing
    only the elements that are present in both input lists. The final
    list can be in any order.

    Uses set intersection for O(1) lookup performance, which is optimal
    for large lists where performance is critical.

    Parameters
    ----------
    list1 : list
        The first list of elements.
    list2 : list
        The second list of elements.

    Returns
    -------
    list
        A list of elements common to both list1 and list2.

    Examples
    --------
    >>> find_common_elements([1, 2, 3, 4, 5], [4, 5, 6, 7, 8])
    [4, 5]
    >>> find_common_elements([1, 2, 3], [4, 5, 6])
    []
    >>> find_common_elements([], [])
    []
    """
    return list(set(list1) & set(list2))


def find_user_by_name(users, name):
    """Find a user's profile by name from a list of user data.

    Converts the user list to a dictionary for O(1) lookup performance,
    which is optimal when lookups are performed frequently.

    Parameters
    ----------
    users : list of dict
        A list of dictionaries, where each dictionary represents a user
        and has 'name', 'age', and 'email' keys. It is recommended to
        convert this list into a more efficient data structure for lookups.
    name : str
        The name of the user to find.

    Returns
    -------
    dict or None
        The dictionary of the found user, or None if no user is found.

    Examples
    --------
    >>> users = [
    ...     {"name": "alice", "age": 30, "email": "alice@example.com"},
    ...     {"name": "bob", "age": 25, "email": "bob@example.com"}
    ... ]
    >>> find_user_by_name(users, "alice")
    {"name": "alice", "age": 30, "email": "alice@example.com"}
    >>> find_user_by_name(users, "charlie")
    None
    >>> find_user_by_name([], "alice")
    None
    """
    user_dict = {user['name']: user for user in users}
    return user_dict.get(name)


def get_list_of_even_numbers(numbers):
    """Return a new list containing only the even numbers from the input list.

    The order of the numbers in the output list must be the same as the
    order of the even numbers in the input list.

    Uses a list comprehension to filter even numbers while preserving
    the original order.

    Parameters
    ----------
    numbers : list of int
        A list of integers.

    Returns
    -------
    list of int
        A new list containing only the even integers from the input list.

    Examples
    --------
    >>> get_list_of_even_numbers([1, 2, 3, 4, 5, 6])
    [2, 4, 6]
    >>> get_list_of_even_numbers([1, 3, 5, 7])
    []
    >>> get_list_of_even_numbers([0, 1, 2, 3])
    [0, 2]
    >>> get_list_of_even_numbers([-4, -3, -2, -1, 0, 1, 2])
    [-4, -2, 0, 2]
    """
    return [num for num in numbers if num % 2 == 0]

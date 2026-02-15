# lab05.py
# Week 05: Functions and error handling
# Refactored user data processing with robust error handling

users = [
    {"name": "alice", "age": 30, "is_active": True, "email": "alice@example.com"},
    {"name": "bob", "age": 25, "is_active": False},
    {"name": "charlie", "age": 35, "is_active": True, "email": "charlie@example.com"},
    {"name": "david", "age": "unknown", "is_active": False}
]


def calculate_average_age(users):
    """
    Calculate the average age of users with valid integer ages.

    This function processes a list of user dictionaries, extracting only
    valid integer age values and computing their average. Users with missing,
    invalid, or non-integer ages are safely excluded from the calculation.

    Parameters
    ----------
    users : list of dict
        A list of user dictionaries. Each dictionary may contain an 'age' key
        with an integer value. Users with missing or non-integer ages are skipped.

    Returns
    -------
    float
        The average age of users with valid integer ages.
        Returns 0.0 if the list is empty or no users have valid ages.

    Examples
    --------
    >>> users = [{"name": "alice", "age": 30}, {"name": "bob", "age": 25}]
    >>> calculate_average_age(users)
    27.5

    >>> calculate_average_age([])
    0.0

    Notes
    -----
    - Uses isinstance() to verify age is an integer type
    - Handles ZeroDivisionError when no valid ages exist
    - Uses .get() method for safe dictionary access
    """
    # Handle empty list edge case
    if not users:
        return 0.0

    total_age = 0
    user_count_for_age = 0

    # Iterate through users and sum valid ages
    for user in users:
        # Only include users with valid integer ages
        if isinstance(user.get("age"), int):
            total_age += user["age"]
            user_count_for_age += 1

    # Calculate average with error handling
    try:
        average_age = total_age / user_count_for_age
        return average_age
    except ZeroDivisionError:
        print("error: cannot calculate average age of an empty list.")
        return 0.0


def get_active_user_emails(users):
    """
    Extract email addresses from all active users.

    This function filters a list of user dictionaries to find users who are
    marked as active and have an email address, then returns their emails.

    Parameters
    ----------
    users : list of dict
        A list of user dictionaries. Each dictionary may contain 'is_active'
        (bool) and 'email' (str) keys. Users must have both to be included.

    Returns
    -------
    list of str
        A list of email addresses from active users who have email addresses.
        Returns an empty list if no active users with emails exist.

    Examples
    --------
    >>> users = [
    ...     {"name": "alice", "is_active": True, "email": "alice@example.com"},
    ...     {"name": "bob", "is_active": False, "email": "bob@example.com"}
    ... ]
    >>> get_active_user_emails(users)
    ['alice@example.com']

    >>> get_active_user_emails([])
    []

    Notes
    -----
    - Uses .get() method to safely access potentially missing keys
    - Requires BOTH is_active=True AND email to exist
    - Handles missing keys gracefully without raising KeyError
    """
    # Handle empty list edge case
    if not users:
        return []

    active_user_emails = []

    # Iterate through users and collect emails from active users
    for user in users:
        # Check both conditions: is_active and email exists
        if user.get("is_active") and user.get("email"):
            active_user_emails.append(user["email"])

    return active_user_emails


if __name__ == '__main__':
    # Call functions and print results
    avg_age = calculate_average_age(users)
    print(f"average user age: {avg_age:.2f}")

    active_emails = get_active_user_emails(users)
    print(f"active user emails: {active_emails}")

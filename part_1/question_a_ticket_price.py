"""Part 1, Question A: calculate a passenger's ticket price.

Approach:
1. Check the discounts from largest to smallest: free, 50%, then 20%.
2. Use if/elif so only one discount applies, even to a senior student.
3. Convert the result to float and round to one decimal place.

Inputs: a positive base price, a positive integer age, and a student flag.
Output: the discounted price as a float, rounded to one decimal place.
Example: calculate_ticket_price(50, 70, True) returns 25.0, not 20.0.
The function does not change any input.
"""


def calculate_ticket_price(base_price, passenger_age, is_student):
    """Return the ticket price after the single largest eligible discount."""
    if passenger_age < 5:
        # Children younger than five travel free.
        price = 0.0
    elif passenger_age <= 17 or passenger_age >= 65:
        # This branch also handles senior students before the student branch.
        price = base_price * 0.5
    elif passenger_age >= 18 and is_student:
        price = base_price * 0.8
    else:
        price = base_price

    # float keeps the output type correct even if the caller supplies 50.
    return round(float(price), 1)
"""Static, versioned Loops learning material for the pilot.

Content mirrors research/loops_learning_module_v0.2.md sections 4-7.
Both experimental conditions receive identical material; only AI
availability differs during the SUPPORTED phase.
"""

LOOPS_MODULE = {
    "module_id": "loops",
    "version": "v0.2.0",
    "explanation": (
        "A loop repeats an operation for each item in a sequence.\n\n"
        "Example:\n"
        "    numbers = [10, 20, 30]\n"
        "    for number in numbers:\n"
        "        print(number)\n\n"
        "The loop takes each value from `numbers` one at a time and executes "
        "the indented block.\n\n"
        "### Conditional iteration\n"
        "    numbers = [10, 25, 40, 15]\n"
        "    for number in numbers:\n"
        "        if number > 20:\n"
        "            print(number)\n\n"
        "The reasoning pattern is:\n"
        "1. inspect each item;\n"
        "2. test the condition;\n"
        "3. perform the required action when the condition is true.\n\n"
        "### Counting\n"
        "    numbers = [10, 25, 40, 15]\n"
        "    count = 0\n"
        "    for number in numbers:\n"
        "        if number > 20:\n"
        "            count += 1\n\n"
        "After the loop, `count == 2`."
    ),
    "worked_example": {
        "problem": "Count how many values are strictly greater than 20.",
        "input": "numbers = [10, 25, 40, 15]",
        "reasoning": (
            "1. initialize a counter;\n"
            "2. inspect each value;\n"
            "3. test whether it is greater than 20;\n"
            "4. increment the counter for qualifying values."
        ),
        "solution": (
            "result = 0\n"
            "for number in numbers:\n"
            "    if number > 20:\n"
            "        result += 1"
        ),
        "expected_result": "2",
    },
    "guided_practice": {
        "problem": "Given `stock_levels = [3, 8, 2, 6, 1]`, count how many stock levels are strictly less than 5.",
        "expected_result": 3,
        "note": "This is practice/familiarization and is not a primary outcome.",
    },
    "static_hints": [
        "Think about what value should keep track of the result while the loop runs.",
        "For each item, check whether it satisfies the required condition.",
        "When the condition is true, update the result.",
    ],
}
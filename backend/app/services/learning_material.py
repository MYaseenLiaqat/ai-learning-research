"""Static, versioned Loops learning material for the pilot.

This revision keeps the construct narrow: basic conditional iteration with a
for-loop. Old v0.2.0 material remains available for frozen participants.
"""

LEGACY_LOOPS_MODULE_V020 = {
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

LEGACY_LOOPS_MODULE_V030 = {
    "module_id": "loops",
    "version": "v0.3.0",
    "explanation": (
        "Learning objective: use a basic Python `for` loop to initialize a result, "
        "iterate through a sequence one item at a time, check a condition, update the result, "
        "and read the final value after the loop ends.\n\n"
        "Prerequisite reminder: variables, lists, comparisons, `if`, and indentation. "
        "You do not need a full Python course to complete this module.\n\n"
        "A `for` loop takes one item from a sequence at a time and runs the indented loop body "
        "once for each item.\n\n"
        "Example:\n"
        "    numbers = [4, 7, 2]\n"
        "    for value in numbers:\n"
        "        print(value)\n\n"
        "The current `value` changes each time the loop runs.\n\n"
        "Trace example:\n"
        "    numbers = [4, 7, 2]\n"
        "    result = 0\n"
        "    for value in numbers:\n"
        "        if value > 3:\n"
        "            result += 1\n"
        "\n"
        "iteration | value | condition | result\n"
        "1         | 4     | True      | 1\n"
        "2         | 7     | True      | 2\n"
        "3         | 2     | False     | 2\n\n"
        "Five-step reasoning framework:\n"
        "1. INITIALIZE — create the result before the loop\n"
        "2. ITERATE — process each item one at a time\n"
        "3. CHECK — test the current item against a condition\n"
        "4. UPDATE — change the result only when the condition is true\n"
        "5. RESULT — read the final value after the loop ends\n\n"
        "### Counting\n"
        "    numbers = [10, 25, 40, 15]\n"
        "    result = 0\n"
        "    for number in numbers:\n"
        "        if number > 20:\n"
        "            result += 1\n\n"
        "Here, `result = 0` is outside the loop because we want one running total. "
        "`result += 1` happens only when the condition is true.\n\n"
        "### Summing / accumulation\n"
        "    prices = [500, 1200, 800]\n"
        "    total = 0\n"
        "    for price in prices:\n"
        "        if price > 1000:\n"
        "            total += price\n\n"
        "Counting uses `result += 1`. Summation uses `result += value`.\n\n"
        "### Comparison reminder\n"
        "- `>` means strictly greater than\n"
        "- `>=` means greater than or equal to\n"
        "- `<` means strictly less than\n"
        "- `<=` means less than or equal to\n\n"
        "Use the comparison carefully: the word 'strictly' changes the threshold.\n\n"
        "### Indentation matters\n"
        "    numbers = [8, 3, 11]\n"
        "    result = 0\n"
        "    for number in numbers:\n"
        "        if number > 5:\n"
        "            result += 1\n\n"
        "The lines inside the loop and inside the `if` statement must be indented. "
        "Otherwise Python will not run the update at the correct time.\n\n"
        "### Common mistakes\n"
        "- initialize the result inside the loop instead of before it\n"
        "- use wrong indentation\n"
        "- update the result outside the condition instead of only when the condition is true\n"
        "- use the wrong comparison operator\n"
        "- overwrite a value instead of accumulating the total\n"
        "- redefine the platform-provided input variable\n"
    ),
    "worked_example": {
        "problem": "Count how many values are strictly greater than 20.",
        "input": "numbers = [10, 25, 40, 15]",
        "reasoning": (
            "1. initialize the result before the loop;\n"
            "2. inspect each value;\n"
            "3. test whether the value is greater than 20;\n"
            "4. update the result only for qualifying values;\n"
            "5. read the final result after the loop."
        ),
        "solution": (
            "result = 0\n"
            "for number in numbers:\n"
            "    if number > 20:\n"
            "        result += 1\n"
            "print(result)"
        ),
        "expected_result": 2,
    },
    "guided_practice": {
        "problem": (
            "Fill in the missing parts of this code to count how many values in `stock_levels` are "
            "strictly less than 5.\n\n"
            "```python\n"
            "stock_levels = [3, 8, 2, 6, 1]\n"
            "result = ___\n"
            "for value in stock_levels:\n"
            "    if value ___ 5:\n"
            "        result ___ 1\n"
            "```\n\n"
            "What value should the final answer be?"
        ),
        "expected_result": 3,
        "note": "This is scaffolded guided practice to reinforce the pattern. It is not a primary outcome.",
    },
    "mini_practice": {
        "problem": "Use a short list and count how many values are less than 10.",
        "example": "observations = [12, 7, 9, 15, 4]",
        "hint": "Start with result = 0, check each value, and count the ones below 10.",
    },
    "static_hints": [
        "Start by deciding what variable will hold the result before the loop begins.",
        "For each item, check the condition and update the result only when it is true.",
        "Check the final value after the loop ends, not inside the loop body.",
    ],
}

LOOPS_MODULE = {
    "module_id": "loops",
    "version": "v0.4.0",
    "explanation": (
        "# Lesson 1: How a for loop actually runs\n\n"
        "A for loop takes values from a list one at a time. The indented code runs once for each value.\n\n"
        "```python\n"
        "numbers = [10, 20, 30]\n\n"
        "for number in numbers:\n"
        "    print(number)\n"
        "```\n\n"
        "**What is happening?** `for` starts the loop. `number` holds the current value and could have another meaningful name. `numbers` is the list being visited. Python handles moving to the next item automatically.\n\n"
        "**Output**\n\n"
        "```text\n10\n20\n30\n```\n\n"
        "**Dry run**\n\n"
        "| iteration | list position | current value | code executed | output |\n| --- | --- | --- | --- | --- |\n| 1 | 0 | 10 | `print(number)` | 10 |\n| 2 | 1 | 20 | `print(number)` | 20 |\n| 3 | 2 | 30 | `print(number)` | 30 |\n\n"
        "Python starts with 10, stores it in `number`, and runs the indented body. Only after the body finishes does it take 20, then 30. After 30 there is no next item, so the loop stops by itself and Python runs the code after the loop.\n\n"
        "**Quick check**\n\n"
        "When the loop runs for the second time, what value is stored in `number`?\n\n"
        "# Lesson 2: Conditions inside a loop\n\n"
        "An `if` inside a loop lets Python decide what to do with each current value. For each item: get the value, check the condition, run the `if` block when it is True, skip it when it is False, then move to the next value. The loop stops when no values remain.\n\n"
        "```python\n"
        "numbers = [10, 25, 15]\n\n"
        "for number in numbers:\n"
        "    if number > 20:\n"
        "        print(number)\n"
        "```\n\n"
        "**Dry run**\n\n"
        "Iteration 1: `number = 10`; `10 > 20` is False, so Python skips the `if` block. Nothing is printed.\n\n"
        "Iteration 2: `number = 25`; `25 > 20` is True, so Python enters the block and prints 25.\n\n"
        "Iteration 3: `number = 15`; `15 > 20` is False, so Python skips the block. No values remain, so the loop ends.\n\n"
        "| iteration | current value | condition | action | output |\n| --- | --- | --- | --- | --- |\n| 1 | 10 | False | skip print | none |\n| 2 | 25 | True | run print | 25 |\n| 3 | 15 | False | skip print | none |\n\n"
        "**Comparison key**\n\n"
        "`>` means greater than; `>=` means greater than or equal to; `<` means less than; `<=` means less than or equal to.\n\n"
        "**Quick check**\n\n"
        "Which values would be printed, and why?\n\n"
        "# Lesson 3: Building a result\n\n"
        "## Part A: Counting\n\n"
        "We can count how many values match a condition. Before checking anything, the count is zero, so `result = 0` comes before the loop.\n\n"
        "```python\n"
        "numbers = [10, 25, 40, 15]\n\n"
        "result = 0\n\n"
        "for number in numbers:\n"
        "    if number > 20:\n"
        "        result += 1\n"
        "```\n\n"
        "**Why `result += 1`?** It means `result = result + 1`. Each matching value increases the count by one. A value that does not match leaves the count unchanged.\n\n"
        "| value | condition | result after this value |\n| --- | --- | --- |\n| start | - | 0 |\n| 10 | False | 0 |\n| 25 | True | 1 |\n| 40 | True | 2 |\n| 15 | False | 2 |\n\n"
        "Final `result = 2`: two values matched.\n\n"
        "## Part B: Summation\n\n"
        "This time we add the actual matching values. We start from 0 because we are doing addition.\n\n"
        "```python\n"
        "prices = [500, 1200, 800, 1500]\n\n"
        "result = 0\n\n"
        "for price in prices:\n"
        "    if price > 1000:\n"
        "        result += price\n"
        "```\n\n"
        "The dry run is: 500 is False, so result is 0; 1200 is True, so result is `0 + 1200 = 1200`; 800 is False, so it stays 1200; 1500 is True, so it becomes `1200 + 1500 = 2700`.\n\n"
        "**The key difference**\n\n"
        "| counting | summing |\n| --- | --- |\n| `result += 1` | `result += price` |\n| add one because one value matched | add the matching value itself |\n\n"
        "# Practice\n\n"
        "## Guided practice\n\n"
        "Fill in the blanks. Count how many stock levels are strictly less than 5.\n\n"
        "```python\n"
        "stock_levels = [3, 8, 2, 6, 1]\n\n"
        "result = ___\n\n"
        "for value in stock_levels:\n"
        "    if value ___ 5:\n"
        "        result ___ 1\n"
        "```\n\n"
        "What final value should `result` have?\n\n"
        "## Mini-practice\n\n"
        "Without running it, which temperatures are printed, and how many are there?\n\n"
        "```python\n"
        "temperatures = [18, 25, 12, 30]\n\n"
        "for temperature in temperatures:\n"
        "    if temperature >= 20:\n"
        "        print(temperature)\n"
        "```"
    ),
    "worked_example": {
        "problem": "Count how many values are strictly greater than 20.",
        "input": "numbers = [10, 25, 40, 15]",
        "reasoning": "Read Lesson 3 Part A and dry-run each value.",
        "solution": "result = 0\nfor number in numbers:\n    if number > 20:\n        result += 1\nprint(result)",
        "expected_result": 2,
    },
    "guided_practice": {
        "problem": (
            "Fill the blanks to count stock levels strictly less than 5.\n\n"
            "```python\n"
            "stock_levels = [3, 8, 2, 6, 1]\n"
            "result = ___\n"
            "for value in stock_levels:\n"
            "    if value ___ 5:\n"
            "        result ___ 1\n"
            "```\n\n"
            "What final value should `result` have?"
        ),
        "expected_result": 3,
        "note": "This is scaffolded guided practice and is not a primary outcome.",
    },
    "mini_practice": {
        "problem": "Reason through the temperature loop in Lesson 3.",
        "example": "temperatures = [18, 25, 12, 30]",
        "hint": "Check each value against 20 and write the matching outputs in order.",
    },
    "static_hints": [
        "Start with the first list value and write the current variable value.",
        "Check the condition before deciding what the indented code does.",
        "For counting add 1; for summing add the matching value.",
    ],
}

LEGACY_LOOPS_MODULE_V040 = LOOPS_MODULE

LOOPS_MODULE_V050 = {
    "module_id": "loops",
    "version": "v0.5.0",
    "explanation": (
        "# Lesson 1: The iterator and execution order\n\n"
        "A `for` loop takes the next value from a sequence, stores it in the iterator variable, and runs the indented body. When the body finishes, Python takes the next value. The iterator variable is the current item for that iteration; it is replaced on the next iteration. After the last item, the loop ends automatically.\n\n"
        "```python\n"
        "numbers = [10, 20, 30]\n\n"
        "for number in numbers:\n"
        "    print(number)\n"
        "```\n\n"
        "Dry-run table:\n\n"
        "**Dry run**\n\n| iteration | position | current value | body action | output |\n| --- | --- | --- | --- | --- |\n| 1 | 0 | 10 | print 10 | 10 |\n| 2 | 1 | 20 | print 20 | 20 |\n| 3 | 2 | 30 | print 30 | 30 |\n\n"
        "The loop variable holds the current value. It is not a counter.\n\n"
        "# Lesson 2: Conditions and execution tracing\n\n"
        "Trace each iteration in this order: get the current value, evaluate the comparison, run or skip the `if` block, update state if needed, then move to the next value. Indentation determines which statements belong to the loop and condition.\n\n"
        "```python\n"
        "numbers = [10, 25, 15]\n\n"
        "for number in numbers:\n"
        "    if number > 20:\n"
        "        print(number)\n"
        "```\n\n"
        "| iteration | current value | comparison | block | output |\n| --- | --- | --- | --- | --- |\n| 1 | 10 | False | skipped | none |\n| 2 | 25 | True | runs | 25 |\n| 3 | 15 | False | skipped | none |\n\n"
        "Use `>`, `>=`, `<`, and `<=` exactly as the task wording requires.\n\n"
        "# Lesson 3: Counters and accumulators\n\n"
        "First decide what `result` represents and initialize it before the loop. A counter answers how many values qualify, so it starts at 0 and uses `result += 1` for each match. This means `result = result + 1`.\n\n"
        "```python\n"
        "result = 0\n"
        "for number in numbers:\n"
        "    if number > 20:\n"
        "        result += 1\n"
        "```\n\n"
        "| current value | qualifies? | state before | update | state after |\n| --- | --- | ---: | --- | ---: |\n| start | - | 0 | none | 0 |\n| 10 | no | 0 | none | 0 |\n| 25 | yes | 0 | add 1 | 1 |\n| 40 | yes | 1 | add 1 | 2 |\n| 15 | no | 2 | none | 2 |\n\n"
        "An accumulator answers what total the qualifying values make, so it also starts at 0 but uses `result += number` or the task's current value. It adds the value itself, not one.\n\n"
        "| current value | qualifies? | total before | update | total after |\n| --- | --- | ---: | --- | ---: |\n| start | - | 0 | none | 0 |\n| 500 | no | 0 | none | 0 |\n| 1200 | yes | 0 | add 1200 | 1200 |\n| 800 | no | 1200 | none | 1200 |\n| 1500 | yes | 1200 | add 1500 | 2700 |\n\n"
        "Choose a counter when the answer is a number of matches. Choose an accumulator when the answer is a total. In a dry run, record the current value, condition, state before the update, update, and state after the update.\n\n"
        "# Practice\n\n"
        "Use fill-in-the-blank practice and short dry-run tables.\n\n"
        "```python\n"
        "stock_levels = [3, 8, 2, 6, 1]\n"
        "result = ___\n"
        "for value in stock_levels:\n"
        "    if value ___ 5:\n"
        "        result ___ 1\n"
        "```\n\n"
        "These activities are instructional and not primary outcomes."
    ),
    "worked_example": {
        "problem": "Count how many values are strictly greater than 20.",
        "input": "numbers = [10, 25, 40, 15]",
        "reasoning": "Trace each value, condition, and counter update.",
        "solution": "result = 0\nfor number in numbers:\n    if number > 20:\n        result += 1",
        "expected_result": 2,
    },
    "guided_practice": {
        "problem": (
            "Fill the blanks to count values in `stock_levels` strictly less than 5.\n\n"
            "```python\n"
            "stock_levels = [3, 8, 2, 6, 1]\n"
            "result = ___\n"
            "for value in stock_levels:\n"
            "    if value ___ 5:\n"
            "        result ___ 1\n"
            "```"
        ),
        "expected_result": 3,
        "note": "Instructional practice, not a primary outcome.",
    },
    "mini_practice": {
        "problem": "Dry-run a loop and identify whether its state is a counter or accumulator.",
        "example": "observations = [12, 7, 9, 15, 4]",
        "hint": "Write the current value, condition, and state after every iteration.",
    },
    "static_hints": [
        "Name what result should represent before the loop.",
        "Trace the current value and condition for each iteration.",
        "Add one for a count; add the current value for a total.",
    ],
}

LEGACY_LOOPS_MODULE_V050 = LOOPS_MODULE_V050

LOOPS_MODULE_V060 = {
    "module_id": "loops",
    "version": "v0.6.0",
    "explanation": (
        "# Lesson 1: Iterator variables and tracing\n\n"
        "A `for` loop assigns one item at a time to an iterator variable. The iterator is the current item, not automatically a counter. Trace each iteration by recording the current item, condition, state before the update, action, and state after the update.\n\n"
        "```python\n"
        "signals = [\"yes\", \"no\", \"yes\"]\n"
        "for signal in signals:\n"
        "    print(signal)\n"
        "```\n\n"
        "# Lesson 2: Decompose the problem\n\n"
        "Before writing code, ask: what does the result represent, what state is needed before iteration, what is the current item, what condition decides the action, which state variables change, and what remains after the loop? Use the framework `UNDERSTAND -> DECOMPOSE -> INITIALIZE -> ITERATE -> CHECK -> UPDATE -> RESULT`.\n\n"
        "# Lesson 3: Common state patterns\n\n"
        "A counter answers how many items qualify. Initialize it to 0 and add 1 for each match. An accumulator answers a total. Initialize it to 0 and add the qualifying value. A maximum tracks the largest value seen so far: compare the current item with the stored maximum and replace the stored maximum when the current item is larger.\n\n"
        "For a longest streak, use multiple state variables. A current-streak variable tracks the run being processed; a best-streak variable tracks the longest run so far. With `if/else`, increase the current streak for a qualifying string and reset it otherwise, then update the best streak when needed.\n\n"
        "| current item | condition | current state | best state |\n| --- | --- | --- | --- |\n| start | - | 0 | 0 |\n| yes | true | 1 | 1 |\n| yes | true | 2 | 2 |\n| no | false | 0 | 2 |\n\n"
        "# Lesson 4: Solve unseen problems\n\n"
        "Use a dry-run table before coding. Name every state variable, initialize it, process one iterator value at a time, apply the comparison or `if/else`, update only the relevant state, and read the final result after the loop. Practice should change contexts and values so learners apply patterns instead of memorizing code."
    ),
    "worked_example": {
        "problem": "Trace a loop that identifies the largest value seen so far.",
        "input": "values = [4, 9, 2]",
        "reasoning": "Identify the maximum state, compare each current value, and update when the current value is larger.",
        "solution": "result = values[0]\nfor value in values:\n    if value > result:\n        result = value",
        "expected_result": 9,
    },
    "guided_practice": {
        "problem": (
            "Identify the state variables and fill the blanks for a longest `yes` streak.\n\n"
            "```python\n"
            "activity = [\"yes\", \"no\", \"yes\", \"yes\"]\n"
            "current = ___\n"
            "best = ___\n"
            "for item in activity:\n"
            "    if item == \"yes\":\n"
            "        current ___ 1\n"
            "    else:\n"
            "        current = ___\n"
            "```"
        ),
        "expected_result": 2,
        "note": "Instructional practice, not a primary outcome.",
    },
    "mini_practice": {
        "problem": "Choose whether an unseen problem needs a counter, accumulator, maximum, or multiple states.",
        "example": "labels = [\"yes\", \"yes\", \"no\"]",
        "hint": "State what the final result represents before choosing variables.",
    },
    "static_hints": [
        "State the result in words before writing code.",
        "List every state variable and its initialization.",
        "Dry-run one item at a time and update only the state required by the pattern.",
    ],
}

MODULE_REGISTRY = {
    "v0.2.0": LEGACY_LOOPS_MODULE_V020,
    "v0.3.0": LEGACY_LOOPS_MODULE_V030,
    "v0.4.0": LEGACY_LOOPS_MODULE_V040,
    "v0.5.0": LOOPS_MODULE_V050,
    "v0.6.0": LOOPS_MODULE_V060,
}


def get_learning_module(version: str):
    module = MODULE_REGISTRY.get(version)
    if module is None:
        raise KeyError(f"Unknown learning module version: {version}")
    return module
"""
Lecture 1

Reading JSON files

import json

with open(file_path) as file:

    nobel = json.load(file)

A list where each element has an id and a label

Unique identifiers

Maybe want to find all Swedish Nobel prize winners or women or something else

csv comma seperated files like excel uses this format

TSV tab seperated files is similar

A list of lists essentially

rows = csv.reader(infile, delimiter=',')

list comprehension

Let's say we want to collect all even numbers below 100 into a list

even_numbers = [x for x in range(0, 101, 2)]

print(even_numbers)

or similar

even_numbers = [x for x in range(101) if x%2 == 0]

set comprehension

remainders = {x: x%7 for x in range(101) if x%2 == 0}

Difference?

In a set every element can only appear once

For dictionaries we use need to return key value pair

{x: x for x in range(101)}

Tuple comprehension

tuple(x % 3 for x in range(20) if x%2 == 0)

Example of list item showing structure

alice_munro = {
    "person": "link",
    "personLabel": "Alice Munro",
    "sexLabel": "female"
}

categories = {n['awardLabel'] for n in nobel}

winners_by_category = {c: [n for n in nobel if n['awardLabel'] == c] for c in categories}

women_by_category = {cat: [w['personLabel'] for w in winners if w['sexLabel'] == 'female']
 for cat, winners in winners_by_category.items()}

Do lab 1
"""
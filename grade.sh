#!/bin/bash

rm results.txt
timeout 500 python3 keyboard.py <<<anything
test -f results.txt && grade=$(cat results.txt) || grade=0
mypy --strict --disallow-any-explicit ./*.py && ((grade = grade + 5))
black --check ./*.py && ((grade = grade + 5))
echo "$grade" >results.txt
echo "Your base grade is: $grade"
if ((grade == 90))
then
    echo "You can compete for the remaining 10 points!"
    echo "Use tuning, control, and meta-optimization to find better solutions."
    echo "If you have questions about how grading happens, just look at this script."
fi
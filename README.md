####################################################
# COMP3106 - Introduction to Artificial Intelligence
# Assignment 2

# March 2022, Zakaria Ismail

# Copyright (c) 2022 by Zakaria Ismail 
# All rights reserved.
####################################################

Activate virtual environment using:
`source env/bin/activate`

Deactivate virtual environment using:
`deactivate`

To run ALL tests, run:
`./A2.py -v`
To display only failing tests, run:
`./A2.py`

Part 1, Resolution Inference Function for Propositional Logic Design:
- function PL_Resolution(KB, Alpha)
- KnowledgeBase obj
- PropositionalLogicSentence (PLSentence?) obj
- QuerySentence (inherits PLSentence?) obj

Note: I will opt for creating less objects, so I'll use sets/lists of integers

Problems:
- I can't create sets containing sets... sad

Observed patterns for DeMorgan's on a CNF sentence
- the number of clauses in the RAW negated CNF sentence is the product of the
    number of elements in each clause
    -> total number of combinations where you pick one item from each clause
- the number of literals in the RAW negated CNF sentence is the number of clauses
    in the sentence
- im sure there's a combinations library for this...
    -> itertools.product()

Part 2, Forward Chaining Inference Function for Propositional Logic Design:
- function PL_FC_Entails(KB, Alpha)
- 
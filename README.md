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

Part 2, Forward Chaining Inference Function for Propositional Logic Design:
- function PL_FC_Entails(KB, Alpha)
- 
#!/usr/bin/env python3
####################################################
# COMP3106 - Introduction to Artificial Intelligence
# Assignment 2

# March 2022, Zakaria Ismail - 101143497

# Copyright (c) 2022 by Zakaria Ismail 
# All rights reserved.
####################################################

import doctest
import logging
import sys

class Literal:
    """
    
    """
    pass

class Clause:
    """
    Set of Literals forming disjoint sentence.
    """
    pass

class CNFSentence:
    """
    Set of Clauses forming CNF sentence.
    """
    pass

class KnowledgeBase:
    """
    
    """
    pass

def PL_Resolution(KB, Alpha):
    """
    
    """
    pass

def PL_FC_Entails(KB, Alpha):
    """
    
    """
    pass

if __name__ == "__main__":
    header = """
    ####################################################
    # COMP3106 - Introduction to Artificial Intelligence
    # Assignment 1

    # February 2022, Zakaria Ismail - 101143497

    # Copyright (c) 2022 by Zakaria Ismail 
    # All rights reserved.
    ####################################################

    Uncomment doctest.testmod() to run the automated doctests.

    Library dependencies:
    """
    print(header)
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(message)s')
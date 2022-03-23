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
from pprint import pprint
import itertools

############
# Part 1
############
class Literal(int):
    """
    Literal.

    Q: Do I even need to abstract it this much?
    Couldn't I just represent it as an integer
    and call it a day... Check if the two integers
    add up to 0 and voila. No need for fancy abstractions.
    Maybe I could make it inherit int?

    """
    # def __init__(self, symbol, is_positive):
    #     self.symbol = symbol
    #     self.is_positive = is_positive
    
    # def __repr__(self) -> str:
    #     output = ""
    #     if self.is_positive:
    #         output.append("-")
    #     return output.append(str(self.symbol))
    pass

class Clause(set):
    """
    Set of Literals forming disjoint sentence.
    
    Note: doctests could fail because I'm using sets,
    so not ordered

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
    ...

    Args:
        - KB (): list of CNF sentences
        - Alpha (): also a list of CNF sentences

    Returns:
        - 1 if KB entails Alpha, -1 otherwise
    
    Theory:
        - For any sentences a and b, a ENTAILS b iff a => b is valid
            - this is equivalent to a OR NOT b, which is also NOT a AND b
        - we want to prove that KB ENTAILS a, wh
    Pseudocode:
    
    function PL-RESOLUTION(KB, a) returns true or false
        inputs: KB the knowledge base, a sentence in propositional logic
                a, the query, a sentence in propositional logic

        clauses <-- the set of clauses in the CNF representation of KB AND NOT a
        new <-- {}
        loop do
            for each pair of clauses Ci, Cj in clauses do
                resolvents <-- PL-RESOLVE(Ci, Cj)
                if resolvents contains the empty clause then 
                    return true
                new <-- new UNION resolvents
            if new SUBSET OF clauses then
                return false
            clauses <-- clauses UNION new

    Approach:
        1. Iterate over each CNF sentence in KB and add each clause to the set of
            clauses
            - convert clause to set and then back to list to set up an order + check
            if in set
        2. Negate Alpha CNF sentence and add each clause to the set of clauses
            - '''
        3. For each pair of clauses, resolve Ci and Cj and return the list of new clauses
            i. ~~if list of clauses is empty~~ WRONG, if it CONTAINS the empty clause, return true
            ii. Add resolved clauses to the set of new clauses
                - no duplicates
        4. If every new clause is already in the set of clauses, then return false. Else,
            add the (unique) clauses to the set of clauses
        5. Repeat from 3.

    Possible improvements:
        - Decrease clause search from O(n) to O(log n) by maintaining a BST/heap

    PL_Resolution([[[-2], [1]], [[1, 2]], [[-1, -2]], [[1, -2]]], [[1, 2], [-1, -2]])
    1
    >>> PL_Resolution([[[-2], [1]], [[1, 2]], [[-1, -2]], [[1, -2]]], [[1, 2], [-1, -2]])
    1
    >>> PL_Resolution([[[-1, -2]], [[1, -2], [1, -3]]], [[-1, -2, -3], [1, 3]])
    -1
    >>> PL_Resolution([[[-1, -2], [1, -2], [1]], [[-2]]], [[-1, 2]])
    -1
    >>> PL_Resolution([[[1, -2, 4]], [[-2, -3, 4]]], [[2, 4], [-1, -2, 3, -4], [1, -2, 3, -4]])
    -1
    >>> PL_Resolution([[[2, -3], [-2, -3]], [[-1]], [[1, -2, 3], [1, -2, -3], [1, -2], [-1, -2, -3]], [[-1, -3]]], [[-3]])
    1
    """
    # Test 1 is failing
    clauses = []
    # Add the set of clauses in KB
    for CNF_sentence in KB:
        for clause in CNF_sentence:
            clause_s = list(set(clause))  # "sorting and also clearing duplicate literals"
            if clause_s not in clauses:
                clauses.append(clause_s)
    
    # Add the set of negated clauses in Alpha
    neg_Alpha = _Negate_CNF_Sentence(Alpha)     # shouldn't I be deep copying... that's expensive tho, not rlly worth
    for clause in neg_Alpha:
        # TBD - The toughest challenge O_O
        clause_s = list(set(clause))
        if clause_s not in clauses:
            clauses.append(clause_s)

    while True:
        new = []    # initialize set of new clauses
        # For each pair of clauses, resolve Ci and Cj
        for Ci, Cj in itertools.combinations(clauses, 2):
            resolvents = _PL_Resolve(list(set(Ci)), list(set(Cj)))    # get list of resolved clauses
            if [] in resolvents:
                # if the empty clause exists
                return 1
            for resolvent in resolvents:
                # Add unique resolvents to the set of new clauses
                if resolvent not in new:
                    new.append(resolvent)

        is_subset = True
        for n in new:
            # Check that new is subset of set clauses
            if n not in new:
                # Add to set of clauses if unique
                is_subset = False
                clauses.append(n)
        
        if is_subset:
            return -1
            

# Maybe I should use objects....
# Why do I have to program DeMorgan's.... it's only used once though
def _get_clause_set():
    """
    Input list 
    """
    pass

def _PL_Resolve(Ci, Cj):
    """
    Resolves two clauses with complementary literals.
    NOTE: don't simplify resolved clauses with complementary
    literals in them, however simplify duplicated clauses
        -> why? I don't know.... I could check if it gives
        the same results

    >>> _PL_Resolve([-2], [1])
    []
    >>> _PL_Resolve([-1,-2,-3], [-1,2])
    [[-1,-3]]
    >>> _PL_Resolve([-1,-3,-4,-5], [-1,-3,-4,5])
    [[-1,-3,-4]]
    >>> _PL_Resolve([-1,-3,-4,-5], [-1,-3,4,5])
    [[-1,-3,-4,4], [-1,-3,-5,5]]
    """
    # Test 2 is failing for some reason....
    resolved_clauses = []
    for lit in Ci:
        if (lit * -1) in Cj:
            # If complementary exists, create resolved clause
            temp_i = Ci.copy()
            temp_i.remove(lit)
            temp_j = Cj.copy()
            temp_j.remove(lit * -1)
            clause = []
            clause.extend(temp_i)
            clause.extend(temp_j)
            clause = list(set(clause))
            if clause not in resolved_clauses:
                resolved_clauses.append(clause)
    return resolved_clauses

def _Negate_CNF_Sentence(CNF_sentence):
    """
    Negates a CNF sentence.
    1. Place negation in front of each clause
    2. Apply DeMorgan's for each clause
    3. ...
        - is there a pattern for this :(
        - i can probably use a permutation/combination/product python library
            to make it hella easy for me.
    Solution:
        - Negate all literals
        - Get product of all the clauses
        - Clean up each clause:
            1. if there are duplicates in a clause, remove. Can b done by converting list(set())
            2. remove pairs that add to 0 (P1 and not P1)

    >>> _Negate_CNF_Sentence([[1,2],[-1,-2]])
    [[1,-2],[-1,2]]
    >>> _Negate_CNF_Sentence([[1, 2], [-1], [-1, 2]])
    [[1,-2]]
    """
    # Test 2 is failing...
    # Now it's not clearing the tautology cases????
    negated_sentence = []
    for raw_clause in itertools.product(*CNF_sentence):
        # Get product of all the clauses
        raw_clause = list(set(raw_clause))  # remove duplicate literals and "sort"
        raw_clause = [literal * -1 for literal in raw_clause]   # negate all literals
        # ~~Remove pairs of literals that add to 0~~
        # Set clause to [] if P or not P detected
        is_tautology = False
        for i in range(len(raw_clause)):
            for j in range(i, len(raw_clause)):
                if raw_clause[i] + raw_clause[j] == 0:
                    # clause is equivalent to []
                    raw_clause = []
                    is_tautology = True
                    break
            if is_tautology: break
        #if is_tautology: break
        
        clause = list(set(raw_clause))
        if clause != [] and clause not in negated_sentence:
            # Do not append a True (empty clause) to the CNF
            negated_sentence.append(clause)

    return negated_sentence


##########
# Part 2
#########

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
    doctest.testmod()

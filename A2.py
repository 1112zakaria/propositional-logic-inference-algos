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
import pdb

log = logging.getLogger(__name__)

############
# Part 1
############

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
    >>> PL_Resolution([[[-1, -3, -4, -5], [-1, -3, -4, 5]], [[-1, -2, 3, 4, 5], [-1, -2, -3]], [[-1, 2, 3, -4, -5], [-2, -4, -5], [1, -2, -3]]], [[1, 3, -4, 5]])
    -1
    """
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
        clause_s = list(set(clause))
        if clause_s not in clauses:
            clauses.append(clause_s)

    while True:
        new = []    # initialize set of new clauses
        # For each pair of clauses, resolve Ci and Cj
        for Ci, Cj in itertools.combinations(clauses, 2):
            resolvents = _PL_Resolve(list(Ci), list(Cj))    # get list of resolved clauses
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
            if n not in clauses:
                # Add to set of clauses if unique
                is_subset = False
                clauses.append(n)
        
        if is_subset:
            return -1
            

def _PL_Resolve(Ci, Cj):
    """
    Resolves two clauses with complementary literals.

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

    negated_sentence = []
    for raw_clause in itertools.product(*CNF_sentence):
        # Get product of all the clauses
        raw_clause = list(set(raw_clause))  # remove duplicate literals and "sort"
        raw_clause = [literal * -1 for literal in raw_clause]   # negate all literals
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
    
    Pseudocode:

    function PL-FC-ENTAILS(KB, q) returns true or false
        inputs: KB, the knowledge base, a set of propositional definite clauses
                q, the query, a proposition symbol

        count <-- a table, where count[c] is the number of symbols in c's premise
        inferred <-- a table, where inferred[s] is initially false for all symbols
        agenda <-- a queue of symbols, initially symbols known to be true in KB

        while agenda is not empty do
            p <-- POP(agenda)
            if p == q then return true
            if inferred[p] == false then
                inferred[p] <-- true
                for each clause c in KB where p is in c.PREMISE do
                    decrement count[c]
                    if count[c] == 0 then add c.CONCLUSION to agenda
        return false
    
    Approach:
        Init:
            - define MAP inferred
            - define MAP count
            - define LIST agenda
        1. Iterate over each clause in KB and everytime a premise (negative literal)
            is present, add to the literal's count in MAP count
            i. Define MAP inferred for literal l as False when it is first detected
            ii. When literal l is detected ~~and it is positive and clause is length 1,
                set l to be True in inferred and~~ (DONT INBETWEEN ~) add to LIST agenda
            iii. MAP length of clause - 1 in count if len clause > 1
        2. Pop a literal p from agenda. If p equals the query q, return True
        3. If inferred[p] is False, set to True
        4. For every clause c in KB, if p is a premise (negative literal) in c, decrement
            count[c]
        5. If count[c] == 0, add conclusion (positive literal) in clause c to agenda
        6. Goto 2 and repeat while agenda is not empty

    >>> PL_FC_Entails([[[-1, 3], [1, -2]], [[2]], [[3]], [[-1, 2]], [[1, -3]], [[-1, -2, 3]], [[-2, 3]]], [[1]])
    1
    >>> PL_FC_Entails([[[3]], [[2]], [[1, -2]], [[-1, 3]], [[1, -3]]], [[1]])
    1
    >>> PL_FC_Entails([[[-1, 3], [2]], [[-2, 4]], [[2, -3, -5]], [[1, -4]], [[-1, -3, 4], [1, -2, -3], [1]], [[2, -4, -5]], [[3, -5]]], [[5]])
    -1
    """
    # Assumes that there are not duplicate clauses....
    inferred = {}
    count = {}
    agenda = []
    clauses = []

    q = Alpha[0][0]

    for CNF_sentence in KB:
        for clause in CNF_sentence:
            clause.sort()   # make it easier to access conclusion
            for literal in clause:
                if literal not in inferred and literal > 0:
                    # Initialize inferred map
                    inferred[literal] = False
                if literal > 0 and len(clause) == 1 and literal not in agenda:
                    # Lone literal detected
                    agenda.append(literal)
            # map number of premises
            count[tuple(clause)] = len(clause) - 1    # checking for all clauses
            clauses.append(clause)
    
    while agenda != []:
        p = agenda.pop()
        if p == q: return 1
        if inferred[p] == False:
            inferred[p] = True
            for clause in clauses:
                if (p * -1) in clause:
                    # Complentary found in clause
                    count[tuple(clause)] -= 1
                if count[tuple(clause)] == 0:
                    agenda.append(clause[-1])
    return -1
    

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

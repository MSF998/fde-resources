# Python Refresher

**Date:** 2026-05-12 | **Track:** Technical | **Session:** XX

## Key Concepts

- Python Class

  ```python
    class PokemonsPlay:
        pokemons_list = []

        # This is a constructor. Constructors ensure memory allocation in memory
        # self represent the object of the class. Initialized by python runtime
        def __init__(self):
            print("Welcome")

    pObj = PokemonsPlay() #pOjb is out object of the class
  ```

- File Handling
  ```python
  pokemon_list = open('pokemon.csv','r').readlines() # readlines return a list
  ```

### Functional Programming

- reduce

  ```python
  from functools import reduce

  sum = reduce(lambda x,y: x+y, iterable)

  data = [3,4,5,1,2]
  reduce(lambda x,y: x+y, data) # 15

  # Initial Expression
  # X     Y         x = x+y
  # ----------------------
  # 3     4
  #       5
  #       1
  #       2

  # Once calculation starts
  # X     Y         x = x+y
  # ----------------------
  # 3     4          3 + 4 = 7
  # 7     5          7 + 5 = 12
  # 12    1         12 + 1 = 13
  # 13    2         12 + 2 = 15

  #reduce() is designed to return X variable as the final result i.e 15
  ```

## What I Built / Tried

-

## Insights & Opinions

-

## Questions / Gaps

-

## Links to Projects

-

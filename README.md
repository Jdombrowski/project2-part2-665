# Project 2 Part 2 
## Jonathan Dombrowski 916921673

## How to compile
Simply run `python autograder.py` to see the grading in action

### I. Overview
### II. Implementation 
### III. Conclusion

---------------------------------------------------
## Overview
The project extended the previous pacman state with the completion of the minimax function. 
We were tasked with implementing both expectimax, and alpha-beta pruning from the extension of minimax, since the two 
are so similar. Following the pseudocode from the slides, along with the material from the lectures was enough
to complete the project. After that, we were tasked with creating a better evaluation function. 
The code was incredibly similar and although I did not have time to complete the modular implementation, I was still 
able to create the other two functions. 

## Implementation 
The code written was based off of the dispatch methodology of the minimax of the last project. The change of the alpha
beta was simply adding the change of tracking the alpha and beta. With expectimax, it was simply changing the minimum function 
to the average function. As far as the 
evaluation function goes, I simply copied over what I could from the previous evaluation function that I create for the reflex
agent. It was very effective, so I refactored what I could into the next iteration. 
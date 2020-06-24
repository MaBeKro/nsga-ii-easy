# nsga-ii-easy

## short

This is a quick implementation of the nsga ii algorithm, as it was described [here](http://www.dmi.unict.it/mpavone/nc-cs/materiale/NSGA-II.pdf).

## long

Background: I made this for personal needs, but if it helps you go ahead.
There is some testing and no performance optimization.

Checkout the example if you want to see it in action.
If you want to try it yourself, the only function you need is `select_next_generation`.
Just put in Individuals that have a Sequence of numbers as fitness attribute and remember that this function does not copy Individuals, so do that yourself before mutating or things get weird.

## details

This implementation differs a little bit from the paper:
The crowding distance compare is only used between individuals of the same rank, so I gave it the option to not check for the rank.


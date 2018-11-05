To run this program, open the main.py, type the tow agents you want, and their parameters.
The default setting is 

startWin(8,player1 = 'mcts', player2 = 'minmax', minmax_depth1 = 6, minmax_depth2 = 4, h1 = 'simple', h2 = 'good', time1 = 4, time2 = 8)

Which means, the player(white) 1 is mcts(uct) with 4 seconds, the player(black) 2 is minimal with 4 depth and good evaluation

There are three type of agents and human: "human", "random", "mcts","minimax"

For mcts(uct), you should give it one paramount, if it is player 1, then time1 = num is need, which num is second. For player 2 it us time2

For minimax, you should give it two parament, if it is player 1, then minmax_depth1 = num, which num is depth you want, and h1 = 'simple' or 'good' which let it use different evaluation. For player 2, they are minmax_depth2 and h2.

To test data using startNoC function. It will not should UI, an n is number of test.

The test data will be released in data folder.
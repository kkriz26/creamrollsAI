---
# creamrollsAI
reinforced learning in python on custom pygame (asteroids based)
based on YT tutorial for AI version of https://github.com/patrickloeber/python-fun/blob/master/snake-pygame/arial.ttf
see: https://www.youtube.com/watch?v=PJl4iabBEz0&t=463s

"python agent.py" initializes ML, while
kremrole.py is a vanilla simple player controlled game its based on "python kremrole.py"

neither take any arguments, for now options are switched inside the code. 
there are two implemented succesfull ML approaches: feeding the agent discretized space with true or false values of player or enemy occupies the space. this option does not work well with multiple enemies at once (see kremroleAI.py), this option has 38 parameters and requires smaller matrices (I used 38 input layer, two 128 layers and 5 output layers =e.g. left, right, top, bottom, no move. more general option feeds the agent onyly if there are enemies within range in either direction and if he is next to the either wall. this works with multiple enemies also and I used thus 10 input 5 output with intermediate 512 or 1024 layer. other would likely work too. 
learning rate had to be adjusted

If you try a new run with different matrix size or want to rerun a optimization, dont forget to delete/backup files in model directory.
check the random step policy for the starting n number of games

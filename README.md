# Racing Line
This program using a genetic algorithm to find a (non optimal) racing line for a given racetrack. The green lines are checkpoints or reward gates to be used in the reward function. I would like to make this code find an optimal racing line by using QLearning but atm, I do not have the capabilities to do so unfortunately. 

If you want to see it in action here is a link: https://youtu.be/Cl2fiM31jGU (terrible quality cause I have no idea how to record propely)
## Messing with it
For just running it, make sure you have pygame installed and then just run the main.py program. \
You can tune the hyperparameters, reward function, moveset, etc. to see if it finds a better racing line. \
If you would like to use your own track, just make one with the borders and the rest being a **transparent background**. Then add the checkpoints that you see fit.

## Bugs
For whatever reason, any line with a positive slope (not including vertical lines) does not work correctly and I cannot figure out why. \
I haven't really implemented what to do after finishing the first lap \
The little spazzing the car does is because it randomly picks between left right or forward so it is pressing left and right at the same time. That is also why it is so unoptimal but still pretty solid. 
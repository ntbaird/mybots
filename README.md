# Random Arm-Bots
Assignment 7 for CS 396 - Artificial Life

TO RUN THE SIMULATION:

In your Python terminal of choice, run search.py
This may look like the following:

python search.py
or python3 search.py

If any problems arise with inaccessible fitness files or locked body.urdf, please try running the command again.

That's it! Future assignments will apply these randomly generated bots into fully formed and evolvable creatures.

# Inspiration/Goal
Karl Sims' Evolved Creatures in competition:

![sims 1](https://user-images.githubusercontent.com/91085742/220190536-c142535f-b737-46b3-b837-d8c112a1107e.jpg)
![sims 2](https://user-images.githubusercontent.com/91085742/220190493-56745a34-700f-4147-a13d-ff79b7fda5b2.jpg)
![sims 3](https://user-images.githubusercontent.com/91085742/220190503-114b7c2a-8aa6-4c5a-97ee-ce1cfe636143.jpg)

Generated bots:

![image](https://user-images.githubusercontent.com/91085742/220190664-ca4085d6-d662-40a3-a9fd-3980f98c7017.png)
![image](https://user-images.githubusercontent.com/91085742/220190749-1451aa57-6dc3-48a8-adbb-7ffc0ba27574.png)

# Method
These bots are generated by first starting with a head and torso, then randomly extending the arms out on either side of the torso in the X, Y, and Z directions. These segments are sized randomly, but symmetrically across the body of the creature. This can also be mirrored to produce a true quadruped (that would most likely not fall over!)
![image](https://user-images.githubusercontent.com/91085742/220191065-f946c067-9e45-4854-b10b-c587afbbbcb1.png)

# Credits
 - r/ludobots for their incredibly detailed tutorial to introduce pyrosim and most features you see here. https://www.reddit.com/r/ludobots/
 - Northwestern University's Artificial Life Seminar
 - Check out these bots in motion here! https://youtu.be/3WNNRpyTTXA

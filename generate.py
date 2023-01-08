import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")

x = 0
y = 0
for j in range(5):
    for k in range(5):
        a = 1
        b = 1
        c = 1
        z = .5
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[a, b, c]) 
            z += a
            a *= .9
            b *= .9
            c *= .9
        y += 1
    x += 1
    y = 0


pyrosim.End()


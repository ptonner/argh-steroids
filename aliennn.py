from alien import Alien
import numpy as np
import neurolab as nl
import random

class AlienNN(Alien):

    def __init__(self, world,):
        super(AlienNN, self).__init__(world)
        # Alien.__init__(self,world)

        # self.angle = random.randint(-90, 90)
        # self.acceleration = [0,0]

        # self.net = nl.net.newff(weights)
        self.net = nl.net.newff([[-10,10] for i in range(5)], [5,5, 4])

        for l in self.net.layers:
            l.initf = nl.init.InitRand([-1., 1.], 'wb')

        self.net.init()
        # self.net.save('test.net')

    def buildInput(self):

        # print self.angle, self.velocity

        playerVec = np.array([self.world.player.position[0]-self.position[0], self.world.player.position[1]-self.position[1]])
        playerVec = playerVec/np.linalg.norm(playerVec)
        playerDot = np.dot(np.array(self.velocity)/np.linalg.norm(self.velocity), playerVec)

        distVelocity = np.add(self.velocity, self.world.player.velocity)
        distVelocityNorm = np.linalg.norm(distVelocity)

        # return [[self.angle, self.velocity[0], self.velocity[1], playerDot, random.random()*10-5]]
        # return [[self.velocity[0], self.velocity[1], playerDot, distVelocityNorm]]
        # return [[self.velocity[0], self.velocity[1]] + distVelocity.tolist()]
        return [self.velocity + distVelocity.tolist() + [playerDot]]

    def compute(self,v):

        return self.net.sim(v)

    def update(self):

        ivec = self.buildInput()
        ovec = self.compute(ivec)[0]

        # print self.angle-ovec[0], self.velocity[0] - ovec[1], self.velocity[1] - ovec[2]

        # self.angle = ovec[0]
        # self.velocity[0] = ovec[1]
        # self.velocity[1] = ovec[2]

        self.velocity[0] += ovec[1]
        self.velocity[1] += ovec[2]

        # self.velocity[0] *= (1+ovec[1])
        # self.velocity[1] *= (1+ovec[2])

        mag = np.sqrt((np.array(self.velocity)**2).sum()) * (3**ovec[3])
        self.velocity = [self.velocity[0]/mag, self.velocity[1]/mag]

        # if self.world.alien_time == 0:
        #     print ivec, ovec, self.velocity

        # print self.angle, self.velocity

        super(Alien, self).update()

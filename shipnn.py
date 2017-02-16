from ship import Ship
from bullet import Bullet
import numpy as np
import neurolab as nl
import random

class ShipNN(Ship):

    def __init__(self, world,):
        super(ShipNN, self).__init__(world)
        # Alien.__init__(self,world)

        # self.angle = random.randint(-90, 90)
        # self.acceleration = [0,0]

        # self.net = nl.net.newff(weights)
        self.net = nl.net.newff([[-10,10] for i in range(2)], [5,5, 4])

        for l in self.net.layers:
            l.initf = nl.init.InitRand([-1., 1.], 'wb')

        self.net.init()
        # self.net.save('test.net')

    def buildInput(self):

        y,x = self.positions()

        return [y+x]

    def compute(self,v):

        return self.net.sim(v)

    def positions(self,ls=None):
        if ls is None:
            ls = self.world.liveSprites(filter=[ShipNN, Bullet])

        y,x = [self.position[1]-s.position[1] for s in ls], [s.position[0]-self.position[0] for s in ls]

        # renormalize for wrapping map
        y = [z if abs(z)<self.world.height/2 else z-np.sign(z)*self.world.height for z in y ]
        x = [z if abs(z)<self.world.width/2 else z-np.sign(z)*self.world.width for z in x ]

        return y,x

    def angles(self,):

        return np.arctan2(*self.positions()) * 180 / np.pi

    def regions(self,):
        angles = self.angles()

        return np.where((angles > 0) & (angles < 90), 0,
                    np.where(angles>90, 1,
                        np.where((angles<0) & (angles > -90), 2, 3)))

    def update(self):

        regions = self.regions()
        # print self.position
        # print self.positions()


        ivec = self.buildInput()
        print np.array(ivec).shape, self.net.ci
        ovec = self.compute(ivec)[0]

        print ovec

        # print self.angle-ovec[0], self.velocity[0] - ovec[1], self.velocity[1] - ovec[2]

        # self.rotate_by(int(ovec[0]*6))
        self.rotate_by(ovec[0])

        self.thrust(ovec[1]>0)

        if ovec[2] > 0:
            self.fire()
            
        super(ShipNN, self).update()

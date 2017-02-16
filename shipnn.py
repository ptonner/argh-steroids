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
        self.net = nl.net.newff([[-10,10] for i in range(9)], [5,5, 4])

        for l in self.net.layers:
            l.initf = nl.init.InitRand([-1., 1.], 'wb')

        self.net.init()
        # self.net.save('test.net')

    def liveSprites(self):
        return self.world.liveSprites(filter=[ShipNN, Bullet])

    def buildInput(self):

        ls = self.liveSprites()
        sizes = np.array(map(lambda x: x.scale, ls))

        y,x = self.positions()
        regions = self.regions()
        angles = self.angles()
        dist = self.distances()

        regionCounts = [sum(regions==i) for i in range(4)]

        select = dist == dist.min()
        angle = angles[select]
        size = sizes[select]
        y = y[select]
        x = x[select]

        # count in regions
        # distance to closest in region

        return [[angle, dist.min(), size, x, y]+regionCounts]

    def compute(self,v):

        return self.net.sim(v)

    def positions(self,ls=None):
        if ls is None:
            ls = self.world.liveSprites(filter=[ShipNN, Bullet])

        y,x = [self.position[1]-s.position[1] for s in ls], [s.position[0]-self.position[0] for s in ls]

        # renormalize for wrapping map
        y = np.array([z if abs(z)<self.world.height/2 else z-np.sign(z)*self.world.height for z in y ])
        x = np.array([z if abs(z)<self.world.width/2 else z-np.sign(z)*self.world.width for z in x ])

        return y,x

    def distances(self,ls=None):
        y,x = self.positions(ls)

        mag = np.sqrt(x**2 + y**2)

        return mag

    def angles(self,norm=True):

        angles = np.arctan2(*self.positions()) * 180 / np.pi
        if norm:
            angles += self.angle
            angles = angles%360
            angles[angles>180] = angles[angles>180]-360
        return angles

    def regions(self,):
        angles = self.angles()

        angles = angles-180

        return np.where((angles > 0) & (angles < 90), 0,
                    np.where(angles>90, 1,
                        np.where((angles<0) & (angles > -90), 2, 3)))

    def update(self):

        try:

            ivec = self.buildInput()
            ovec = self.compute(ivec)[0]

            # raise Exception()

            self.rotate_by(ovec[0])

            self.thrust(ovec[1]>0)

            if ovec[2] > 0:
                self.fire()
        except Exception, e:
            # print e
            pass

        super(ShipNN, self).update()

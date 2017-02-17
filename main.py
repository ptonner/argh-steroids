#!/usr/bin/python
from __future__ import print_function

import os
import random
import math

import pygame
from pygame import mixer

import util
import asteroid
import aliennn
import text
import world
import ship
import shipnn

import numpy as np
from database import Network, Base, Run
from mutate import Mutate


class Game(object):
    def __init__(self, surface, session, draw=True, net=None, evolve=False):
        self.surface = surface
        self.session = session
        self.world = world.World(surface)
        self.width = self.world.width
        self.height = self.world.height
        self.clock = pygame.time.Clock()
        self.level = 1
        self.draw = draw

        self.net = None
        self.run = None

        self.loadNet = not net is None
        self.evolve = evolve
        self.epoch = 1
        self.epochSize = 8
        self.offspringRate=.25

        if self.evolve:
            self.currentNets = list(self.session.query(Network).join(Run).order_by(Run.score.desc()))[:self.epochSize]
            self.currentRuns = []
            self.testedNets = []

            print(self.currentNets)

        if self.loadNet:
            self.net = session.query(Network).filter(Network.id==net).first()

        # print self.net

    def draw_hud(self):
        text.draw_string(self.surface, "SCORE %.2lf" % self.world.score,
                         util.WHITE, 10, [10, 20])
        text.draw_string(self.surface, "LEVEL %d" % self.level,
                         util.WHITE, 10, [10, 40])

        try:

            text.draw_string(self.surface, "NETWORK %d" % self.net.id,
                             util.WHITE, 10, [10, 60])

            ivec = self.world.player.buildInput()
            text.draw_string(self.surface, "IVEC %s" % '\t'.join(['%.0lf'%i for i in ivec[0]]),
                             util.WHITE, 10, [10, 80])

            ovec = self.world.player.compute(ivec)[0]
            text.draw_string(self.surface, "OVEC %s" % '\t'.join(['%.2lf'%i for i in ovec]),
                             util.WHITE, 10, [10, 100])

            # y,x = self.world.player.positions()
            # s = "POSITIONS %s" % '\t'.join([', '.join(['%.0lf'%i for i in p]) for p in (x,y)])
            # text.draw_string(self.surface, s,
            #                  util.WHITE, 10, [10, 60])
            # regions = self.world.player.regions()
            # text.draw_string(self.surface, "REGIONS %s" % '\t'.join(['%d'%i for i in regions]),
            #                  util.WHITE, 10, [10, 80])
            # # text.draw_string(self.surface, "ANGLE %.2lf" % self.world.player.angle,
            # #                  util.WHITE, 10, [10, 120])
            # angles = self.world.player.angles(norm=True)
            # text.draw_string(self.surface, "ANGLES %s" % '\t'.join(['%.2lf'%i for i in angles]),
            #                  util.WHITE, 10, [10, 100])
        except:
            pass


    def start_screen(self):
        self.world.add_text('ARGH ITS THE ASTEROIDS', scale = 20)
        self.world.add_text('PRESS ESC TO QUIT')
        self.world.add_text('PRESS LEFT AND RIGHT TO ROTATE')
        self.world.add_text('PRESS UP FOR THRUST')
        self.world.add_text('PRESS SPACE FOR FIRE')
        self.world.add_text('PRESS M TO TURN MUSIC ON OR OFF')
        self.world.add_text('OR USE MOUSE CONTROLS')
        self.world.add_text('WATCH OUT FOR ALLEN THE ALIEN')
        self.world.add_text('PRESS ENTER TO START', scale = 20)

        for i in range(4):
            asteroid.Asteroid(self.world, random.randint(50, 100), 1)
        self.world.particle.starfield()

        while not self.world.quit and not self.world.enter:
            self.world.update()
            self.surface.fill(util.BLACK)
            self.draw_info()
            self.world.draw()
            # set the limit very high, we can use the start screen as a
            # benchmark
            self.clock.tick(200)
            pygame.display.flip()

    def draw_info(self):
        if self.world.info:
            text.draw_string(self.surface,
                             "FPS %d" % self.clock.get_fps(),
                             util.WHITE, 10, [10, self.height - 20])
            text.draw_string(self.surface,
                             "OBJECTS %d" % self.world.n_objects(),
                             util.WHITE, 10, [10, self.height - 40])
            text.draw_string(self.surface,
                             "PARTICLES %d" % self.world.particle.n_particles(),
                             util.WHITE, 10, [10, self.height - 60])

    def level_start(self):
        start_animation_frames = 0#100
        start_animation_time = start_animation_frames

        while not self.world.quit:
            if start_animation_time == 0:
                break

            self.world.update()
            if self.world.spawn:
                asteroid.Asteroid(self.world,
                                  random.randint(75, 100),
                                  self.level)

            self.surface.fill(util.BLACK)
            self.draw_hud()

            self.draw_info()
            start_animation_time -= 1
            t = float(start_animation_time) / start_animation_frames
            # text.draw_string(self.surface, "LEVEL START", util.WHITE,
            #                  t * 150,
            #                  [self.width / 2, self.height / 2],
            #                  centre = True,
            #                  angle = t * 200.0)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def play_level(self):
        while not self.world.quit:
            if self.world.n_asteroids == 0:
                break
            if not self.world.player:
                break
            if self.world.next_level:
                self.world.remove_asteroids()
                break

            self.world.update()

            if self.draw:
                self.surface.fill(util.BLACK)
                self.draw_hud()
                self.draw_info()
                self.world.draw()
            # self.clock.tick(60)
            pygame.display.flip()

            print(self.status() + "         ", end='\r')

    def game_over(self):
        end_animation_frames = 100
        end_animation_time = end_animation_frames

        while not self.world.quit:
            if end_animation_time == 0:
                break

            self.world.update()

            self.surface.fill(util.BLACK)
            self.draw_hud()
            self.draw_info()
            end_animation_time -= 1
            t = float(end_animation_time) / end_animation_frames
            text.draw_string(self.surface, "GAME OVER", util.WHITE,
                             math.log(t + 0.001) * 150,
                             [self.width / 2, self.height / 2],
                             centre = True,
                             angle = 180)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def epilogue(self):
        while not self.world.quit:
            if self.world.enter:
                break

            self.world.update()

            if self.draw:
                self.surface.fill(util.BLACK)
                text.draw_string(self.surface, "PRESS ENTER TO PLAY AGAIN",
                                 util.WHITE,
                                 20,
                                 [self.width / 2, self.height / 2],
                                 centre = True,
                                 angle = 0)
                self.draw_hud()
                self.draw_info()
                self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def status(self):

        return 'net: %s, score: %.2lf, level: %d, n_asteroids: %d' % (self.net, self.world.score, self.level, self.world.n_asteroids)

    def nextNetwork(self):

        if self.loadNet:
            self.run = Run(network=self.net)
            self.session.add(self.run)

        elif self.evolve:

            # don't add null net
            if not self.net is None:
                self.testedNets.append(self.net)

            # trigger new epoch
            if len(self.currentRuns) == self.epochSize:
                assert len(self.testedNets) == self.epochSize

                scores = [r.score if r.score > 0 else 0 for r in self.currentRuns]
                normScore = [1.*s/sum(scores) for s in scores]

                numOffsping = int(self.offspringRate*self.epochSize)
                numSurvive = self.epochSize - numOffsping

                self.currentNets = []
                self.currentRuns = []
                self.testedNets = []

                # add surviving nets
                counts = np.random.multinomial(numSurvive, normScore)
                for i,c in enumerate(counts):
                    self.currentNets += [self.testedNets[i]]*c

                # generate offspring
                counts = np.random.multinomial(numOffsping, normScore)
                for i,c in enumerate(counts):
                    for j in range(c):
                        temp  = shipnn.ShipNN(self.world, self.testedNets[i])
                        m = Mutate(temp.net)
                        n = Network(parent = self.testedNets[i])
                        self.session.add(n)
                        self.session.commit()

                        m.mutant().save('.networks/%d.csv'%n.id)
                        self.currentNets.append(n)

                print (self.currentNets)

            self.net = self.currentNets.pop()
            self.run = Run(network=self.net)
            self.session.add(self.run)
            self.currentRuns.append(self.run)

        else:
            self.net =  Network()
            self.session.add(self.net)

            self.run = Run(network=self.net)
            self.session.add(self.run)

        self.session.commit()

    def play_game(self):
        # self.start_screen()

        while not self.world.quit:
            self.level = 1
            self.world.reset()
            self.world.particle.starfield()

            # if not self.loadNet:
            #     self.net =  Network()
            #     self.session.add(self.net)
            # self.net = self.nextNetwork()
            #
            # self.run = Run(network=self.net)
            # self.session.add(self.run)
            #
            # self.session.commit()

            self.nextNetwork()

            while not self.world.quit:
                self.level_start()

                self.world.add_player(self.net)

                # self.alien = aliennn.AlienNN(self.world)
                for i in range(self.level * 2):
                    asteroid.Asteroid(self.world,
                                      random.randint(75, 100),
                                      0.5 + self.level / 4.0)

                # for i in range(self.level*1):
                #     self.alien = aliennn.AlienNN(self.world)

                self.play_level()

                if not self.world.player:
                    break

                if not self.world.quit:
                    self.level += 1
                    self.world.score += 500

            print()

            self.run.levelsCompleted = self.level
            if self.world.shots > 0:
                self.run.accuracy = 1.*self.world.bulletImpacts/self.world.shots
            self.run.score = self.world.score

            self.session.add(self.run)
            self.session.commit()

            # self.game_over()
            # self.epilogue()

def main():

    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument("--noDraw",dest='noDraw',action='store_true',default=False)
    parse.add_argument("--net",default=None,type=int,dest='net')
    parse.add_argument("--evolve",dest='evolve',action='store_true',default=False)
    args = parse.parse_args()

    ########################################
    # start database stuff

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///history.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    # Insert a Person in the person table
    # new_person = Person(name='new person')
    # session.add(new_person)
    # session.commit()

    # Insert an Address in the address table
    # new_address = Address(post_code='00000', person=new_person)
    # session.add(new_address)
    # session.commit()

    # end database stuff
    #########################################

    pygame.init()
    mixer.init()

    # audio channel allocation:
    #
    #   0 - background music
    #   1 - ship engines
    #   2 - ship guns
    #   3 - alien
    #   4 to 7 - explosions
    #
    # we reserve the first four channels for us to allocate and let mixer pick
    # channels for explosions automatically
    mixer.set_reserved(4)


    surface = pygame.display.set_mode()
    # surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    # surface = pygame.display.set_mode([800, 600])
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Argh, it's the Asteroids!!")

    game = Game(surface,session, not args.noDraw, args.net, evolve=args.evolve)

    game.play_game()

    pygame.quit()

if __name__ == "__main__":
    main()

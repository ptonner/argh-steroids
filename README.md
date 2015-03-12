# Argh-steroids

Asteroids-like game using pygame. 

Install [pygame](http://pygame.org) and run `main.py`.

![Start screen](/screenshots/start_screen.png)
![In play](/screenshots/play.png)

# Features

* Asteroids bump off each other. It uses a map to make collision detection
  fast.

* Your ship has a shield and you can bump into asteroids a few times. The
  shield regenerates slowly.

* Mouse and keyboard controls.

* Vector graphics using an affine transform rather than a lot of trig
  functions. 

* Particle system for explosions.

* Small, simple code. It's only 1,200 lines for everything, it should be easy 
  to hack on.

* It's fast enough on a Raspberry-Pi 2. On my modest laptop it can animate 
  more than 200 asteroids and more than 5,000 particles at 60 fps.

# Secret keys

* Hold 'S' during level start animation to spawn extra asteroids for testing.

* Hold 'I' during play to see object and FPS counts.

# TODO

* Collision detection is just touching circles, we could look at the geometry
  as well to get pixel-perfect detection.

* Collision physics just exchanges the two velocities, we could do true
  billiard-ball collisions.

* The wrap-around is rather crude. We could do collisions correctly on screen
  edges and draw asteroids as they wrap.
 
# Author

John Cupitt

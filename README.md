# Argh-steroids

Asteroids-like game using pygame. 
(Python 3 compatible)

Install [pygame](http://pygame.org) and run `main.py`.

Alternatively, there's a [WebGL 
version](http://jcupitt.github.io/argh-steroids-webgl).

Sounds From [FreeSound.org](https://www.freesound.org/)

![Start screen](/screenshots/start_screen.png)
![In play](/screenshots/play.png)


# Changes from Original

* Added sound (on TODO list)

* Made python 3 compatible (on TODO list)

* changes shield behaviour (not on TODO list)
Shield mode 1 uses a key press and stays on for a period of time before turning off. There is a cool down between key presses
(0 for original shield mode)
User can change SHIELDBEHAVIOR with the variable on line 23 in ship

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

* Hold 'I' to see object and FPS counts.

* Press 'P' to toggle particles on and off. This can help the framerate
  on slower systems.

* Press 'N' to skip to the next level. Handy for testing. 

# TODO
* Collision detection is just touching circles, we could look at the geometry
  as well to get pixel-perfect detection.

* Collision physics just exchanges the two velocities, we could do true
  billiard-ball collisions.

* The wrap-around is rather crude. We could draw sprites as they wrap.
 
# Author

John Cupitt

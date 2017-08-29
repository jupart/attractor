#########
Attractor
#########
A puzzle solving mobile game where the player uses the forces of magnetic attraction
and replusion to achieve goals.

* built with `python <https://python.org>`_, `kivy <kivy.org>`_, `kivent <https://kivent.org>`_
* intended for release on android


########
Features
########
* 2d graphics
* music tracks for sets of levels
* sound effects for attractor collision
* touch to move magnets
* achievement system
* timed play
* scored play

###################
Project checkpoints
###################
√ First level, navigating attractor through obstacles using magnets
√ Decide on visual aesthetic
3. First set of 10 levels, sound effects
4. Decide on aural aesthetic, music for first set
5. Alpha release
6. Incorporate feedback where necessary
7. Next set of 10 levels
8. Beta release

##############
Idea Sketchpad
##############
√ player controls an attractor that can switch "poles"
  √ neutral, north, or south based
  √ maybe it should be simply charged-based (positive, negative, neutral)
  √ level is laid out statically, so player only changes the attractor's charge

√ improve level menu
√ display the time it took to finish level
√ display # of Attractor changes it took
* metrics: time/level and time/pole/level
√ implement membrane
x magnet show needs alpha gradient to edge or some other design
√ continue to next level on completion, only show selector from menu
x horizontal levels in which magnets only affect v_y (flappy bird?)

![demo](demo.jpg)


# Introduction
A simple **image viewer** that focuses on cumulative browsing.
Images are queried from a *search bar* and loaded onto an infinite *board*, it can accomodates and infinite amount of images at different scales without compromises on quality.


## Installation (Linux)
1. Download a *Python 3.14.5 (or higher)* installer from [here](https://www.python.org/downloads/), unless the former isn't already installed on your machine
2. Execute the installer with privilege `sudo python -BO install.py`


## Usage
1. Run the program with `tom [SAVE].tom` (replace `[SAVE]` with a name of your choice)
2. Press `s` on your keyboard to open the *search bar*
3. Write a path to a valid image file and press `RETURN` on the keyboard to load it onto the *board*
4. Left click an image and drag the mouse, the image will drag as well
5. Left click an image and scroll the mouse wheel, the image will rescale
6. Right click and drag the mouse, the entire canvas will drag as well
7. Scroll the mouse wheel, the canvas will rescale
8. Left click the mouse cursor onto an image and press `x` on the keyboard to delete it


## Troubleshooting
* If *PyGame Community Edition* doesn't install regularly from pip, try following the specifications from [here](https://pypi.org/project/pygame-ce/)


## Trivia
1. This program originated from an idea of mine at the end of July of 2026, I had many exams to take but the excuse to spend time making this was that it was *essential* for organizing my notes.
2. The name *tom* came to mind while thinking of the song title "tower of memories" by ivri.


# Development
The execution starts from `main.py` that applies `tom_serialization.py` to calculate the initial state of `tom_program.py`, a state machine that handles transitions between an *image board* implemented in `tom_board.py` and a *search query* implemented in `tom_search.py`.


## Upcoming features
* Improve the search box
* Image comments
* World grid
* Physical panning and zooming (momentum, viscousity and elasticity)
* Local and global rotation
* Image cropping
* Lazy scaling (only scale what is in scope)
* Image preview while searching


## Issues
* The cursor 'loses' the image if one drags to fast. The code looks like this
  ```python
  ...
  # If the mouse moves and the left button is pressed
  elif event.type == pg.MOUSEMOTION and event.buttons[0]:
  ...
  # If the mouse cursor is inside the image
  if self.pt_in_box(cur_proj, self.srf_pos[i], self.srf_size_on[i]):
      # Move the image by the mouse's relative displacement
      self.srf_pos[i].x += cam.lenabs(event.rel[0])
      self.srf_pos[i].y += cam.lenabs(event.rel[1])
  ```
  the *bug* originates from the fact that mouse cursor check is done before the displacement, a possible fix is for the cursor check to happen with respect to the final position of the image instead.
* The gaussian blur implementation `pg.transform.gaussian_blur` is painfully slow.
* Elements outside of the scope still get rescaled, the performance is terrible.


## Methods

### Fixed point scaling
Given a change in camera `z`, which `X` should the camera be placed at such that a point `x` remains unchanged (primed variables indicate the transformed counterpart)?
```
(x/z + X) = (x'/z' + X') and x = x'
  => (x/z + X) = (x/z' + X')

X' = x/z - x/z' + X = x(1/z - 1/z') + X
   = x((z'-z)/zz') + X = = x(z'(1-z/z')/zz') + X
   = x((1-z/z')/z) + X

dz := z/z'
X' = x((1-z/z')/z) + X 
  => X += (1-dz)x/z
```
Therefore `(1-dz)x/z` will be the final camera offset that maintains the absolute position `x` constant. This is how I've implemented fixed point zooming.

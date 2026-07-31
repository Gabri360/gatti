# Introduction
Ideally this program's functionality will be limited to: *displaying*, *arranging*, *grouping*, and *commenting* images.

# Installation
1. Download this repository.
2. This python script requires the following package obtainable by `pip install pygame-ce`.
3. Run `python main.py`.

# Usage
1. Go to the "settings.json" file and set the root variable according to your environment.
2. Run the "main.py" file with a valid Python (version > 3.14.5) interpreter.
3. Extend the root path with keyboard input.
4. When the hints collapse to a single one press enter.
5. Repeat until encountering a valid image file, pressing enter will load the image.
6. You can move images by dragging them, you can scale images with by scrolling.
7. Remove images with `x` and screenshot the whole display with `s`.


# Patch Notes

## New
Remove images with `x`, screenshot with `s` has been removed.

## Upcoming
* Improve the search box.
* Image comments.
* World grid.
* Physical panning and zooming (momentum, viscousity and elasticity).
* Local and global rotation.

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
* When an image is clicked it's ordering is modified correctly but it gives an undesirable result for the rest of the images relative ordering.

# Trivia
* This program originated from an idea of mine at the end of July of 2026, I had many exams to take but the excuse to spend time making this was that it was *essential* for organizing my notes.
* The name *tom* came to mind while thinking of the song title "tower of memories" by ivri.

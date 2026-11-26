# Syndrome rectangles

The left assignment chooses the row syndrome A and the right assignment chooses the column syndrome B. The displayed code consists of the four pairs with A = B. Each matching block contains one point.

- **Diagonal** highlights the four true pairs.
- **Overlap** uses the column rectangle {00, 01} × {01} and the row rectangle {00} × {00, 01}. Both contain the false pair (00, 01), so it appears twice, while their union contains it once. Extra green diagonal cells identify code points outside the chosen rectangles.
- **Square** uses {00, 01} × {00, 01}. Two of its four cells are true, and its true block cap is one. The inequality t² ≤ L·|R| becomes 4 ≤ 4.

Extract the ZIP and open index.html. Choose a worked example, drag the matrix or use the rotation slider. The disclosure opens row and column selectors for a custom rectangle. The exact counts update below the plot.

Run `python3 visualization/render.py` with Pillow and Arial fonts to rebuild the GIF and ZIP. Set `Q515_FONT_DIR` to the folder containing Arial.ttf and Arial Bold.ttf if those files are elsewhere. The standard-library repository replay independently checks the displayed fixture.

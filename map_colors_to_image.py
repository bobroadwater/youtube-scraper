from PIL import Image
import numpy as np

mask = np.array(Image.open("masks/borders_neon.png"))
wc = np.array(Image.open("wordclouds/wc_emoji_clear_borders_2.png"))

for r in range(mask.shape[0]):
    for c in range(mask.shape[1]):
        if wc[r,c,3] != 0:
            wc[r,c,0:3] = mask[r,c,0:3]

im = Image.fromarray(wc, "RGBA")
im.save("wordclouds/wc_emoji_clear_borders_2_neon.png")
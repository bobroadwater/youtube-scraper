import os
import string
import random
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

# It is important to use io.open to correctly load the file as UTF-8
text = open('comments.txt', encoding='utf-8').read()

# the regex used to detect words is a combination of normal words, ascii art, and emojis
# 2+ consecutive letters (also include apostrophes), e.x It's
normal_word = r"(?:\w[\w']+)"
# 2+ consecutive punctuations, e.x. :)
ascii_art = r"(?:[{punctuation}][{punctuation}]+)".format(punctuation=string.punctuation)
# a single character that is not alpha_numeric or other ascii printable
emoji = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
# regexp = r"{normal_word}|{ascii_art}|{emoji}".format(normal_word=normal_word, ascii_art=ascii_art,
#                                                      emoji=emoji)
regexp = r"{ascii_art}|{emoji}".format(ascii_art=ascii_art, emoji=emoji)

mask = np.array(Image.open("masks/borders_neon.png"))

# Generate a word cloud image
# EmojiOne font https://github.com/13rac1/emojione-color-font#install-on-windows
wc = WordCloud(background_color=None, mode='RGBA', mask=mask, height=1080, width=1920,
               font_path='EmojiOneColor-SVGinOT.ttf', regexp=regexp).generate(text)

# wc.recolor(color_func=grey_color_func, random_state=3)
# image_colors = ImageColorGenerator(mask)
# wc.recolor(color_func=image_colors)

wc.to_file('wordclouds/wc_emoji_neon_clear_borders.png')
# import matplotlib.pyplot as plt
# plt.imshow(wc)
# plt.axis("off")
# plt.show()
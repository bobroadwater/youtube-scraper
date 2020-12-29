import os
import string
import random
from wordcloud import WordCloud

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

# Generate a word cloud image
# EmojiOne font https://github.com/13rac1/emojione-color-font#install-on-windows
wc = WordCloud(background_color=None, mode='RGBA', height=1080, width=1920, 
               font_path='EmojiOneColor-SVGinOT.ttf', regexp=regexp).generate(text)
# wc.recolor(color_func=grey_color_func, random_state=3)


wc.to_file('wc_emoji-color.png')
import matplotlib.pyplot as plt
plt.imshow(wc)
plt.axis("off")
plt.show()
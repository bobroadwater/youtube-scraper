from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

comments = open('comments.txt', encoding='utf-8').read()

# read the mask
logo_coloring = np.array(Image.open("pic_logo.png"))
stopwords = set(STOPWORDS)
stopwords.add("I")

# wc = WordCloud(background_color=None, mode="RGBA", max_words=2000, mask=logo_coloring,
#                stopwords=stopwords, max_font_size=40, random_state=42, scale=3)
wc = WordCloud(background_color=None,  mode='RGBA', max_words=2000, mask=logo_coloring,
               stopwords=stopwords, max_font_size=40, random_state=42, scale=3)
# generate word cloud
wc.generate(comments)

# create coloring from image
# image_colors = ImageColorGenerator(logo_coloring)
image_colors = ImageColorGenerator(np.array(Image.open("neon_stretch.png")))
wc.recolor(color_func=image_colors)

wc.to_file('wc_clear-neon_clear-bkg.png')
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.show()
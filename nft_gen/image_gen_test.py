try:
    from PIL import Image, ImageSequence
except ImportError:
    import Image
import json
import os

transparent_foreground = Image.open('Purple.png').convert('RGBA')
animated_gif = Image.open('background.gif')


frames = []
for frame in ImageSequence.Iterator(animated_gif):
    frame = frame.copy().convert('RGBA')
    frame.paste(transparent_foreground, mask=transparent_foreground)
    frames.append(frame)

print(len(frames))
frames[0].save('output.gif', save_all=True, append_images=frames[1:])
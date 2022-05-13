try:
    from PIL import Image, ImageSequence
except ImportError:
    import Image

overlay = Image.open('Purple.png').convert('RGBA')

width, height = overlay.size
print ('WxH: {}:{}'.format(width, height))

background = Image.open('background.gif')

width, height = background.size
print ('WxH: {}:{}'.format(width, height))

overlay = overlay.resize((width, height), Image.ANTIALIAS)

width, height = overlay.size
print ('WxH: {}:{}'.format(width, height))


frames = []
for frame in ImageSequence.Iterator(background):
    frame = frame.copy().convert('RGBA')
    frame.paste(overlay, mask=overlay)
    frames.append(frame)

print(len(frames))
frames[0].save('output.gif', save_all=True, append_images=frames[1:])
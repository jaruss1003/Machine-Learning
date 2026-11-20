from PIL import Image
import glob

files = sorted(glob.glob("spin_*.png"))
CROP = (184, 604, 1364, 1620)

frames = []
for f in files:
    im = Image.open(f).convert("RGB").crop(CROP)
    im = im.resize((900, 775), Image.LANCZOS)
    frames.append(im)

palette = frames[0].quantize(colors=256, method=Image.MEDIANCUT)
qframes = [fr.quantize(palette=palette, dither=Image.FLOYDSTEINBERG) for fr in frames]
qframes[0].save("055_compare_spin.gif", save_all=True,
                append_images=qframes[1:], duration=67, loop=0)
print("saved", len(qframes), "frames")

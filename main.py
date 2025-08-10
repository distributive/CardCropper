from pathlib import Path
from PIL import Image
import os

################################################################################

SIZES = (
    # NRDB
    ("nrdb", "small_", 51, 71, "jpeg"),
    ("nrdb", "medium_", 116, 162, "jpeg"),
    ("nrdb", "large_", 165, 230, "jpeg"),
    ("nrdb", "xlarge_", 300, 418, "jpeg"),

    # JNet
    ("jnet", "standard_", 452, 632, "png"),
    ("jnet", "high_", 731, 1037, "png"),

    # Creator resource portal
    ("creator", "", 1500, 2100, "png"),
)

################################################################################

def main():
    rawMask = Image.open("./mask.png").convert("RGBA")
    directory = "./source"
    for filename in os.listdir(directory):
        filestem = Path(filename).stem
        # Get each image
        file = os.path.join(directory, filename)
        img = Image.open(file).convert("RGB")
        width, height = img.size
        # Crop the image
        cropX = 0.0444305381727 * width
        cropY = 0.0317533364013 * height
        cropped = img.crop((cropX, cropY, width - cropX, height - cropY))
        # Cut the corners
        mask = rawMask.resize((cropped.size[0], cropped.size[1])).split()[-1]
        masked = cropped.convert("RGBA")
        masked.putalpha(mask)
        # Resize
        for folder, prefix, w, h, format in SIZES:
            imgOut = cropped if format == "jpeg" else masked
            imgOut.resize((w,h)).save("./out/" + folder + "/" + prefix + filestem + "." + format, format=format)

################################################################################

if (__name__ == "__main__"):
    main()

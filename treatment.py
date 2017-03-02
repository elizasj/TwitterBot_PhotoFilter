import os
from PIL import Image as PIL_Image
from PIL import ImageColor
from PIL import ImageOps
from wand.image import Image


def image_treatment(filename, target_size=(1080, 1080)):

    with PIL_Image.open(filename) as img:
        # check for min required size
        imageWidth, imageHeight = img.size
        if imageWidth < target_size[0] or imageHeight < target_size[1]:
            raise ValueError("Your picture needs to be at least 1080x1080.")

        centerWidth = int(imageWidth / 2)
        centerHeight = int(imageHeight / 2)

        x1 = centerWidth - (540)
        y1 = centerHeight - (540)
        x2 = centerWidth + (540)
        y2 = centerHeight + (540)

        # crop
        cropstep = img.crop((x1, y1, x2, y2))
        cropped_image = "crop-{}".format(filename)
        cropstep.save(cropped_image)

    # filter
    with Image(filename=cropped_image) as img:
        img.level(black=0, white=1.5, gamma=1.375, channel='composite_channels')
        img.modulate(brightness=100, saturation=190, hue=100)
        img.contrast_stretch(black_point=0.01, white_point=0.97, channel='composite_channels')
        processed_image = "processed-{}".format(filename)
        img.save(filename=processed_image)

    # add birds
    with PIL_Image.open(processed_image) as img:
        birds = PIL_Image.open("birds.png")
        img.paste(birds, (0, 0), birds)
        final_filename = "final-{}".format(filename)
        img.save(final_filename)

    os.remove(filename)
    os.remove(cropped_image)
    os.remove(processed_image)

    return final_filename

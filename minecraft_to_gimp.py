#!/usr/bin/python
# https://www.gimp.org/docs/python/index.html

import sys

from gimpfu import *

DEBUG = False

def minecraft_to_gimp(current_image, current_layer, frametime):
    # Redirect stdout and stderr to a file for debugging
    if DEBUG:
        # By necessity, __file__ will be in the gimp plugins directory in order
        # for this to be run in GIMP.
        sys.stdout = open(__file__ + '.stdout', 'w+')
        sys.stderr = open(__file__ + '.stderr', 'w+')
    def cleanup():
        pdb.gimp_progress_end()
        if DEBUG:
            sys.stdout.close()
            sys.stderr.close()

    # Compute how many milliseconds between each frame from the frametime.
    ms = round(1000 / (20 / frametime))
    print('Computed %d ms between each frame' % ms)

    # Compute the frame count from the input Minecraft texture
    width, height = current_layer.width, current_layer.height
    if height % width != 0:
        gimp.message('Image height is not divisible by width.')
        cleanup()
        return
    frames = height / width
    print('Converting %s to a GIMP image with %d frames' % (
        current_image.name, frames))

    # Create a new image for separating each frame into its own layer.
    image = gimp.Image(width, width, RGB)
    for i, height_offset in enumerate(range(0, height, width)):
        layer = pdb.gimp_layer_new_from_visible(
            current_image, image, "Layer %d (%d ms)" % (i, ms))
        # Add the layer to the image
        image.add_layer(layer)
        # Resize the layer, positioning the width-sized window at the
        # appropriate frame.
        layer.resize(width, width, 0, -height_offset)
        # Move the layer up to overlap back over the image bounds.
        layer.translate(0, -height_offset)
    gimp.Display(image)
    gimp.displays_flush()
    cleanup()

register(
    "minecraft_to_gimp", # name
    "Minecraft to GIMP", # blurb
    "Converts a Minecraft animated texture to GIMP layers", # help
    "omgimanerd", # author
    "omgimanerd", # copyright
    "2024", # date
    "<Image>/Filters/Minecraft/Minecraft to GIMP", # menupath
    "*", # imagetypes
    [
        (PF_INT8, 'frametime', 'How many ticks each frame will last', 1)
    ], # params
    [], # results
    minecraft_to_gimp)

main()

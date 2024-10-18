#!/usr/bin/python
# https://www.gimp.org/docs/python/index.html

import math
import sys

from gimpfu import *

DEBUG = False

def gimp_to_minecraft(current_image, current_layer):
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

    # Check if the input image has valid dimensions
    width, height = current_image.width, current_image.height
    if width != height:
        gimp.message('Image width is not the same as its height.')
        cleanup()
        return
    log = math.log(width, 2)
    if int(log) != log:
        gimp.message('Image dimensions are not a power of 2.')
        cleanup()
        return
    if len(current_image.layers) == 1:
        gimp.message('Current image only has one layer.')
        cleanup()
        return

    # Minecraft animated texture is the result of stacking the layers
    # vertically.
    image = gimp.Image(width, width * len(current_image.layers))
    # Layers are returned from top to bottom, so reverse them for placement.
    for i, layer in enumerate(reversed(current_image.layers)):
        # Check that the layer dimensions are the same as the image
        if layer.width != width or layer.height != height:
            gimp.message('%s dimensions do not match image!' % layer.name)
            cleanup()
            return
        # Copy the layer to the output image at the right offset.
        copy = pdb.gimp_layer_new_from_drawable(layer, image)
        image.add_layer(copy)
        copy.translate(0, height * i)
    # Merge all the visible layers
    pdb.gimp_image_merge_visible_layers(image, 0) # EXPAND-AS-NECESSARY
    gimp.Display(image)
    gimp.displays_flush()
    gimp.delete(image)

    gimp.message(
        'Successfully converted %s into a Minecraft animated texture.' %
        (current_image.name))
    cleanup()

register(
    "gimp_to_minecraft", # name
    "GIMP to Minecraft", # blurb
    "Converts a series of GIMP layers to Minecraft's animated texture", # help
    "omgimanerd", # author
    "omgimanerd", # copyright
    "2024", # date
    "<Image>/Filters/Minecraft/GIMP to Minecraft", # menupath
    "*", # imagetypes
    [], # params
    [], # results
    gimp_to_minecraft)

main()

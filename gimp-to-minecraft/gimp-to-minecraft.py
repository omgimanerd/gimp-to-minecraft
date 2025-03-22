#!/usr/bin/env python3
# gimp-to-minecraft converts a GIMP animated image with stacked layers into
# the Minecraft animated texture format by stacking the layers vertically into
# a single image.

from typing import override

import math
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../gimp-minecraft-bridge-lib'))

from gimp_minecraft_bridge_lib import GimpMinecraftBridgePlugin

import gi

gi.require_version('Gimp', '3.0')

from gi.repository import Gimp, GLib

class GimpToMinecraft(GimpMinecraftBridgePlugin):
  def __init__(self):
    super().__init__(
      name='gimp-to-minecraft',
      menu_label='GIMP to Minecraft',
      menu_path='<Image>/Filters/Minecraft',
      debug=False
    )

  @override
  def run(self, procedure, run_mode, current_image, drawables, config,
          run_data):
    def error(s):
      return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR,
                                         GLib.Error(s))

    # Check the dimensions of the input image.
    width, height = current_image.get_width(), current_image.get_height()
    if width != height:
      self.cleanup()
      return error('Image width is not the same as its height.')
    log = math.log(width, 2)
    if int(log) != log:
      self.cleanup()
      return error('Image dimensions are not a power of 2.')
    layers = current_image.get_layers()
    if len(layers) == 1:
      self.cleanup()
      return error('Image only has one layer.')

    # Stack all the layers vertically into a new image.
    image = Gimp.Image.new(width, width * len(layers),
                           current_image.get_base_type())
    for i, layer in enumerate(reversed(layers)):
      if layer.get_width() != width or layer.get_height() != height:
        self.cleanup()
        return error(f'Layer {layer.get_name()} dimensions do not match image.')
      # Copy the layer to the output image at the right offset
      copy = Gimp.Layer.new_from_drawable(layer, image)
      image.insert_layer(copy, None, 0)
      copy.transform_translate(0, height * i)
      copy.set_visible(True)
    # Merge all the visible layers into a single layer
    layer = image.merge_visible_layers(Gimp.MergeType.EXPAND_AS_NECESSARY)
    layer.set_name('minecraft-texture')

    Gimp.Display.new(image)
    Gimp.displays_flush()

    self.cleanup()
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

Gimp.main(GimpToMinecraft.__gtype__, sys.argv)

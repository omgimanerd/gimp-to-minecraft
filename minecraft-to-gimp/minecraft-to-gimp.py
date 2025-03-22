#!/usr/bin/python
# minecraft-to-gimp converts a Minecraft animated texture into a GIMP animated
# image by slicing the vertically stacked textures into layers within GIMP.

from typing import override

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../gimp-minecraft-bridge-lib'))

from gimp_minecraft_bridge_lib import GimpMinecraftBridgePlugin

import gi

gi.require_version('Gimp', '3.0')

from gi.repository import Gimp, GLib

class MinecraftToGimp(GimpMinecraftBridgePlugin):
  def __init__(self):
    super().__init__(
      name='minecraft-to-gimp',
      menu_label='Minecraft to GIMP',
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
    if height % width != 0:
      self.cleanup()
      return error('Image height is not divisible by its width.')

    # Create a new image for separating each frame into its own layer.
    image = Gimp.Image.new(width, width, current_image.get_base_type())
    for i, height_offset in enumerate(range(0, height, width)):
      layer = Gimp.Layer.new_from_visible(current_image, image, f'Frame {i}')
      image.insert_layer(layer, None, 0)
      layer.resize(width, width, 0, -height_offset)
      layer.transform_translate(0, -height_offset)

    Gimp.Display.new(image)
    Gimp.displays_flush()

    self.cleanup()
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

Gimp.main(MinecraftToGimp.__gtype__, sys.argv)

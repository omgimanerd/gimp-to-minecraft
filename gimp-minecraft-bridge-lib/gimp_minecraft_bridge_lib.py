#!/usr/bin/env python3
# Library file shared by gimp-to-minecraft and minecraft-to-gimp plugins.
# In Gimp 3.0, the plugin executable must match the parent directory, so this
# will not be loaded as a plugin.

import sys

from typing import override

import gi

gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')

from gi.repository import Gimp

class GimpMinecraftBridgePlugin(Gimp.PlugIn):
    """Helper base class that gimp-to-minecraft and minecraft-to-gimp will
    inherit from.

    https://lazka.github.io/pgi-docs/#Gimp-3.0
    """

    def __init__(self, name='', menu_label='', menu_path='', documentation='',
                 debug=False):
        self._name = name
        self._menu_label = menu_label
        self._menu_path = menu_path
        self._documentation = documentation
        self._debug = debug
        if self._debug:
            sys.stdout = open(f'{name}.stdout', 'w+')
            sys.stderr = open(f'{name}.stderr', 'w+')

    @override
    def do_query_procedures(self):
        return [self._name]

    @override
    def do_set_i18n(self, name):
        return False

    @override
    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN,
                                            self.run, None)
        procedure.set_image_types('*')
        procedure.set_menu_label(self._menu_label)
        procedure.add_menu_path(self._menu_path)
        procedure.set_documentation(self._documentation)
        procedure.set_attribution('omgimanerd', 'omgimanerd', '2025')
        return procedure

    def cleanup(self):
        if self._debug:
            sys.stdout.close()
            sys.stderr.close()

    def run(self, procedure, run_mode, current_image, drawables, config,
            run_data):
        raise NotImplementedError

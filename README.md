# gimp-minecraft-bridge

The Python-Fu plugins here are used in GIMP 3.0 to convert between Minecraft's
animated textures and a layered image that is easier to work with in GIMP.

## Installation

Find your GIMP plug-ins directory. You can see the directory by opening
`Edit > Preferences > Folders > Plug-ins`.

On Windows, there will usually be two paths that look something like:
```
C:/Users/USER/AppData/Roaming/GIMP/3.0/plug-ins
C:/Users/USER/AppData/Local/Programs/GIMP 3/lib/gimp/3.0/plug-ins
```
Either of them of will work.

If you are lazy, you can simply clone this project into the `plug-ins`
directory.
```
cd path/to/GIMP/3.0/plug-ins

git clone git@github.com:omgimanerd/gimp-to-minecraft .
```
This will put the rest of the project crap in the directory though.

Alternatively, you can use the installer script.
```
cd path/to/GIMP/3.0/plug-ins

curl https://raw.githubusercontent.com/omgimanerd/gimp-minecraft-bridge/refs/heads/gimp-3.0/install.sh | bash
```

## Usage

Once you've copied the scripts into your plugins directory, they are available
under the Filters menu:

![Filters > Minecraft](png/menu.png)

I have them bound to keyboard shortcuts for ease of use, which you can do under
`Edit > Keyboard Shortcuts`

Invoke the `Minecraft to GIMP` script on a Minecraft style animated texture
will slice the texture into layers which you can then edit and preview using
GIMP's animation tooling. `GIMP to Minecraft` does the opposite to stack the
image layers back into the Minecraft animated texture format.

### Example:

![Example](png/example.png)

Using AE2's singularity texture as an example, invoking the script on the left
image generates the image on the right, with each frame sliced into layers.
You can then use `Filters > Animation > Playback` to preview the animation, and
each frame becomes its own separate layer for editing. Once you're done editing
the individual layers, you can use `GIMP to Minecraft` to convert it back into
the Minecraft format.

## Author
omgimanerd

# Gwyddion-Utils
This project is to provide a SPM data browser for fast image reviewing and saving (like Nanonis Scan Inspector). It is based on [Gwyddion](http://gwyddion.net/), using the Gwyddion python API.

It can be used independently as GUI to browse SPM image data, or started as a
function in Gwyddion.

Its biggest advantage is the fast review of the SPM data and fast saving
function.

Currently, it can handle Nanonis .sxm file and Omicron .mtrx file.

## Usage
### Use as independent GUI
To use it independently, you need to have Gwyddion installed with pygwy.

You need to be able to use the gwyddion outside Gwyddion software by `import gwy`.

Then you can simply run the SPMBrowser.py in **GwyBrowser/gwybrowser**.

### Use within the Gwyddion
To use it within the Gwyddion, you need to have Gwyddion installed with pygwy.

For the python part, you need pygtk, numpy, matplotlib and re.

Put the pygwy, ui and icon folders inside the **GwyBrowser** to the ~/.gwyddion file.

# dxfsnap
Simple script to round coordinates of a DXF file.

The targeted use case is to snap points to a grid, typically after entities in
file have been scaled and went off grid.

Thanks to the structure of DXF files, the script is also very simple. Maybe too
simple? Tell me if you encounter problems.

Does not work with binary DXF.
Does not handle entities defined by an angle.

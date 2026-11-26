# Creality Print slicing attempt

Creality Print 7.2 was invoked with its documented command-line form (`--slice 0 --outputdir <dir> --logfile <file> <project.3mf>`) for both the Prototype 03 Revision 02 and Prototype 04 projects. The executable launched a GUI process instead of completing headless slicing. No G-code, slice log, or filament/time metadata was produced. The launched processes were closed; pre-existing Creality Print sessions were not touched. No package or third-party slicer was installed.

Therefore there are no actual sliced toolpaths to inspect and no actual sliced-mass comparison to report. CAD volume alone is not being used as a substitute for sliced filament mass.

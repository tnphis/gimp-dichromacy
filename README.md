## gimp-dichromacy
Multimodel color blindness simulation plugins for GIMP using Python-Fu.
Put the .py files in your /*user home*/.gimp-2.x/plug-ins directory.
Only 8 bit per channel rgb images are supported. If GIMP ever supports 16 bit per channel, this plugin will likely crash due to low-level ops that assume the bpp to be fixed.

This gimp plugin simulates color blindness using the well-known Brettel et. al. model and a more recently developed physiological model by Gustavo M. Machado, Manuel M. Oliveira, and Leandro A. F. Fernandes ([link](http://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html)).

Since math calculations are rather slow in Python, and pixel-level operations are required, a parallel version (using multiprocessor library) has been developed for use on multi-core systems. The single thread version is only recommended for single-core systems.

The Brettel model calculations are based on the data obtained from the color space articles on wikipedia and [http://cvrl.ioo.ucl.ac.uk/cie.htm](http://cvrl.ioo.ucl.ac.uk/cie.htm) (details in the code comments).
In the resulting images, the yellows are marginally shifted towards orange in comparison to Vischeck, another well-known Brettel model implementation, but this difference is not significant enough to look like an error, especially, given the luminosity similarities.
It can probably be explained by slightly different calibration (the xyz-lms matrix or rgb color space).
Both, sRGB and Adobe RGB color spaces can be used for this model.

The physiological model matrices are pre-calculated by the researchers, and I have not tried to reproduce the results myself. Judging by the appearance, they used the same calibration as Vischeck which seems to be close enough to the sRGB color space. Thus, selecting Adobe RGB is not going to make any difference for this method.

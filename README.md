## gimp-dichromacy
Multimodel color blindness simulation plugins for GIMP using Python-Fu.
Put the .py files in your /*user home*/.gimp-2.x/plug-ins directory.
Only 8 bit per channel rgb images are supported. If GIMP ever supports 16 bit per channel, this plugin will likely crash due to low-level ops that assume the bpp to be fixed.

This gimp plugin simulates color blindness using the well-known Brettel et. al. model and a more recently developed physiological model by Gustavo M. Machado, Manuel M. Oliveira, and Leandro A. F. Fernandes ([link](http://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html)).

Since math calculations are rather slow in Python, and pixel-level operations are required, a parallel version (using multiprocessor library) has been developed for use on multi-core systems. The single thread version is only recommended for single-core systems.

The Brettel model calculations are based on the data obtained from [http://en.wikipedia.org/wiki/LMS_color_space](http://en.wikipedia.org/wiki/LMS_color_space), [http://en.wikipedia.org/wiki/SRGB](http://en.wikipedia.org/wiki/SRGB), [http://en.wikipedia.org/wiki/Adobe_RGB_color_space](http://en.wikipedia.org/wiki/Adobe_RGB_color_space) and [http://cvrl.ioo.ucl.ac.uk](http://cvrl.ioo.ucl.ac.uk) (details in the code comments).
4 different transformation types and anchor point values are available: the CIE standard + von Kries XYZ -> LMS transformation, "spectrally sharpened" CIECAM02, CRT primaries used by Vischeck and GIMP (using those should reproduce the GIMP display filters when the gamma correction but is fixed and be close to Vischeck although not quite the same since they use the gamma value of 2.0) and CVRL-proposed transformations based on the cone fundamentals obtained in their research.
Both, sRGB and Adobe RGB color spaces can be used for this model as long as CIE or CVRL transformations are used.

The physiological model matrices are pre-calculated by the researchers, and I have not tried to reproduce the results myself. Judging by the appearance, they used the same calibration as Vischeck (CRT primaries). These primaries are not exactly the same as the sRGB but it shouldn't be critical given that most monitors don't reproduce sRGB exactly. Thus, the color space selection is meaningless for this method (same values are used for both choices).

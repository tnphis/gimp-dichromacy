from __future__ import division

from gimpfu import *
import multiprocessing
from array import array

#RGB to R'G'B' matrices for the physiological model.
#Based on the research by Gustavo M. Machado, Manuel M. Oliveira, and Leandro A. F. Fernandes
#(http://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html)
#mentioned in another plugin (http://registry.gimp.org/node/24885).
#The matrices are pre-calculated by the researchers and I have not tried to reproduce the results myself (might do it at some unspecified point in the future).
#Judging by the appearance, they used the same calibration as the Vischeck (CRT Primaries).
#These primaries are not exactly the same as the sRGB but it shouldn't be critical given that most monitors don't reproduce sRGB exactly.
#protanomaly, deuteranomaly, tritanomaly for responsivity shifts @ 2nm steps.
physio_model_matrices = [[ #2nm
		[[0.856167, 0.182038, -0.038205]
		,[0.029342, 0.955115, 0.015544]
		,[-0.002880, -0.001563, 1.004443]
		]
		,

		[[0.866435, 0.177704, -0.044139]
		,[0.049567, 0.939063, 0.011370]
		,[-0.003453, 0.007233, 0.996220]
		]
		,

		[[0.926670, 0.092514, -0.019184]
		,[0.021191, 0.964503, 0.014306]
		,[0.008437, 0.054813, 0.936750]
		]
	],[ #4nm
		[[0.734766, 0.334872, -0.069637]
		,[0.051840, 0.919198, 0.028963]
		,[-0.004928, -0.004209, 1.009137]
		]
		,

		[[0.760729, 0.319078, -0.079807]
		,[0.090568, 0.889315, 0.020117]
		,[-0.006027, 0.013325, 0.992702]
		]
		,

		[[0.895720, 0.133330, -0.029050]
		,[0.029997, 0.945400, 0.024603]
		,[0.013027, 0.104707, 0.882266]
		]
	],[ #6nm
		[[0.630323, 0.465641, -0.095964]
		,[0.069181, 0.890046, 0.040773]
		,[-0.006308, -0.007724, 1.014032]
		]
		,

		[[0.675425, 0.433850, -0.109275]
		,[0.125303, 0.847755, 0.026942]
		,[-0.007950, 0.018572, 0.989378]
		]
		,

		[[0.905871, 0.127791, -0.033662]
		,[0.026856, 0.941251, 0.031893]
		,[0.013410, 0.148296, 0.838294]
		]
	],[ #8nm
		[[0.539009, 0.579343, -0.118352]
		,[0.082546, 0.866121, 0.051332]
		,[-0.007136, -0.011959, 1.019095]
		]
		,

		[[0.605511, 0.528560, -0.134071]
		,[0.155318, 0.812366, 0.032316]
		,[-0.009376, 0.023176, 0.986200]
		]
		,

		[[0.948035, 0.089490, -0.037526]
		,[0.014364, 0.946792, 0.038844]
		,[0.010853, 0.193991, 0.795156]
		]
	],[ #10nm
		[[0.458064, 0.679578, -0.137642]
		,[0.092785, 0.846313, 0.060902]
		,[-0.007494, -0.016807, 1.024301]
		]
		,

		[[0.547494, 0.607765, -0.155259]
		,[0.181692, 0.781742, 0.036566]
		,[-0.010410, 0.027275, 0.983136]
		]
		,

		[[1.017277, 0.027029, -0.044306]
		,[-0.006113, 0.958479, 0.047634]
		,[0.006379, 0.248708, 0.744913]
		]
	],[ #12nm
		[[0.385450, 0.769005, -0.154455]
		,[0.100526, 0.829802, 0.069673]
		,[-0.007442, -0.022190, 1.029632]
		]
		,

		[[0.498864, 0.674741, -0.173604]
		,[0.205199, 0.754872, 0.039929]
		,[-0.011131, 0.030969, 0.980162]
		]
		,

		[[1.104996, -0.046633, -0.058363]
		,[-0.032137, 0.971635, 0.060503]
		,[0.001336, 0.317922, 0.680742]
		]
	],[ #14nm
		[[0.319627, 0.849633, -0.169261]
		,[0.106241, 0.815969, 0.077790]
		,[-0.007025, -0.028051, 1.035076]
		]
		,

		[[0.457771, 0.731899, -0.189670]
		,[0.226409, 0.731012, 0.042579]
		,[-0.011595, 0.034333, 0.977261]
		]
		,

		[[1.193214, -0.109812, -0.083402]
		,[-0.058496, 0.979410, 0.079086]
		,[-0.002346, 0.403492, 0.598854]
		]
	],[ #16nm
		[[0.259411, 0.923008, -0.182420]
		,[0.110296, 0.804340, 0.085364]
		,[-0.006276, -0.034346, 1.040622]
		]
		,

		[[0.422823, 0.781057, -0.203881]
		,[0.245752, 0.709602, 0.044646]
		,[-0.011843, 0.037423, 0.974421]
		]
		,

		[[1.257728, -0.139648, -0.118081]
		,[-0.078003, 0.975409, 0.102594]
		,[-0.003316, 0.501214, 0.502102]
		]
	],[ #18nm
		[[0.203876, 0.990338, -0.194214]
		,[0.112975, 0.794542, 0.092483]
		,[-0.005222, -0.041043, 1.046265]
		]
		,

		[[0.392952, 0.823610, -0.216562]
		,[0.263559, 0.690210, 0.046232]
		,[-0.011910, 0.040281, 0.971630]
		]
		,

		[[1.278864, -0.125333, -0.153531]
		,[-0.084748, 0.957674, 0.127074]
		,[-0.000989, 0.601151, 0.399838]
		]
	],[ #20nm
		[[0.152286, 1.052583, -0.204868]
		,[0.114503, 0.786281, 0.099216]
		,[-0.003882, -0.048116, 1.051998]
		]
		,

		[[0.367322, 0.860646, -0.227968]
		,[0.280085, 0.672501, 0.047413]
		,[-0.011820, 0.042940, 0.968881]
		]
		,

		[[1.255528, -0.076749, -0.178779]
		,[-0.078411, 0.930809, 0.147602]
		,[0.004733, 0.691367, 0.303900]
		]
	]]

f_rec_24 = 1 / 2.4
f_pow_22 = 563 / 256
f_rec_22 = 256 / 563

#Vector ops, quick, dirty and non-generic
def vproduct3d(p_matrix, p_vector):
	#every new number assignment involves a new object creation in py.
	#therefore, just do it in one step.
	return [
		p_matrix[0][0] * p_vector[0] + p_matrix[0][1] * p_vector[1] + p_matrix[0][2] * p_vector[2],
		p_matrix[1][0] * p_vector[0] + p_matrix[1][1] * p_vector[1] + p_matrix[1][2] * p_vector[2],
		p_matrix[2][0] * p_vector[0] + p_matrix[2][1] * p_vector[1] + p_matrix[2][2] * p_vector[2]
	]

def mproduct3d(m1, m2):
	l_rslt = [[0,0,0],[0,0,0],[0,0,0]]
	for x in range(0,3):
		for y in range(0,3):
			l_rslt[x][y] = m1[x][0] * m2[0][y] + m1[x][1] * m2[1][y] + m1[x][2] * m2[2][y]

	return l_rslt

def det3d(m):
	return (m[0][0] * m[1][1] * m[2][2] + m[0][1]*m[1][2]*m[2][0] + m[0][2]*m[1][0]*m[2][1]) - (m[2][0]*m[1][1]*m[0][2] + m[2][1]*m[1][2]*m[0][0] + m[2][2]*m[1][0]*m[0][1])

def minverse3d(m):
	l_rslt = [[0,0,0],[0,0,0],[0,0,0]]

	l_rslt[0][0] = (m[1][1] * m[2][2] - m[1][2] * m[2][1]) / det3d(m)
	l_rslt[0][1] = (m[0][2] * m[2][1] - m[0][1] * m[2][2]) / det3d(m)
	l_rslt[0][2] = (m[0][1] * m[1][2] - m[0][2] * m[1][1]) / det3d(m)
	l_rslt[1][0] = (m[1][2] * m[2][0] - m[1][0] * m[2][2]) / det3d(m)
	l_rslt[1][1] = (m[0][0] * m[2][2] - m[0][2] * m[2][0]) / det3d(m)
	l_rslt[1][2] = (m[0][2] * m[1][0] - m[0][0] * m[1][2]) / det3d(m)
	l_rslt[2][0] = (m[1][0] * m[2][1] - m[1][1] * m[2][0]) / det3d(m)
	l_rslt[2][1] = (m[0][1] * m[2][0] - m[0][0] * m[2][1]) / det3d(m)
	l_rslt[2][2] = (m[0][0] * m[1][1] - m[0][1] * m[1][0]) / det3d(m)

	return l_rslt

#The transformation matrices.
#There are 3 possible transformations: CIE standard (default), CRT primaries (obtained from the GIMP source, transforms rgb to lms directly)
#and transformations using the cone responsivity functions proposed by CVRL at http://cvrl.ioo.ucl.ac.uk/
#The RGB->XYZ matrices are parts of the standards and
#are obtained directly from wikipedia (http://en.wikipedia.org/wiki/SRGB, http://en.wikipedia.org/wiki/Adobe_RGB_color_space).
#For the default CIE XYZ to LMS the von Kries and the "spectrally sharpened" CIECAM02 matrices from http://en.wikipedia.org/wiki/LMS_color_space are available.
#The pre-normalized D65 version is used for convenience and reduction of the number of math ops per pixel.
l_srgb_to_xyz = [[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]
l_argb_to_xyz = [[0.57667, 0.18556, 0.18823], [0.29734, 0.62736, 0.07529], [0.02703, 0.07069, 0.99134]]
#standard D65 normalized von Kries matrix
l_xyz_to_lms_std = [[0.4002, 0.7076, -0.0808], [-0.2263, 1.1653, 0.0457], [0, 0, 0.9182]]
#CIECAM02 normalized
l_xyz_to_lms_ciecam02 = [[0.77196, 0.452557, -0.171078],[-0.67956, 1.63951, 0.00589],[0.002759, 0.0125072, 0.90438]]

#normalized matrix based on CVRL cone responsivity functions and their proposed xyz-lms transformation
l_xyz_to_lms_cvrl = [[0.208075059415457832,0.844942658420110809,-0.0392268157892593896], [-0.481356562461972489,1.35870646456651937,0.0907465087728057704], [0,0,0.918273645546372817]]

#pre-compute matrices
l_srgb_to_lms_std = mproduct3d(l_xyz_to_lms_std, l_srgb_to_xyz)
l_lms_to_srgb_std = minverse3d(l_srgb_to_lms_std)

l_argb_to_lms_std = mproduct3d(l_xyz_to_lms_std, l_argb_to_xyz)
l_lms_to_argb_std = minverse3d(l_argb_to_lms_std)

l_srgb_to_lms_cvrl = mproduct3d(l_xyz_to_lms_cvrl, l_srgb_to_xyz)
l_lms_to_srgb_cvrl = minverse3d(l_srgb_to_lms_cvrl)

l_argb_to_lms_cvrl = mproduct3d(l_xyz_to_lms_cvrl, l_argb_to_xyz)
l_lms_to_argb_cvrl = minverse3d(l_argb_to_lms_cvrl)

l_srgb_to_lms_ciecam02 = mproduct3d(l_xyz_to_lms_ciecam02, l_srgb_to_xyz)
l_lms_to_srgb_ciecam02 = minverse3d(l_srgb_to_lms_ciecam02)

l_argb_to_lms_ciecam02 = mproduct3d(l_xyz_to_lms_ciecam02, l_argb_to_xyz)
l_lms_to_argb_ciecam02 = minverse3d(l_argb_to_lms_ciecam02)

#the CRT Primaries. This matrix is used in the GIMP's display filters as well as vischeck plugins.
#This should exactly reproduce the GIMP display filters once the gamma correction bug is fixed.
#Vischeck uses a gamma of 2.0 for some reason, so, the results would be slightly different (and I see no need to reproduce them exactly).
#Like the CVRL version, this matrix is normalized to preserve grays (hence the difference from the original).
l_rgb_to_lms_crt = [[0.346627074323396749,0.588128722657128773,0.0652442030194744787],[0.155314378964580652,0.732279188523181272,0.112406432512238076],[0.0347284313493614684,0.115966495018429594,0.849305073632208941]]
l_lms_to_rgb_crt = minverse3d(l_rgb_to_lms_crt)

#Simulated primaries. Those are obtained by integrating the simulated gauss primaries over the cone sensitivities
l_srgb_to_lms_gauss = [[0.2728947482494285, 0.6541833404838804, 0.07292191126669095], [0.10077567453708611, 0.7746124282721973, 0.12461189719071666], [0.01738270643404226, 0.0916553175648222, 0.8909619760011355]]
l_lms_to_srgb_gauss = minverse3d(l_srgb_to_lms_gauss)

l_argb_to_lms_gauss = [[0.38236406650405713, 0.5417565993667248, 0.07587933412921799], [0.14140523181028158, 0.7287415112766454, 0.12985325691307292], [0.024309306361990635, 0.050357981546618226, 0.9253327120913911]]
l_lms_to_argb_gauss = minverse3d(l_argb_to_lms_gauss)

#Same stuff but for the ciecam02 "sharpened" cones.
l_srgb_to_lms_gauss02 = [[0.4050637434896599, 0.5723769181277797, 0.022559338382560624], [0.06973952110175391, 0.8655696559089129, 0.06469082298933329], [0.020770556755829978, 0.11582283084695165, 0.8634066123972184]]
l_lms_to_srgb_gauss02 = minverse3d(l_srgb_to_lms_gauss02)

l_argb_to_lms_gauss02 = [[0.567802342533737, 0.40871302645999746, 0.023484631006265713], [0.097401571785687, 0.835499859686826, 0.06709856852748701], [0.02911359996082812, 0.07212022994756716, 0.8987661700916048]]
l_lms_to_argb_gauss02 = minverse3d(l_argb_to_lms_gauss02)

#The transformations combined. List dimensions: transformation type, color space
l_brettel_transforms = [
	[ #CIE standard (von Kries)
		{
			'rgbtolms' : l_srgb_to_lms_std,
			'lmstorgb' : l_lms_to_srgb_std
		},
		{
			'rgbtolms' : l_argb_to_lms_std,
			'lmstorgb' : l_lms_to_argb_std
		}
	],
	[ #CIECAM02
		{
			'rgbtolms' : l_srgb_to_lms_ciecam02,
			'lmstorgb' : l_lms_to_srgb_ciecam02
		},
		{
			'rgbtolms' : l_argb_to_lms_ciecam02,
			'lmstorgb' : l_lms_to_argb_ciecam02
		}
	],
	[ #CRT primaries
		{
			'rgbtolms' : l_rgb_to_lms_crt,
			'lmstorgb' : l_lms_to_rgb_crt
		},
		{
			'rgbtolms' : l_rgb_to_lms_crt,
			'lmstorgb' : l_lms_to_rgb_crt
		}
	],
	[ #CVRL proposed version
		{
			'rgbtolms' : l_srgb_to_lms_cvrl,
			'lmstorgb' : l_lms_to_srgb_cvrl
		},
		{
			'rgbtolms' : l_argb_to_lms_cvrl,
			'lmstorgb' : l_lms_to_argb_cvrl
		}
	],
	[ #Simulated primaries (normal cones)
		{
			'rgbtolms' : l_srgb_to_lms_gauss,
			'lmstorgb' : l_lms_to_srgb_gauss
		},
		{
			'rgbtolms' : l_argb_to_lms_gauss,
			'lmstorgb' : l_lms_to_argb_gauss
		}
	],
	[ #Simulated primaries (ciecam02 "sharpened" cones)
		{
			'rgbtolms' : l_srgb_to_lms_gauss02,
			'lmstorgb' : l_lms_to_srgb_gauss02,
		},
		{
			'rgbtolms' : l_argb_to_lms_gauss02,
			'lmstorgb' : l_lms_to_argb_gauss02
		}
	]
]

#The LMS coordinates of the spectral colors for the Brettel color model, standard CIE version.
#The XYZ coordinates are obtained from http://cvrl.ioo.ucl.ac.uk/cie.htm and converted to LMS using the matrix above.
#These values don NOT need to stay within the gamut, the projection takes care of it, as stated in the research paper.
l_xyz_coeffs_std = {
	475 : [0.1421, 0.1126, 1.0419],
	485 : [0.05795, 0.1693, 0.6162],
	575 : [0.8425, 0.9154, 0.0018],
	660 : [0.1649, 0.061, 0]
}

l_lms_coeffs_std = {}
l_lms_coeffs_ciecam02 = {}
for l, coeff in l_xyz_coeffs_std.iteritems():
	l_lms_coeffs_std[l] = vproduct3d(l_xyz_to_lms_std, coeff)
	l_lms_coeffs_ciecam02[l] = vproduct3d(l_xyz_to_lms_ciecam02, coeff)

#Combined anchor coefficients list (by model). By transformation type.
#The RGB primaries version is obtained from GIMP source.
#The CVRL version is obtained directly from the responsivity charts at cvrl.ioo.ucl.ac.uk.
#Both the primaries and the CVRL coefficients are adjusted for the LMS transformation normalization,
#hence the differences from the source.

#the original values for reference
#{
#	475 : [0.118802, 0.205398,	0.516411],
#	485 : [0.163952, 0.268063,	0.290322],
#	575 : [0.99231, 0.740291, 0.00017504],
#	660 : [0.0930085, 0.00730255, 0]
#}

#red:
#srgb normal: {0.101653953058952029,0.140286938872420523,0.849078585881792289,0.0795835229464448389}
#argb normal: {0.101507095554895532,0.140084269039378397,0.847851938436039675,0.079468550166811174}
#srgb cam: {0.104505827138756821,0.14422265089016564,0.872899255299235547,0.0818162170959669351}
#argb cam: {0.104888363722905241,0.144750568248832175,0.876094444587432025,0.082115699881498898}

#blue
#srgb normal: {0.827244078668466425,0.465069790161686156,0.000280398371704182062}
#argb normal: {0.824478004737193004,0.463514726238037817,0.000279460797599583013}
#srgb cam: {0.655300896103247846,0.368404752723096761,0.000222117400392153736}
#argb cam: {0.65766015371847254,0.369731107873097949,0.000222917082143644178}

l_lms_coeffs_combined = [
	#CIE standard
	l_lms_coeffs_std,
	l_lms_coeffs_ciecam02,
	{ #CRT Primaries
		475 : [0.548577, 1.295495, 7.00863],
		485 : [0.879586, 1.835352, 4.321414],
		575 : [6.751715, 6.009815, 0.012824],
		660 : [0.626123, 0.0575055, 0.0]
	},
	{ #CVRL
		475 : [0.185767, 0.23705678, 0.9175],
		485 : [0.1620026, 0.3093741, 0.5158188],
		575 : [0.98051357, 0.85439695, 0.000310927],
		660 : [0.091895, 0.084251, 0.0]
	},
	[ #Simulated primaries - those are color-space dependent, if only marginally.
		{
			475 : [0.101654, 0.205398, 0.827244],
			485 : [0.140287, 0.268063,	0.46507],
			575 : [0.84908, 0.740291, 0.0002804],
			660 : [0.0795835, 0.00730255, 0]
		},
		{
			475 : [0.1015071, 0.205398, 0.824478],
			485 : [0.140084, 0.268063,	0.4635147],
			575 : [0.847852, 0.740291, 0.00027946],
			660 : [0.07946855, 0.00730255, 0]
		}
	],
	[ #Simulated primaries, sharpened cones.
		{
			475 : [0.104506, 0.205398, 0.6553],
			485 : [0.14422265, 0.268063,	0.36973],
			575 : [0.8729, 0.740291, 0.0002221174],
			660 : [0.081816, 0.00730255, 0]
		},
		{
			475 : [0.104888, 0.205398, 0.65766],
			485 : [0.14475, 0.268063,	0.3697311],
			575 : [0.8761, 0.740291, 0.000222917],
			660 : [0.0821157, 0.00730255, 0]
		}
	]
]

def get_coeff(p_vect, p_coeff):
	if p_coeff == 'a':
		return p_vect[2] - p_vect[1]
	elif p_coeff == 'b':
		return p_vect[0] - p_vect[2]
	elif p_coeff == 'c':
		return p_vect[1] - p_vect[0]

#standard sRGB and aRGB gamma correction procedures
def linearize_srgb_value(p_val):
	if p_val <= 10:
		return p_val / 12.92
	else:
		return ((p_val + 14.025) / 1.055)**2.4

def delinearize_srgb_value(p_val):
	if p_val < 0.798355:
		i_return_value = int(round(12.92 * p_val))
	else:
		i_return_value = int(round(1.055 * p_val**(1/2.4) - 14.025))

	if i_return_value < 256 and i_return_value >= 0:
		return i_return_value
	elif i_return_value > 255:
		return 255
	elif i_return_value < 0:
		return 0

def linearize_argb_value(p_val):
	return (p_val) ** (563 / 256)

def delinearize_argb_value(p_val):
	if p_val >= 0:
		i_return_value = int(round(p_val**(256 / 563)))
	else:
		return 0

	if i_return_value < 256 and i_return_value >= 0:
		return i_return_value
	elif i_return_value > 255:
		return 255
	elif i_return_value < 0:
		return 0

def linearize_value(p_val, p_color_space):
	if p_color_space == 0:
		return linearize_srgb_value(p_val)
	elif p_color_space == 1:
		return linearize_argb_value(p_val)

def delinearize_value(p_val, p_color_space):
	if p_color_space == 0:
		return delinearize_srgb_value(p_val)
	elif p_color_space == 1:
		return delinearize_argb_value(p_val)

#This converts a pixel region into a C array.
#This is necessary to send the region data to all the parallel processes.
def serialize_pixel_region(p_region):
	return array('B', p_region[0:p_region.w,p_region.y:(p_region.y + p_region.h)])

#The main pixel-level calculations for the Brettel model. Since the XYZ->LMS matrix	is pre-normalized,
#the coordinates of the grays are assumed to be (1,1,1), thus, reducing the number of math ops required.
def process_brettel(p_region_data, anomaly, transformation, color_space, bpp, p_is_main_thread = False):
	i_total_len = len(p_region_data)

	#choose the correct transformation matrices
	l_lms_to_rgb = l_brettel_transforms[transformation][color_space]['lmstorgb']
	l_rgb_to_lms = l_brettel_transforms[transformation][color_space]['rgbtolms']

	#chose the correct anchor point values
	if transformation < 4:
		l_lms_coeffs = l_lms_coeffs_combined[transformation]
	else:
		l_lms_coeffs = l_lms_coeffs_combined[transformation][color_space]

	#precalc all anchor coefficients into constants.
	f_coeff_a_475 = get_coeff(l_lms_coeffs[475], 'a')
	f_coeff_b_475 = get_coeff(l_lms_coeffs[475], 'b')
	f_coeff_c_475 = get_coeff(l_lms_coeffs[475], 'c')
	f_coeff_a_485 = get_coeff(l_lms_coeffs[485], 'a')
	f_coeff_b_485 = get_coeff(l_lms_coeffs[485], 'b')
	f_coeff_c_485 = get_coeff(l_lms_coeffs[485], 'c')
	f_coeff_a_575 = get_coeff(l_lms_coeffs[575], 'a')
	f_coeff_b_575 = get_coeff(l_lms_coeffs[575], 'b')
	f_coeff_c_575 = get_coeff(l_lms_coeffs[575], 'c')
	f_coeff_a_660 = get_coeff(l_lms_coeffs[660], 'a')
	f_coeff_b_660 = get_coeff(l_lms_coeffs[660], 'b')
	f_coeff_c_660 = get_coeff(l_lms_coeffs[660], 'c')

	#precalc the linear values. Since only 8 bit per channel images are supported for now,
	#we only need to have 256 possible linearized values. Such pre-calculation makes the
	#pixel-level calculations noticeably faster than applying the linearization function every time.
	l_linear_values = []
	for i in range(256):
		l_linear_values.append(linearize_value(i, color_space))

	#the pixel region data is serialized into a flat array of bytes with each pixel represented by bpp of them.
	#we need to modify the first 3 bits.
	for idx in range(i_total_len // bpp):
		#not sure if this check or just updating the progress for every pixel is faster.
		#visually, doesn't seem to make a difference.
		if p_is_main_thread and idx % 1000 == 0:
			gimp.progress_update(0.05 + float(idx) / float(i_total_len / bpp) * 0.9)

		pixel = p_region_data[idx*bpp:idx*bpp+3]
		l_color_vect = [l_linear_values[pixel[0]], l_linear_values[pixel[1]], l_linear_values[pixel[2]]]
		l_lms_vect = vproduct3d(l_rgb_to_lms, l_color_vect)

		if anomaly == 0:
			#protanopia
			if l_lms_vect[2] < l_lms_vect[1]:
				l_lms_vect[0] = -(f_coeff_b_575 * l_lms_vect[1] + f_coeff_c_575 * l_lms_vect[2]) / f_coeff_a_575
			else:
				l_lms_vect[0] = l_lms_vect[0] = -(f_coeff_b_475 * l_lms_vect[1] + f_coeff_c_475 * l_lms_vect[2]) / f_coeff_a_475
		elif anomaly == 1:
			#deuteranopia
			if l_lms_vect[2] < l_lms_vect[0]:
				l_lms_vect[1] = -(f_coeff_a_575 * l_lms_vect[0] + f_coeff_c_575 * l_lms_vect[2]) / f_coeff_b_575
			else:
				l_lms_vect[1] = -(f_coeff_a_475 * l_lms_vect[0] + f_coeff_c_475 * l_lms_vect[2]) / f_coeff_b_475
		elif anomaly == 2:
			#tritanopia
			if l_lms_vect[1] < l_lms_vect[0]:
				l_lms_vect[2] = -(f_coeff_a_660 * l_lms_vect[0] + f_coeff_b_660 * l_lms_vect[1]) / f_coeff_c_660
			else:
				l_lms_vect[2] = -(f_coeff_a_485 * l_lms_vect[0] + f_coeff_b_485 * l_lms_vect[1]) / f_coeff_c_485

		l_new_color_vect = vproduct3d(l_lms_to_rgb, l_lms_vect)
		p_region_data[idx*bpp:idx*bpp+3] = array('B', [delinearize_value(l_new_color_vect[0], color_space), delinearize_value(l_new_color_vect[1], color_space), delinearize_value(l_new_color_vect[2], color_space)])

	return p_region_data

def process_physio(p_region_data, anomaly, shift, color_space, bpp, p_is_main_thread = False):
	i_total_len = len(p_region_data)

	#precalc the linear values. Same as above.
	l_linear_values = []
	for i in range(256):
		l_linear_values.append(linearize_value(i, color_space))

	for idx in range(i_total_len // bpp):
		if p_is_main_thread and idx % 1000 == 0:
			gimp.progress_update(0.05 + float(idx) / float(i_total_len / bpp) * 0.9)

		pixel = p_region_data[idx*bpp:idx*bpp+3]
		l_color_vect = [l_linear_values[pixel[0]], l_linear_values[pixel[1]], l_linear_values[pixel[2]]]
		l_new_color_vect = vproduct3d(physio_model_matrices[shift][anomaly], l_color_vect)

		p_region_data[idx*bpp:idx*bpp+3] = array('B', [delinearize_value(l_new_color_vect[0], color_space), delinearize_value(l_new_color_vect[1], color_space), delinearize_value(l_new_color_vect[2], color_space)])

	return p_region_data

def calibrated_dichromacy(img, layer, anomaly, model, transformation, shift, color_space):
	#gimp.progress_init("Dichromatizing " + layer.name + "...")
	gimp.progress_init('Serializing image data')
	i_thread_cnt = multiprocessing.cpu_count()

	# Set up an undo group, so the operation will be undone in one step.
	pdb.gimp_image_undo_group_start(img)

	# Get the layer position.
	pos = 0;
	for i in range(len(img.layers)):
		if(img.layers[i] == layer):
			pos = i

	# Create a new layer to save the results (otherwise is not possible to undo the operation).
	newLayer = gimp.Layer(img, layer.name + " temp", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
	img.add_layer(newLayer, pos)
	layerName = layer.name

	# Clear the new layer.
	pdb.gimp_edit_clear(newLayer)
	newLayer.flush()

	try:
		#Create a number of pixel regions equal to the number of cores in the system,
		#serialize them and apply the pixel-level procedures defined above to every one of them.
		#The first region is handled in this process while separete processes are created for the subsequent ones.
		l_new_region_collection = [[]]

		l_results = []
		l_serialized_regions = []
		if i_thread_cnt > 1:
			#create a pool of processes to handle the extra regions and process them asynchronously below.
			o_pool = multiprocessing.Pool(processes=i_thread_cnt)
			for cpu in range(1, i_thread_cnt):
				i_start = (layer.height // i_thread_cnt) * cpu
				if cpu < i_thread_cnt - 1:
					i_end = (layer.height // i_thread_cnt) * (cpu + 1)
				else:
					i_end = layer.height

				l_serialized_regions.append(serialize_pixel_region(layer.get_pixel_rgn(0, i_start, layer.width, i_end - i_start)))
				gimp.progress_update(0.05 * cpu / float(i_thread_cnt + 1))

		#Process the first region in this thread.
		o_riginal_serialized_region = serialize_pixel_region(layer.get_pixel_rgn(0, 0, layer.width, layer.height // i_thread_cnt))

		gimp.progress_init('Performing parallel calculations')
		gimp.progress_update(0.05)

		if model == 0:
			#Brettel et. al.
			for rgn in l_serialized_regions:
				l_results.append(o_pool.apply_async(process_brettel, [rgn, anomaly, transformation, color_space, layer.bpp]))

			l_new_region_collection[0] = process_brettel(o_riginal_serialized_region, anomaly, transformation, color_space, layer.bpp, True)
		elif model == 1:
			#physiological (Machado, Oliveira, Fernandes).
			for rgn in l_serialized_regions:
				l_results.append(o_pool.apply_async(process_physio, [rgn, anomaly, shift, color_space, layer.bpp]))

			l_new_region_collection[0] = process_physio(o_riginal_serialized_region, anomaly, shift, color_space, layer.bpp, True)

		for res in l_results:
			l_new_region_collection.append(res.get())

		gimp.progress_init('Flushing new data')
		gimp.progress_update(0.95)

		#Now deserialize the flat region data arrays back into pixel regions
		i_dx = 0
		for stripe in l_new_region_collection:
			gimp.progress_update(0.95 + (float((i_dx / i_thread_cnt) * 0.05)))
			i_y_start = (layer.height // i_thread_cnt) * i_dx
			if i_dx < i_thread_cnt - 1:
				i_y_end = (layer.height // i_thread_cnt) * (i_dx + 1)
			else:
				i_y_end = layer.height

			pr = newLayer.get_pixel_rgn(0, i_y_start, layer.width, i_y_end - i_y_start)
			pr[0:pr.w, pr.y:(pr.y + pr.h)] = stripe.tostring()
			i_dx += 1

		# Update the new layer.
		newLayer.flush()
		newLayer.merge_shadow(True)
		newLayer.update(0, 0, newLayer.width, newLayer.height)

		# Remove the old layer.
		img.remove_layer(layer)

		# Change the name of the new layer (two layers can not have the same name).
		newLayer.name = layerName
	except Exception as err:
		import traceback
		gimp.message("Unexpected error: " + str(err) + traceback.format_exc())

	# Close the undo group.
	pdb.gimp_image_undo_group_end(img)

	# End progress.
	pdb.gimp_progress_end()

# Register with The Gimp
register(
	"python_fu_multimodel_cvd_parallel",
	"Multimodel color blindness simulator (parallel)",
	"Multimodel color blindness simulator. sRGB and Adobe RGB (Brettel with CIE and CVRL transformations only) color spaces, D65. Empirical (Brettel) and physiological models. This version is intended for use on all multicore (i.e. almost all modern) systems.  Unfortunately, rather slow due to slow math operations in Python and the necessity to perform pixel-level calculations. It should work on single core machines but will be slightly slower due to the serialization and deserialization of data.",
	"Konstantin Kharlov (tnphis)",
	"Public domain",
	"2015",
	"<Image>/Python-Fu/Effects/Multimodel color blindness simulator (parallel)",
	"RGB*",
	[
		(PF_OPTION, "Anomaly", "Type of color vision anomaly", 1, ["Protanomaly", "Deuteranomaly", "Tritanomaly"]),
		(PF_OPTION, "Model", "Simulation model", 0, ["Empirical (Brettel et. al.)", "Physiological (Machado, Oliveira, Fernandes)"]),
		(PF_OPTION, "Transformation", "Empirical model transformation", 0, ["CIE standard (von Kries)", "CIECAM02 (\"spectrally sharpened\")", "CRT primaries (Vischeck, GIMP filters)", "CVRL", "Simulated primaries (normal cones)", "Simulated primaries (ciecam02 \"sharpened\" cones)"]),
		(PF_OPTION, "Shift", "Physiological model cone responsivity shift", 9, ['2nm','4nm','6nm','8nm','10nm','12nm','14nm','16nm','18nm','20nm (dichromacy)']),
		(PF_OPTION, "Colorspace", "Color space (Brettel with CIE and CVRL transformations only)", 0, ["sRGB", "Adobe RGB"])
	],
	[],
	calibrated_dichromacy
)

main()

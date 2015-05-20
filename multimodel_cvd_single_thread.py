from __future__ import division

from gimpfu import *

#RGB to R'G'B' matrices for the physiological model.
#Based on the research by Gustavo M. Machado, Manuel M. Oliveira, and Leandro A. F. Fernandes
#(http://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html)
#mentioned in another plugin (http://registry.gimp.org/node/24885).
#The matrices are pre-calculated by the researchers, and I have not tried to reproduce the results myself (might do it at some unspecified point in the future).
#Judging by the appearance, they used the same calibration as Vischeck
#which seems to be close enough to the sRGB color space.
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

#The transformation matrices. The RGB->XYZ matrices are parts of the standards and
#are obtained directly from wikipedia (http://en.wikipedia.org/wiki/SRGB, http://en.wikipedia.org/wiki/Adobe_RGB_color_space).
#For XYZ to LMS the Hunt-Pointer-Estevez matrix from http://en.wikipedia.org/wiki/LMS_color_space is used.
#The pre-normalized D65 version is used for convenience and reduction of the number of math ops per pixel.
#In the resulting images, the yellows are marginally shifted towards orange in comparison to Vischeck,
#but this difference is not significant enough to look like an error, especially, given the luminosity similarities.
#It can probably be explained by slightly different calibration (the xyz-lms matrix or rgb color space used).
#You may try the equal energy version if you like but it will not leave the grays invariant.
l_srgb_to_xyz = [[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]
l_xyz_to_lms = [[0.4002, 0.7076, -0.0808], [-0.2263, 1.1653, 0.0457], [0, 0, 0.9182]] #d65
l_argb_to_xyz = [[0.57667, 0.18556, 0.18823], [0.29734, 0.62736, 0.07529], [0.02703, 0.07069, 0.99134]]
#l_xyz_to_lms = [[0.38971, 0.68898, -0.07868],[-0.22981, 1.1834, 0.04641],[0, 0, 1]] #equal energy

#pre-compute matrices
l_srgb_to_lms = mproduct3d(l_xyz_to_lms, l_srgb_to_xyz)
l_lms_to_srgb = minverse3d(l_srgb_to_lms)

l_argb_to_lms = mproduct3d(l_xyz_to_lms, l_argb_to_xyz)
l_lms_to_argb = minverse3d(l_argb_to_lms)

#The LMS coordinates of the spectral colors for the Brettel color model.
#The XYZ coordinates are obtained from http://cvrl.ioo.ucl.ac.uk/cie.htm and converted to LMS using the matrix above.
#These values don NOT need to stay within the gamut, the projection takes care of it, as stated in the research paper.
l_xyz_coeffs = {
	475 : [0.1421, 0.1126, 1.0419],
	485 : [0.05795, 0.1693, 0.6162],
	575 : [0.8425, 0.9154, 0.0018],
	660 : [0.1649, 0.061, 0]
}

l_lms_coeffs = {}
for l, coeff in l_xyz_coeffs.iteritems():
	l_lms_coeffs[l] = vproduct3d(l_xyz_to_lms, coeff)

def get_coeff(p_vect, p_coeff):
	if p_coeff == 'a':
		return p_vect[2] - p_vect[1]
	elif p_coeff == 'b':
		return p_vect[0] - p_vect[2]
	elif p_coeff == 'c':
		return p_vect[1] - p_vect[0]

#precalc all coeffs into consts
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

def calibrated_dichromacy(img, layer, anomaly, model, shift, color_space):
	l_anomaly_names = ['protanomaly', 'deuteranomaly', 'tritanomaly']
	gimp.progress_init('Applying ' + l_anomaly_names[anomaly] + ' simulation to ' + layer.name + '...')

	#Set up an undo group, so the operation will be undone in one step.
	pdb.gimp_image_undo_group_start(img)

	#Get the layer position.
	pos = 0;
	for i in range(len(img.layers)):
		if(img.layers[i] == layer):
			pos = i

	#Create a new layer to save the results (otherwise is not possible to undo the operation).
	newLayer = gimp.Layer(img, layer.name + " temp", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
	img.add_layer(newLayer, pos)
	layerName = layer.name

	#Clear the new layer.
	pdb.gimp_edit_clear(newLayer)
	newLayer.flush()

	l_rgb_to_lms = []
	l_lms_to_rgb = []
	if color_space == 0:
		l_rgb_to_lms = l_srgb_to_lms
		l_lms_to_rgb = l_lms_to_srgb
	elif color_space == 1:
		l_rgb_to_lms = l_argb_to_lms
		l_lms_to_rgb = l_lms_to_argb

	#The following tile-based calculation code used the example in test-discolour-v4.py
	#from the templates available here: http://registry.gimp.org/node/5969 as a baseline.
	#There are some nice templates available there for those who find the official documentation lacking.
	try:
		#Calculate the number of tiles.
		tn = int(layer.width / 64)
		if(layer.width % 64 > 0):
			tn += 1
		tm = int(layer.height / 64)
		if(layer.height % 64 > 0):
			tm += 1

		#precalc the linear values. Since only 8 bit per channel images are supported for now,
		#we only need to have 256 possible linearized values. Such pre-calculation makes the
		#pixel-level calculations noticeably faster than applying the linearization function every time.
		l_linear_values = []
		for i in range(256):
			l_linear_values.append(linearize_value(i, color_space))

		#Iterate over the tiles.
		if model == 0:
			for i in range(tn):
				for j in range(tm):
					#Update the progress bar.
					gimp.progress_update(float(i*tm + j) / float(tn*tm))

					#Get the tiles.
					srcTile = layer.get_tile(False, j, i)
					dstTile = newLayer.get_tile(False, j, i)

					#Iterate over the pixels of each tile.
					for x in range(srcTile.ewidth):
						for y in range(srcTile.eheight):
							pixel = srcTile[x,y]
							l_color_vect = l_color_vect = [l_linear_values[ord(pixel[0])], l_linear_values[ord(pixel[1])], l_linear_values[ord(pixel[2])]]
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

							res = chr(delinearize_value(l_new_color_vect[0], color_space)) + chr(delinearize_value(l_new_color_vect[1], color_space)) + chr(delinearize_value(l_new_color_vect[2], color_space))

							#If the image has an alpha channel (or any other channel) copy their values.
							if(len(pixel) > 3):
								for k in range(len(pixel)-3):
									res += pixel[k+3]

							#Save the value in the result layer.
							dstTile[x,y] = res
		elif model == 1:
			for i in range(tn):
				for j in range(tm):
					#Update the progress bar.
					gimp.progress_update(float(i*tm + j) / float(tn*tm))

					#Get the tiles.
					srcTile = layer.get_tile(False, j, i)
					dstTile = newLayer.get_tile(False, j, i)

					#Iterate over the pixels of each tile.
					for x in range(srcTile.ewidth):
						for y in range(srcTile.eheight):
							pixel = srcTile[x,y]
							l_color_vect = [l_linear_values[ord(pixel[0])], l_linear_values[ord(pixel[1])], l_linear_values[ord(pixel[2])]]
							l_trans_matrix = physio_model_matrices[shift][anomaly]
							l_new_color_vect = vproduct3d(l_trans_matrix, l_color_vect)

							res = chr(delinearize_value(l_new_color_vect[0], color_space)) + chr(delinearize_value(l_new_color_vect[1], color_space)) + chr(delinearize_value(l_new_color_vect[2], color_space))

							#If the image has an alpha channel (or any other channel) copy their values.
							if(len(pixel) > 3):
								for k in range(len(pixel)-3):
									res += pixel[k+3]

							#Save the value in the result layer.
							dstTile[x,y] = res

		#Update the new layer.
		newLayer.flush()
		newLayer.merge_shadow(True)
		newLayer.update(0, 0, newLayer.width, newLayer.height)

		#Remove the old layer.
		img.remove_layer(layer)

		#Change the name of the new layer (two layers can not have the same name).
		newLayer.name = layerName
	except Exception as err:
		import traceback
		gimp.message("Unexpected error: " + str(err) + traceback.format_exc())

	#Close the undo group.
	pdb.gimp_image_undo_group_end(img)

	#End progress.
	pdb.gimp_progress_end()

# Register with The Gimp
register(
	"python_fu_multimodel_cvd_single",
	"Multimodel color blindness simulator (single thread)",
	"Multimodel color blindness simulator. sRGB and Adobe RGB (Brettel only) color spaces, D65. Empirical (Brettel) and physiological models. Unfortunately, rather slow due to slow math operations in Python and the necessity to perform pixel-level calculations. This version is intended for use on single-core machines only. It will work on multicore machines but will be much slower than the multicore version.",
	"Konstantin Kharlov (tnphis)",
	"Public domain",
	"2015",
	"<Image>/Python-Fu/Effects/Multimodel color blindness simulator (single thread)",
	"RGB*",
	[
		(PF_OPTION, "Anomaly", "Type of color vision anomaly", 1, ["Protanomaly", "Deuteranomaly", "Tritanomaly"]),
		(PF_OPTION, "Model", "Simulation model", 0, ["Empirical (Brettel et. al.)", "Physiological (Machado, Oliviera, Fernandes)"]),
		(PF_OPTION, "Shift", "Cone responsivity shift (physiological model only)", 9, ['2nm','4nm','6nm','8nm','10nm','12nm','14nm','16nm','18nm','20nm']),
		#(PF_SLIDER, "Shift", "Lambda shift (physiological model only)", 20, [2,20,2]),
		(PF_OPTION, "Colorspace", "Color space", 0, ["sRGB", "Adobe RGB (Brettel only)"])
	],
	[],
	calibrated_dichromacy
)

main()

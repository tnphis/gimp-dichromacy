from __future__ import division
import math
from copy import deepcopy

def vproduct3d(p_matrix, p_vector):
	#every new number assignment involves a new object creation in py.
	#therefore, just do it in one step.
	return [
		p_matrix[0][0] * p_vector[0] + p_matrix[0][1] * p_vector[1] + p_matrix[0][2] * p_vector[2],
		p_matrix[1][0] * p_vector[0] + p_matrix[1][1] * p_vector[1] + p_matrix[1][2] * p_vector[2],
		p_matrix[2][0] * p_vector[0] + p_matrix[2][1] * p_vector[1] + p_matrix[2][2] * p_vector[2]
	]

def gauss(x, mean, sdleft, sdright=None):
	if sdright is None:
		sdright = sdleft
	if x > mean:
		return round(math.exp(-(x - mean)**2 / (2 * sdright**2)), 6)
	else:
		return round(math.exp(-(x - mean)**2 / (2 * sdleft**2)), 6)

def generate_gauss_primaries(p_fn, **args):
	l_func = []
	for x in range(args['min'], args['max'] + 1):
		l_primaries_vect = [
			gauss(x, args['vals'][0][0], args['vals'][0][1], args['vals'][0][2]),
			gauss(x, args['vals'][1][0], args['vals'][1][1], args['vals'][1][2]),
			gauss(x, args['vals'][2][0], args['vals'][2][1], args['vals'][2][2])
		]

		l_calibrated_vect = vproduct3d(args['calibration_matrix'], l_primaries_vect)

		l_func.append([
			x,
			l_calibrated_vect[0] * args['final_coeffs'][0],
			l_calibrated_vect[1] * args['final_coeffs'][1],
			l_calibrated_vect[2] * args['final_coeffs'][2]
		])

	s_out_fn = open(p_fn, 'w')
	for row in l_func:
		s_out_fn.write(','.join([str(row[0]), str(row[1]), str(row[2]), str(row[3])]) + '\n')

	s_out_fn.close()

if __name__ == '__main__':
	#"wide" red spectrum but no green channel mixing required to match the chromaticity specs
	generate_gauss_primaries('primaries_srgb_std_gauss.csv', min=360, max=830, vals=[[635, 28.5, 25], [537, 32, 35], [447, 18, 30.3]], calibration_matrix=[[1,0,0.023],[0,1,0],[0.021,0,1]], final_coeffs = [0.927926,1.0144366,1.09576])
	generate_gauss_primaries('primaries_argb_std_gauss.csv', min=360, max=830, vals=[[635, 28.5, 25], [536.2, 23.4, 16.6], [447, 18, 30.3]], calibration_matrix=[[1,0,0.023],[0,1,0],[0.021,0,1]], final_coeffs = [0.9616656,1.0431,0.8433537])

	#alternative red, seems closer to the real white LED or CCFL-backlit LCD spectra
	#but requires some green channel mixed into the red and blue for proper calibration
	generate_gauss_primaries('primaries_srgb_alt_red.csv', min=360, max=830, vals=[[640.9, 20, 30], [537, 32, 35], [447, 18, 30.3]], calibration_matrix=[[1,0.043,0.01],[0,1,0],[0.032,0.001,1]], final_coeffs = [1.28506,.93731,1.01113])
	generate_gauss_primaries('primaries_argb_alt_red.csv', min=360, max=830, vals=[[640.9, 20, 30], [536.2, 23.4, 16.6], [447, 18, 30.3]], calibration_matrix=[[1,0.06,0.012],[0,1,0],[0.033,0.0015,1]], final_coeffs = [1.317512, .930552, .751203])

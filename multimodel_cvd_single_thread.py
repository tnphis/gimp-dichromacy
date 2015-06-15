from __future__ import division

from gimpfu import *

#RGB to R'G'B' matrices for the physiological model.
#Based on the research by Gustavo M. Machado, Manuel M. Oliveira, and Leandro A. F. Fernandes
#(http://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html)
#mentioned in another plugin (http://registry.gimp.org/node/24885).
#The matrices are pre-calculated by the researchers and the primaries they used were not provided in the paper.
#Judging by the appearance, they used the same calibration as the Vischeck (CRT Primaries).
#protanomaly, deuteranomaly, tritanomaly for responsivity shifts @ 2nm steps for L and M cones and presumably ~6nm steps for S cones.
physio_model_matrices = [[ #2nm/~6nm
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
	],[ #4nm/~12nm
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
	],[ #6nm/~18nm
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
	],[ #8nm/~24nm
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
	],[ #10nm/~30nm
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
	],[ #12nm/~36nm
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
	],[ #14nm/~42nm
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
	],[ #16nm/~48nm
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
	],[ #18nm/~54nm
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
	],[ #20nm/~60nm
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

#Matrices obtained with simulated primaries. Dimensions: shift, color space, anomaly.
#Shift steps are 2 nm for L and M cones and 7nm for L cones.
physio_model_sim_matrices = [[[[[0.8399401892783793, 0.1907905127336531, -0.03073070201203243], [0.032886461038398485, 0.95600995317495, 0.01110358578665184], [-0.007393516758380458, -0.014839199987122732, 1.0222327167455032]], [[0.8491516959474267, 0.1742057189868368, -0.023357414934263576], [0.05428378499047967, 0.9402094307238155, 0.005506784285705016], [-0.0020670880228678516, 0.010944555480803388, 0.9911225325420644]], [[0.8094715743351788, 0.11690502287699933, 0.07362340278782187], [0.0487508834224058, 0.9355928454706185, 0.0156562711069759], [0.0638127344890388, 0.2243335010003178, 0.7118537645106435]]], [[[0.8572468265628987, 0.15972223022423038, -0.016969056787129122], [0.0441883970242237, 0.9452741317502342, 0.010537471225541911], [-0.007704102874930676, -0.013841881020913264, 1.0215459838958438]], [[0.875345517094726, 0.13824106560369642, -0.013586582698422445], [0.07410700165789791, 0.9212371514626672, 0.004655846879434752], [9.307560426002198e-05, 0.008127720266002836, 0.991779204129737]], [[0.853261614967605, 0.09189764795912392, 0.054840737073270945], [0.05839125704649814, 0.9285946818414814, 0.013014061112020164], [0.07849824817771346, 0.17391141532201834, 0.747590336500268]]]], [[[[0.7107374797984265, 0.34577562220906355, -0.056513102007490046], [0.0564010988831915, 0.9230090631766211, 0.02058983794018758], [-0.013307321567481064, -0.03206388510870326, 1.0453712066761844]], [[0.7339053462603586, 0.3066354130870479, -0.040540759347406585], [0.09773744029236991, 0.8930941996079214, 0.009168360099708658], [-0.002883392570260405, 0.020643298378021178, 0.9822400941922389]], [[0.7471241019023493, 0.16951356816251262, 0.08336232993513809], [0.06499564853069792, 0.9089373755600999, 0.026066975909202386], [0.08238987012620683, 0.30756213051563175, 0.6100479993581615]]], [[[0.7391522393467258, 0.2921582048191591, -0.03131044416588502], [0.0763941062215194, 0.9039275630706485, 0.019678330707832065], [-0.014000671066422212, -0.02982145326261166, 1.0438221243290338]], [[0.7791853791104643, 0.24464276657242634, -0.023828145682890683], [0.1343419275464141, 0.8579365938564735, 0.007721478597112252], [0.0012072210210145387, 0.015325556382457025, 0.9834672225965283]], [[0.8116569040199104, 0.12500876138634887, 0.06333433459374066], [0.07517852058253596, 0.9027421356462695, 0.022079343771194485], [0.09918480444878076, 0.23744815815847792, 0.6633670373927412]]]], [[[[0.6028306956397803, 0.47675011424199576, -0.0795808098817759], [0.07348328209810336, 0.8974451633877236, 0.029071554514173134], [-0.01809104568307919, -0.05166243153315421, 1.0697534772162334]], [[0.6428206196779086, 0.41121007954348515, -0.05403069922139375], [0.13387613663889789, 0.8544393041280506, 0.011684559233051728], [-0.002889332793184247, 0.029300419312953192, 0.9735889134802311]], [[0.7419813898706751, 0.1860384981352734, 0.07198011199405158], [0.06611111482325846, 0.898364032939237, 0.035524852237504775], [0.0856368600561601, 0.35051401399469667, 0.5638491259491433]]], [[[0.6384110165303305, 0.4058605460565407, -0.044271562586871316], [0.10022228981277337, 0.8718221006852528, 0.02795560950197362], [-0.019170083768743074, -0.047994124067269765, 1.0671642078360126]], [[0.7027788800738984, 0.32931243716356745, -0.03209131723746583], [0.18501500603608453, 0.805185083616242, 0.009799910347673399], [0.002979480297886609, 0.021703645990203073, 0.9753168737119101]], [[0.8197622365120241, 0.125618538302826, 0.05461922518514975], [0.07142561491112778, 0.8973356541528218, 0.031238730936050285], [0.09824426320276791, 0.2701919313382292, 0.6315638054590028]]]], [[[[0.5107225819045514, 0.5901158659421897, -0.10083844784674112], [0.08579671205881607, 0.8773928650655703, 0.03681042287561362], [-0.021880545613566983, -0.0735719667093495, 1.0954525123229162]], [[0.5693695248047418, 0.4954723294472192, -0.06484185425196098], [0.1646822363548715, 0.8219539316066161, 0.013363832038512477], [-0.0022887948840041427, 0.03715458646053298, 0.9651342084234711]], [[0.7712631773898438, 0.18181362112061528, 0.046923201489541044], [0.05799576340887558, 0.8954057451523105, 0.04659849143881408], [0.0806236862910234, 0.3827779267646398, 0.5365983869443368]]], [[[0.5507733184613725, 0.5055448565603669, -0.05631817502173944], [0.11772905690783954, 0.8466883799559427, 0.03558256313621763], [-0.02329322759571808, -0.0683502541049877, 1.091643481700706]], [[0.64105889526734, 0.39783587795884406, -0.038894773226183926], [0.22858780232710996, 0.7602687441137514, 0.011143453559138372], [0.005260210198045263, 0.027429599105802924, 0.9673101906961517]], [[0.8542452604002873, 0.10999316874492493, 0.03576157085478779], [0.05664418670734367, 0.8997765481396095, 0.04357926515304662], [0.08665555502722966, 0.3027048742008694, 0.6106395707719008]]]], [[[[0.43063313204090764, 0.6902959925853179, -0.12092912462622557], [0.09448314781551209, 0.8615296843354215, 0.04398716784906649], [-0.024754138477602387, -0.09780717391467034, 1.1225613123922726]], [[0.5091815400438867, 0.5644715263606555, -0.07365306640454194], [0.19148302897484, 0.7941043088263221, 0.014412662198838036], [-0.001218588552631671, 0.04436684504461312, 0.9568517435080186]], [[0.8190874211398118, 0.16893184196917055, 0.011980736891017724], [0.04490585888087115, 0.8940687983648807, 0.061025342754248285], [0.07117999002196379, 0.42246580650585047, 0.5063542034721856]]], [[[0.47325233031871006, 0.5945375607543737, -0.06778989107308367], [0.13035630103350732, 0.82693400238344, 0.042709696583052625], [-0.026409093371183554, -0.09093522925666832, 1.1173443226278519]], [[0.5905555834393348, 0.4540378425541851, -0.0445934259935199], [0.2667460624662582, 0.7213290738072039, 0.011924863726537796], [0.007946569188880453, 0.032619338313677464, 0.959434092497442]], [[0.8885992026035675, 0.09676868530532257, 0.014632112091109747], [0.04178246809082736, 0.8971851946097715, 0.06103233729940095], [0.07597873973500943, 0.36004634550786047, 0.5639749147571301]]]], [[[[0.3598738044214893, 0.7804589196889083, -0.1403327241103976], [0.1003523284327433, 0.8489165128556513, 0.05073115871160565], [-0.02675141256685736, -0.12444023225324709, 1.1511916448201045]], [[0.459220408486233, 0.621715129715382, -0.08093553820161509], [0.21520067967716214, 0.7698248465687407, 0.014974473754097134], [0.00022597292530922037, 0.05105018378437567, 0.9487238432903151]], [[0.8651104662811802, 0.16036274305949594, -0.025473209340675942], [0.03226373532347235, 0.8886915626256437, 0.07904470205088415], [0.062437399376177205, 0.4831470038446135, 0.45441559677920923]]], [[[0.40368433991586083, 0.6752614214794087, -0.07894576139526974], [0.13914526352144954, 0.8114080377140712, 0.04944669876447903], [-0.02852694826520372, -0.1158373058071924, 1.144364254072396]], [[0.5488130430291988, 0.5006252001637405, -0.049438243192939296], [0.30068304824089603, 0.6870505562836265, 0.012266395475477268], [0.01096544086452143, 0.037355930094434185, 0.9516786290410445]], [[0.8897109654099284, 0.10795467510653572, 0.002334359483535567], [0.0403596398768194, 0.8774126494112534, 0.08222771071192705], [0.08166488144506423, 0.4522020601623406, 0.46613305839259517]]]], [[[[0.29647618536517917, 0.8629485663557984, -0.1594247517209776], [0.10399462266575453, 0.8388673812959329, 0.057137996038312655], [-0.02788401285974104, -0.15359034609196792, 1.181474358951709]], [[0.41731112909809265, 0.6697153302314403, -0.08702645932953285], [0.2364958482712997, 0.748352164909728, 0.01515198681897234], [0.0019763739175436565, 0.0572865260650254, 0.9407371000174308]], [[0.8871793638806025, 0.16819650692514349, -0.055375870805745936], [0.025886794703455313, 0.8755541593039694, 0.09855904599257545], [0.06064981719136755, 0.5655711543588899, 0.3737790284497424]]], [[[0.3404602335395305, 0.749532145394923, -0.08999237893445353], [0.14486681837001697, 0.7992573384979638, 0.055875843132019126], [-0.02963336582139476, -0.14318134897233387, 1.1728147147937287]], [[0.5140442158640733, 0.5395674192418559, -0.05361163510592912], [0.33126715342292395, 0.6564758555540886, 0.012256991022987496], [0.01426333101216218, 0.041700727196764445, 0.9440359417910734]], [[0.8432516229801897, 0.15464837244115748, 0.0021000045786526006], [0.05859843378753413, 0.8391606403977232, 0.10224092581474246], [0.1080138508296733, 0.5532937235016869, 0.3386924256686397]]]], [[[[0.23896193497102483, 0.9395514559697611, -0.1785133909407859], [0.10585076210825577, 0.8308688097457633, 0.06328042814598107], [-0.02814189075546684, -0.18541890281193488, 1.2135607935674018]], [[0.38185484657396723, 0.7103185383450938, -0.09217338491906119], [0.2558542568603131, 0.7291250504839917, 0.01502069265569525], [0.003982036047837429, 0.06313697368266219, 0.9328809902695003]], [[0.8750873127674208, 0.19745301111365537, -0.07254032388107606], [0.02849558175465486, 0.8554469702267579, 0.1160574480185874], [0.06839145258872795, 0.6522146467320181, 0.27939390067925396]]], [[[0.28235514533499995, 0.8187468728437622, -0.10110201817876222], [0.14810405956621153, 0.7898354361004944, 0.06206050433329394], [-0.029696231824476227, -0.1731261772546212, 1.2028224090790975]], [[0.48491775162850403, 0.5723315581965829, -0.05724930982508705], [0.35914542563256585, 0.6288916784169736, 0.01196289595046024], [0.017800127296535653, 0.0457002521477855, 0.9364996205556788]], [[0.7697182863826866, 0.2230437135882155, 0.007238000029097753], [0.08877887972943083, 0.7944330286343472, 0.11678809163622189], [0.14130881028306458, 0.6289883869137525, 0.2297028028031829]]]], [[[[0.18619490593239016, 1.011669112442283, -0.19786401837467343], [0.10625660075349413, 0.8245280067597136, 0.06921539248679251], [-0.027496820570524615, -0.22012826607385086, 1.2476250866443757]], [[0.351649966029953, 0.7449121128792489, -0.09656207890920188], [0.2736410046464124, 0.7117216871023939, 0.014637308251193762], [0.006204758463007039, 0.06864823593088859, 0.9251470056061043]], [[0.8383996265933364, 0.24121915296845492, -0.07961877956179134], [0.037727921671309866, 0.8331465372707831, 0.12912554105790713], [0.08181854553136009, 0.7224105563557087, 0.1957708981129312]]], [[[0.22841670307659862, 0.8840081884883114, -0.11242489156491012], [0.1493063989072691, 0.7826428387913498, 0.06805076230138105], [-0.02866685068735756, -0.2058643321845366, 1.2345311828718941]], [[0.4604214899996176, 0.600032781589193, -0.060454271588810615], [0.3848098743969846, 0.6037556667873006, 0.011434458815714574], [0.021545101638168706, 0.04939060790822916, 0.9290642904536021]], [[0.6992516140602896, 0.2883768536187238, 0.012371532320986409], [0.11843629853870788, 0.7561242775457038, 0.12543942391558813], [0.16850431574966152, 0.6730123981490681, 0.15848328610127038]]]], [[[[0.13728296113751381, 1.0804333315121337, -0.21771629264964737], [0.10547275534887718, 0.8195385257319527, 0.07498871891917025], [-0.02590414830493433, -0.25796320407473516, 1.283867352379669]], [[0.3257760193246399, 0.7745585702278507, -0.10033458955249058], [0.29013582957140127, 0.6958189053593138, 0.014045265069284898], [0.008615107967784393, 0.07385680509835939, 0.917528086933856]], [[0.7965808262973266, 0.285399573614159, -0.08198039991148554], [0.04851490511247902, 0.8137280581890343, 0.13775703669848688], [0.0951114658297513, 0.7696449223565498, 0.13524361181369893]]], [[[0.1778895175542736, 0.9462083262395897, -0.12409784379386324], [0.14882602471450104, 0.7772867668185375, 0.07388720846696137], [-0.02648076487657983, -0.24162367309593275, 1.2681044379725128]], [[0.43977224405574517, 0.6235338270564937, -0.06330607111223904], [0.4086412903129436, 0.5806480850894711, 0.010710624597585039], [0.02547426792029295, 0.05280039406227273, 0.9217253380174342]], [[0.6485749353055696, 0.3358401099867354, 0.015584954707694852], [0.14005361536746053, 0.7296087316655648, 0.13033765296697458], [0.18621181665151101, 0.6965737422455609, 0.11721444110292817]]]]]

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
#There are 5 possible transformations: integration of the products of simulated gauss primaries and the cone responsivities (default),
#CRT primaries (obtained from the GIMP source, transforms rgb to lms directly), Von Kries https://en.wikipedia.org/wiki/LMS_color_space(),
#CVRL-proposed LMS-XYZ transformation (http://cvrl.ioo.ucl.ac.uk/database/text/cienewxyz/cie2012xyz2.htm)
#and a special "spectrally-sharpened" CIECAM02 transformation used for color adaptation algorithms (https://en.wikipedia.org/wiki/CIECAM02).

#The RGB->XYZ matrices are parts of the standards and
#can be located in the following wikipedia articles: http://en.wikipedia.org/wiki/SRGB, http://en.wikipedia.org/wiki/Adobe_RGB_color_space.

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

#Simulated primaries.
l_srgb_to_lms_gauss = [[0.27183462993912216, 0.6553861709738599, 0.07277919908701798], [0.10011063617075368, 0.7755605316616854, 0.12432883216756103], [0.016743294516306868, 0.09181436057854941, 0.8914423449051437]]
l_lms_to_srgb_gauss = minverse3d(l_srgb_to_lms_gauss)

l_argb_to_lms_gauss = [[0.3812453850551629, 0.5429077147318113, 0.07584690021302574], [0.1406469922303191, 0.729748952647324, 0.129604055122357], [0.023772477908623052, 0.0504560223501845, 0.9257714997411925]]
l_lms_to_argb_gauss = minverse3d(l_argb_to_lms_gauss)

#The transformations combined. List dimensions: transformation type, color space
l_brettel_transforms = [
	[ #Simulated primaries, alternative red (normal cones)
		{
			'rgbtolms' : l_srgb_to_lms_gauss,
			'lmstorgb' : l_lms_to_srgb_gauss
		},
		{
			'rgbtolms' : l_argb_to_lms_gauss,
			'lmstorgb' : l_lms_to_argb_gauss
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
	[ #CIECAM02
		{
			'rgbtolms' : l_srgb_to_lms_ciecam02,
			'lmstorgb' : l_lms_to_srgb_ciecam02
		},
		{
			'rgbtolms' : l_argb_to_lms_ciecam02,
			'lmstorgb' : l_lms_to_argb_ciecam02
		}
	]
]

#The LMS coordinates of the spectral colors for the Brettel color model, standard CIE version.
#The XYZ coordinates are obtained from http://cvrl.ioo.ucl.ac.uk/cie.htm.
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

l_lms_coeffs_combined = [
	[ #Simulated primaries - those are color-space dependent, if only marginally.
		{
			475 : [0.101716, 0.205398, 0.8276665],
			485 : [0.140373, 0.268063, 0.465307],
			575 : [0.8496, 0.740291, 0.00028054],
			660 : [0.0796324, 0.00730255, 0]
		},
		{
			475 : [0.101582, 0.205398, 0.824943],
			485 : [0.140188, 0.268063, 0.463776],
			575 : [0.84848, 0.740291, 0.0002796],
			660 : [0.079527, 0.00730255, 0]
		}
	],
	{ #CRT Primaries
		475 : [0.548577, 1.295495, 7.00863],
		485 : [0.879586, 1.835352, 4.321414],
		575 : [6.751715, 6.009815, 0.012824],
		660 : [0.626123, 0.0575055, 0.0]
	},
	l_lms_coeffs_std, #Von Kries
	{ #CVRL
		475 : [0.185767, 0.23705678, 0.9175],
		485 : [0.1620026, 0.3093741, 0.5158188],
		575 : [0.98051357, 0.85439695, 0.000310927],
		660 : [0.091895, 0.084251, 0.0]
	},
	l_lms_coeffs_ciecam02
]

def get_coeff(p_vect, p_coeff):
	if p_coeff == 'a':
		return p_vect[2] - p_vect[1]
	elif p_coeff == 'b':
		return p_vect[0] - p_vect[2]
	elif p_coeff == 'c':
		return p_vect[1] - p_vect[0]

#standard sRGB and aRGB gamma correction procedures. Hardcoding 8 bits per channel for the moment.
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

def calibrated_dichromacy(img, layer, anomaly, model, transformation, primaries, shift, color_space):
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

	#choose the correct transformation matrices
	l_lms_to_rgb = l_brettel_transforms[transformation][color_space]['lmstorgb']
	l_rgb_to_lms = l_brettel_transforms[transformation][color_space]['rgbtolms']

	#chose the correct anchor point values
	if transformation > 0:
		l_lms_coeffs = l_lms_coeffs_combined[transformation]
	else:
		#simulated primaries, marginal color space depencence present.
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

	#get the correct physio model matrix
	l_physio_matrix = physio_model_matrices[shift][anomaly]
	if primaries == 1:
		l_physio_matrix = physio_model_sim_matrices[shift][color_space][anomaly]

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
							l_new_color_vect = vproduct3d(l_physio_matrix, l_color_vect)

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
	"Multimodel color blindness simulator. sRGB and Adobe RGB color spaces (for some options), D65. Empirical (Brettel) and physiological models with multiple options. Unfortunately, rather slow due to slow math operations in Python and the necessity to perform pixel-level calculations. This version is intended for use on single-core machines only. It will work on multicore machines but will be much slower than the multicore version.",
	"Konstantin Kharlov (tnphis)",
	"Public domain",
	"2015",
	"<Image>/Python-Fu/Effects/Multimodel color blindness simulator (single thread)",
	"RGB*",
	[
		(PF_OPTION, "Anomaly", "Type of color vision anomaly", 1, ["Protanomaly", "Deuteranomaly", "Tritanomaly"]),
		(PF_OPTION, "Model", "Simulation model", 0, ["Empirical (Brettel et. al.)", "Physiological (Machado, Oliveira, Fernandes)"]),
		(PF_OPTION, "Transformation", "Empirical model transformation", 0, ["Simulated primaries integration", "CRT primaries (Vischeck, GIMP filters)", "Von Kries (CIE standard)", "CVRL", "CIECAM02 (CIE \"spectrally sharpened\")"]),
		(PF_OPTION, "Primaries", "Physiological model primaries", 0, ["Original research (presumably measured CRT)", "Simulated gauss"]),
		(PF_OPTION, "Shift", "Physiological model cone responsivity shift", 9, ['2nm (L, M) / ~6nm (S, original) / 7nm (S, simulated)','4nm (L, M) / ~12nm (S, original) / 14nm (S, simulated)','6nm (L, M) / ~18 nm (S, original) / 21nm (S, simulated)','8nm (L, M) / ~24mm (S, original) / 28nm (S, simulated)','10nm (L, M) / ~30nm (S, original) / 35nm (S, simulated)','12nm (L, M) / ~36nm (S, original) / 42nm (S, simulated)','14nm (L, M) / ~42nm (S, original) / 49nm (S, simulated)','16nm (L, M) / 48nm (S, original) / 56nm (S, simulated)','18nm (L, M) / ~54nm (S, original) / 63nm (S, simulated)','20nm/~60nm/70nm (dichromacy)']),
		(PF_OPTION, "Colorspace", "Color space", 0, ["sRGB", "Adobe RGB (non-CRT primaries/transformation only)"])
	],
	[],
	calibrated_dichromacy
)

main()

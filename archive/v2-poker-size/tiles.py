Values = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K']
Suits = ['C', 'D', 'H', 'S']
LandResources = ['B', 'C', 'H', 'P']
WaterResources = ['f', 'j', 's', 't']

Deck1 = {
	# Clubs Diamonds Hearts Spades
	'A': ['Pt', 'Cs', 'Hj', 'Bf'],
	'2': ['t', 'H', 'C', 'f'],
	'3': ['P', 'j', 's', 'B'],
	'4': ['C', 'f', 't', 'H'],
	'5': ['B', 'P', 'j', 't'],
	'6': ['j', 'H', 't', 'P'],
	'7': ['s', 'B', 'P', 'j'],
	'8': ['f', 's', 'B', 'P'],
	'9': ['H', 'C', 'f', 's'],
	'0': ['j', 't', 'H', 'C'],
	'J': ['C', 'f', 'B', 's'],
	'Q': ['B', 't', 's', 'H'],
	'K': ['f', 'P', 'C', 'j'],
}

Deck2 = {
	# Clubs Diamonds Hearts Spades
	'A': ['Cj', 'Pf', 'Bt', 'Hs'],
	'2': ['s', 'B', 'P', 'j'],
	'3': ['C', 'f', 't', 'H'],
	'4': ['P', 'j', 's', 'B'],
	'5': ['H', 'C', 'f', 's'],
	'6': ['s', 'B', 'f', 'C'],
	'7': ['t', 'H', 'C', 'f'],
	'8': ['j', 't', 'H', 'C'],
	'9': ['B', 'P', 'j', 't'],
	'0': ['f', 's', 'B', 'P'],
	'J': ['H', 'j', 'P', 't'],
	'Q': ['P', 'C', 'j', 'f'],
	'K': ['t', 's', 'H', 'B'],
}

LandEdges = [3, 6, 7]
WaterEdges = [0, 1, 4]
InvalidEdges = [2, 5, 8, 9]

Topology = {
	# <suit,value>:
	#	Borders,
	#	#Land, #Water, #Ports,
	#	LandResourceConnect, WaterResourceConnect
	'CA': ['1616', 2, 1, 2, '1616', '1616'],
	#'C2': ['0014', 1, 1, 0, '____', '0014'],
	'C2': ['1776', 1, 1, 0, '_776', '1___'],	# single water
	'C3': ['0160', 1, 1, 0, '__6_', '01_0'],	# single land
	'C4': ['0176', 1, 1, 0, '__76', '01__'],	# dup
	'C5': ['1760', 1, 1, 0, '_76_', '1__0'],	# dup
	'C6': ['1740', 1, 1, 1, '1740', '1740'],	# dup
	'C7': ['1436', 2, 1, 0, '__36', '14__'],
	'C8': ['1414', 2, 1, 0, '____', '1414'],
	'C9': ['1416', 2, 1, 0, '___6', '141_'],	# single land
	#'C0': ['1774', 1, 1, 0, '_77_', '1__4'],
	'C0': ['1636', 1, 2, 0, '_636', '1___'],	# single water
	#'CJ': ['1636', 1, 2, 1, '1636', '1636'],
	'CJ': ['1774', 1, 1, 1, '1774', '1774'],
	'CQ': ['0174', 1, 1, 1, '0174', '0174'],	# dup
	#'CK': ['1776', 1, 1, 1, '1776', '1776'],
	'CK': ['0176', 1, 1, 1, '0176', '0176'],	# dup

	'DA': ['3434', 2, 1, 2, '3434', '3434'],
	'D2': ['0016', 1, 1, 0, '___6', '001_'],	# single land
	#'D3': ['0140', 1, 1, 0, '____', '0140'],
	'D3': ['3774', 1, 1, 0, '377_', '___4'],	# single water
	#'D4': ['0176', 1, 1, 0, '__76', '01__'],	# dup
	'D4': ['0014', 1, 1, 0, '____', '0014'],
	'D5': ['1760', 1, 1, 0, '_76_', '1__0'],	# dup
	'D6': ['1740', 1, 1, 1, '1740', '1740'],	# dup
	'D7': ['3636', 2, 1, 0, '3636', '____'],
	'D8': ['4141', 2, 1, 0, '____', '4141'],
	'D9': ['4143', 2, 1, 0, '___3', '414_'],	# single land
	#'D0': ['4177', 1, 1, 0, '__77', '41__'],
	'D0': ['3436', 1, 2, 0, '3_36', '_4__'],	# single water
	#'DJ': ['3436', 1, 2, 1, '3436', '3436'],
	'DJ': ['4177', 1, 1, 1, '4177', '4177'],
	'DQ': ['0174', 1, 1, 1, '0174', '0174'],	# dup
	#'DK': ['3774', 1, 1, 1, '3774', '3774'],
	'DK': ['0036', 1, 1, 1, '0036', '0036'],

	'HA': ['4343', 2, 1, 2, '4343', '4343'],
	'H2': ['0034', 1, 1, 0, '__3_', '00_4'],	# single land
	#'H3': ['0360', 1, 1, 0, '_36_', '0__0'],
	'H3': ['4377', 1, 1, 0, '_377', '4___'],	# single water
	#'H4': ['0374', 1, 1, 0, '_37_', '0__4'],	# dup
	'H4': ['0140', 1, 1, 0, '____', '0140'],
	'H5': ['3740', 1, 1, 0, '37__', '__40'],	# dup
	'H6': ['3760', 1, 1, 1, '3760', '3760'],	# dup
	'H7': ['6363', 2, 1, 0, '6363', '____'],
	'H8': ['1434', 2, 1, 0, '__3_', '14_4'],	# single land
	#'H9': ['1634', 1, 2, 0, '_63_', '1__4'],
	'H9': ['4363', 1, 2, 0, '_363', '4___'],	# single water
	'H0': ['3776', 1, 1, 0, '3776', '____'],
	#'HJ': ['4363', 1, 2, 1, '4363', '4363'],
	'HJ': ['1634', 1, 2, 1, '1634', '1634'],
	'HQ': ['0376', 1, 1, 1, '0376', '0376'],	# dup
	#'HK': ['4377', 1, 1, 1, '4377', '4377'],
	'HK': ['0360', 1, 1, 1, '0360', '0360'],

	'SA': ['6161', 2, 1, 2, '6161', '6161'],
	#'S2': ['0036', 1, 1, 0, '__36', '00__'],
	'S2': ['6177', 1, 1, 0, '6_77', '_1__'],
	'S3': ['0340', 1, 1, 0, '_3__', '0_40'],	# single land
	'S4': ['0374', 1, 1, 0, '_37_', '0__4'],	# dup
	'S5': ['3740', 1, 1, 0, '37__', '__40'],	# dup
	'S6': ['3760', 1, 1, 1, '3760', '3760'],	# dup
	'S7': ['4361', 2, 1, 0, '_36_', '4__1'],
	'S8': ['4161', 2, 1, 0, '__6_', '41_1'],	# single land
	#'S9': ['4163', 1, 2, 0, '__63', '41__'],
	'S9': ['6163', 1, 2, 0, '6_63', '_1__'],	# single water
	'S0': ['6377', 1, 1, 0, '6377', '____'],
	#'SJ': ['6163', 1, 2, 1, '6163', '6163'],
	'SJ': ['4163', 1, 2, 1, '4163', '4163'],
	'SQ': ['0376', 1, 1, 1, '0376', '0376'],	# dup
	#'SK': ['6177', 1, 1, 1, '6177', '6177'],
	'SK': ['0374', 1, 1, 1, '0374', '0374'],	# dup
}

# Sanity check the data table
for ti in Topology:
	t = Topology[ti]
	edges = t[0]
	num_land = t[1]
	num_water = t[2]
	ports = t[3]
	land_connect = t[4]
	water_connect = t[5]
	if ports == 0:
		edge_check = ''
		for i in range(0,4):
			if land_connect[i] == water_connect[i]:
				print 'invalid land/water connect:', ti, land_connect, water_connect
			if land_connect[i] == '_':
				edge_check += water_connect[i]
			else:
				edge_check += land_connect[i]
		if edges != edge_check:
			print 'mismatched edges:', ti, edges, edge_check
	else:
		if edges != land_connect:
			print 'Invalid land_connect:', ti, land_connect
		if edges != water_connect:
			print 'Invalid water_connect:', ti, water_connect
	#print ti, Topology[ti]

land_short_edges = {}
land_long_edges = {}
water_short_edges = {}
water_long_edges = {}

land_short_edges['_'] = 0
land_long_edges['_'] = 0
water_short_edges['_'] = 0
water_long_edges['_'] = 0

for i in range(0, 8):
	land_short_edges[str(i)] = 0
	land_long_edges[str(i)] = 0
	water_short_edges[str(i)] = 0
	water_long_edges[str(i)] = 0

for ti in Topology:
	t = Topology[ti]
	land_connect = t[4]
	water_connect = t[5]

	land_short_edges[land_connect[0]] += 1
	land_long_edges[land_connect[1]] += 1
	land_short_edges[land_connect[2]] += 1
	land_long_edges[land_connect[3]] += 1

	water_short_edges[water_connect[0]] += 1
	water_long_edges[water_connect[1]] += 1
	water_short_edges[water_connect[2]] += 1
	water_long_edges[water_connect[3]] += 1

print land_short_edges
print land_long_edges
print water_short_edges
print water_long_edges

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import re
import subprocess
import sys

hide_guides = True
run_checks = False

resource_encode = {
	'fish': 'f',
	'squid': 's',
	'turtle': 't',
	'banana': 'B',
	'flower': 'H',	# Hibiscus
	'coconut': 'C',
	
	'pirate': 'x',
	'portcircle': 'p',
}

card_info = {
	# <id>: [ pattern, resources, debug-info, label, (seed) ]
	# pattern:
	#   r: resource (f,s,t,B,C,H)
	#   x: pirate
	#   p: port (f,s,t,B,C,H)
	#   l/w: land/water connection
	#   dl/dw: dead-end land (water)
	# resources:
	#   f,s,t: water resources: fish, squid, turtle
	#   B,C,H: land resources: banana, coconut, flower/hibiscus
	#   x: pirate
	#   p: port

	'0000a':	['3rw',	'fst',	'',	'Juven Isle', 25],
	'0000b':	['xw',	'x',	'',	'Argh Isle', 27],

	'0014a':	['rw',	'f',	'',	'Point Exter'],
	'0014b':	['xw',	'x',	'',	'Exclamation Point'],
	'0014c':	['xw',	'x',	'Name',	'Unused'],

	'0016a':	['pl',	'pC',	'TODO',	'Unused'],
	'0016b':	['pw',	'ps',	'TODO',	'Unused'],
	'0016c':	['rdl',	'B',	'TODO',	'Dissa Point'],

	'0034a':	['pl',	'pH',	'TODO',	'Rose Port'],
	'0034b':	['pw',	'pf',	'TODO',	'Port Ico'],
	'0034c':	['rdl', 'C',	'TODO',	'Unused'],

	'0036a':	['pw',	'pf',	'TODO',	'Port Folio'],
	'0036b':	['rl',	'B',	'TODO',	'Unused'],
	'0036c':	['rw',	's',	'TODO',	'Unused'],

	'0174a':	['pl',	'pC',	'TODO',	'Port-au-Bella'],
	'0174b':	['pw',	'ps',	'TODO',	'Port Manteau'],
	'0174c':	['rdl',	'H',	'TODO', 'Unused'],

	'0176a':	['pl',	'pB',	'TODO',	'Port Lee'],
	'0176b':	['pw',	'pt',	'TODO',	'Ruby Port'],
	'0176c':	['rl',	'H',	'TODO',	'Unused'],

	'0374a':	['pl',	'pH',	'TODO',	'Port Starboard'],
	'0374b':	['pw',	'pf',	'TODO',	'Spoils Port'],
	'0374c':	['rw',	't',	'TODO',	'Unused'],

	'0376a':	['pl',	'pB',	'TODO',	'Crusted Port'],
	'0376b':	['pw',	'ps',	'TODO',	'Port Royale'],
	'0376c':	['rdw',	't',	'TODO', 'Unused'],

	'1414a':	['rw',	's',	'TODO',	'Kidneystone Pass'],
	'1414b':	['xw',	'x',	'TODO',	'Noneshall Pass'],

	'1416a':	['pl',	'pC',	'TODO',	'Port-au-Potée'],
	'1416b':	['pw',	'pt',	'TODO',	'Port Hole'],
	'1416c':	['rdl',	'H',	'TODO',	'Unused'],

	'1434a':	['pl',	'pH',	'TODO',	'Back Port'],
	'1434b':	['pw',	'pf',	'TODO',	'Tawny Port'],
	'1434c':	['rdl',	'B',	'TODO',	'Unused'],
	'1434d':	['rdl',	'C',	'TODO',	'Unused'],

	'1436a':	['pl',	'pB',	'TODO',	'Port Judgement'],
	'1436b':	['pw',	'ps',	'TODO',	'Port Able'],
	'1436c':	['2rdw','fs',	'TODO',	'Unused'],
	'1436d':	['rw',	't',	'TODO',	'Unused'],

	'1616a':	['2rdl','BC',	'TODO',	'Unused'],
	'1616b':	['2rdw','tf',	'TODO',	'Unused'],

	'1634a':	['pl',	'pC',	'TODO',	'Serial Port'],
	'1634b':	['pw',	'pt',	'TODO',	'Newport'],
	'1634c':	['2rdl','HB',	'TODO',	'Letme Inlet'],
	'1634d':	['rl',	'C',	'TODO',	'Unused'],

	'1636a':	['pl',	'pH',	'TODO',	'Grande Port'],
	'1636b':	['pw',	'pf',	'TODO',	'Watersport'],
	'1636c':	['rdw',	's',	'TODO',	'Unused'],
	'1636d':	['rdw',	't',	'TODO',	'Unused'],

	'1774a':	['pl',	'pC',	'TODO',	'Freeport'],
	'1774b':	['rl',	'B',	'TODO',	'Unused'],
	'1774c':	['rw',	'f',	'TODO',	'Unused'],

	'1776a':	['pl',	'pB',	'TODO',	'Port End'],
	'1776b':	['pw',	'ps',	'TODO',	'Port Tristam'],
	'1776c':	['rdw',	'f',	'TODO',	'Unused'],

	'3434a':	['2rdl','CH',	'TODO',	'Unused'],
	'3434b':	['2rdw','st',	'TODO',	'Unused'],

	'3436a':	['pl',	'pH',	'TODO',	'Morgansport'],
	'3436b':	['pw',	'pt',	'TODO',	'Port Ray'],
	'3436c':	['rdw',	's',	'TODO',	'Unused'],

	'3636a':	['rl',	'C',	'TODO',	'Unused'],
	'3636b':	['xl',	'x',	'TODO',	'Unused'],

	'3774a':	['pl',	'pB',	'TODO',	'Port Quinta'],
	'3774b':	['pw',	'pt',	'TODO',	'Port Roberts'],
	'3774c':	['rdw',	'f',	'TODO',	'Unused'],

	'3776a':	['rl',	'H',	'TODO',	'Unused'],
	'3776b':	['xl',	'x',	'TODO',	'Unused'],
	'3776c':	['xl',	'x',	'TODO',	'Unused'],

	'7777a':	['3rl',	'BCH',	'TODO',	'Unused'],
	'7777b':	['xl',	'x',	'TODO',	'Unused'],
}

# Port
# ====
# Portuga - cf. Tortuga http://www.thewayofthepirates.com/regions-and-places/tortuga/
# Davenport; Port Cullis; Rose Port; Port Ico; Port Folio; Port-au-Bella; Port Manteau
# Port Lee; Ruby Port; Port Starboard; Spoils Port; Crusted Port
# Port Royale - http://www.atlasobscura.com/places/sunken-pirate-stronghold-at-port-royal
# Port Hole; Port-au-Potée; Back Port; Tawny Port; Port Judgement; Port Able; Serial Port
# Newport - Oldport?; Watersport; Grande Port; Freeport; Port End; Port Tristam; Morgansport
# Port Ray; Port Quinta; Port Roberts
# --
# Vintage Port; Reserve Port; White Port; Com Port; Jonesport; Port Rackham; Cooke Port
# Queensport; Port Roger; Port Crabbe; Port Tempest; Silver Port; Dis Port; Pearl Bay Port
# Kingsport; Portsmouth; Data Port - cf. Data Point
#--
# Port Ugâl; Port Raiture

# Bays, Coves and Inlets
# * Letme Inlet
# Fishstick Bay; Lulla Bay; Dread Cove; Cove Ariant; Cove Alent; Almond Bay; Pork Bay
# Hapless Bay; Black Jack Bay; Jolly Bay; Shady Cove; Knob Cove; Shark Bay; Scurvy Dog Bay
# Half Moon Bay; Stingray Bay; Crystal Bay; Darkwater Bay; Hammerhead Bay; Crybay Bay
# Spirit Bay; Loading Bay; Ghost Bay; Mutiny Bay; One-Ear Cove
# Bomb Bay; Al Cove

# Pass & Strait
# =============
#* Noneshall Pass
#* Kidneystone Pass
# Dire Strait; Crooked Strait; Inappropriate Pass; Je-ne-sais Pass; Buck Pass; Tress Pass
# --
# Forward Pass; Season Pass; Backstage Pass; Twisted Strait; Encom Pass; Privateer Strait
# By Pass; Im Pass; Sur Pass; Over Pass; Under Pass

# Pumpk Inlet; Gobl Inlet; Rais Inlet; Viol Inlet; With Inlet; Urch Inlet; Insul Inlet
# Coff Inlet; Hero Inlet

# Point
# =====
# Check Point; Point Illism; Point Exter; Counter Point; Mary Isthmus; Cur Isthmus
# Data Point; Mid Point; Dagger Point; Needle Point; Dissa Point; Point Less
# Pin Point; Gun Point; Knife Point; View Point; Rea Point; Exclamation Point

# Beach
# =====
# Peg-leg Beach; Shelly Beach; Treasure Beach; Rustyspike Beach; Half-Pig Landing
# Scabby Beach; Skullwater Beach; Coconut Beach; Baldhead Beach; Buccaneer Landing

# Isle
# ====
# Used: Juven Isle
# ====
# Fewt Isle; Noob Isle; Seen Isle; Peen Isle; Rept Isle; Miss Isle; Pure Isle
# Duct Isle; Fraj Isle; Comp Isle; Erect Isle; Quint Isle; Imbess Isle; Chamom Isle
# Crocod Isle; Prehense Isle; Percent Isle; Text Isle; Tact Isle; Project Isle
# Merchant Isle; Insect Isle; Fert Isle
# Isle Land; Carl Isle; Aisle Isle; Argh Isle; Ex Isle; Carlyle Isle
# Blubbernut Isle; Crane Isle

defs = [
	# texture octaves freq blur
	['textureGrassBig', 'texture', 2, 0.07, 2.5],
	['textureGrassSmall', 'texture', 4, 0.5, 1.0],
	['textureLand', 'texture', 4, 0.5, 0.8],
	['textureForestBig', 'texture', 2, 0.3, 2.0],
	['textureForestSmall', 'texture', 4, 0.35, 1.0],
	# roughen turbulence octaves freq scale
	['roughenShoreline', 'roughen', 'turbulence', 4, 0.05, 6.6],
	# roughen noise octaves freq1 freq2 scale
	['roughenForest', 'roughen', 'noise', 4, 0.15, 0.15, 6.6],
	# filter blur x y width height stddev
	['blurWaterDeep', 'filter', 'blur', -0.056690667, -0.041619708, 1.1133813, 1.0832394, 6.9191359],
	['blurWaterShallow', 'filter', 'blur', -0.055818416, -0.042102724, 1.1116368, 1.0842054, 6.5615005],
	['blurWaterHilight', 'filter', 'blur', -0.25, -0.25, 1.5, 1.5, 6.8575319],
	['blurGrass', 'filter', 'blur', -0.032100266, -0.019164084, 1.0642005, 1.0383282, 2.3862132],
	['blurForestShadow', 'filter', 'blur', -0.033575919, -0.018674107, 1.0671518, 1.0373482, 2.1997847],
	['blurFlowerInner', 'filter', 'blur', -0.42, -0.42, 1.84, 1.84, 1.6055398],
	['blurFlowerMiddle', 'filter', 'blur', -0.24, -0.24, 1.48, 1.48, 1.9337049],
	# gradient stops [<stop1>, ...]
	['gradientStopsFish', 'gradient', 'stops', [[0, 'ff5555', 1], [1, 'ffffff', 1]]],
	['gradientStopsCoconut', 'gradient', 'stops', [[0, 'ffffff', 1], [1, 'c8c8c8', 0]]],
	['gradientStopsFlower', 'gradient', 'stops', [[0, 'b16dff', 1], [1, 'e7d2ff', 1]]],
	# gradient linear xlink, x1, y1, x2, y2, transform
	['gradientFish', 'gradient', 'linear', 'gradientStopsFish', 178.78909, -114.78283, 180.4073, -103.78283, 'translate(-178.76256,1.0606602)'],
	# gradient radial xlink, cx, cy, fx, fy, r, transform
	['gradientCoconut', 'gradient', 'radial', 'gradientStopsCoconut', 1.9440963, -60.612652, 1.9440963, -60.612652, 6.7232941, 'matrix(1.691364,-0.31394812,0.29762395,1.603419,17.826033,-7.042221)'],
	['gradientFlower', 'gradient', 'radial', 'gradientStopsFlower', 60.884877, -69.65275, 60.884877, -69.65275, 15.83531, 'matrix(0.8413905,0,0,0.87120012,-50.722984,-48.679159)'],
]

def error(msg):
	print '\nERROR: %s\n' % msg
	sys.exit(0)

class IslandsGen(object):
	def __init__(self, options):
		self.options = options
		
		self.curr_file = 0
		self.curr_card = 0
		self.out = 0
		self.indent_count = 0
		self.seed = 0

		self.bleed = 11.25 # = 1/8"
		self.safe_margin = 11.25 # = 1/8"

		self.page_size = 246.6
		self.card_size = 225
		self.guide_height = 22.5
		
		self.draw_resource = {
			'banana': self.draw_banana,
			'coconut': self.draw_coconut,
			'fish': self.draw_fish,
			'flower': self.draw_flower,
			'squid': self.draw_squid,
			'turtle': self.draw_turtle,
			'pirate': self.draw_pirate,
			'portcircle': self.draw_port_circle,
		}
		
		self.route_style = 'display:inline;fill:none;stroke:#000000;stroke-width:2;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:0.1, 5;stroke-dashoffset:0;stroke-opacity:1'

	def write(self, str):
		self.out.write('  ' * self.indent_count)
		self.out.write(str)
	
	def write_raw(self, str):
		self.out.write(str)
	
	def indent(self, count=1):
		self.indent_count += count
	
	def outdent(self, count=1):
		self.indent_count -= count
		
	def write_header(self):
		namespaces = [
			'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
			'xmlns="http://www.w3.org/2000/svg"',
			'xmlns:cc="http://creativecommons.org/ns#"',
			'xmlns:xlink="http://www.w3.org/1999/xlink"',
			'xmlns:dc="http://purl.org/dc/elements/1.1/"',
			'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"',
			'xmlns:svg="http://www.w3.org/2000/svg"',
			'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"',
			]
		self.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
		self.write('<svg version="1.1" height="246.6" width="246.6" %s>\n' % ' '.join(namespaces))
		
		self.write('<metadata>\n')
		self.indent()
		self.write('<rdf:RDF>\n')
		self.indent()
		self.write('<cc:Work rdf:about="">\n')
		self.indent()
		self.write('<dc:format>image/svg+xml</dc:format>\n')
		self.write('<dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>\n')
		self.write('<dc:title/>\n')
		self.write('<dc:creator>\n')
		self.indent()
		self.write('<cc:Agent><dc:title>Gary Kacmarcik</dc:title></cc:Agent>\n')
		self.outdent()
		self.write('</dc:creator>\n')
		self.outdent()
		self.write('</cc:Work>\n')
		self.outdent()
		self.write('</rdf:RDF>\n')
		self.outdent()
		self.write('</metadata>\n')
		self.write('\n')
		
	def write_footer(self):
		self.write('\n')
		self.write('</svg>\n')

	def write_defs(self):
		self.write('<defs>\n')
		self.indent()

		for d in defs:
			name = d[0]
			type = d[1]
			subtype = d[2]
			if type == 'filter':
				if subtype == 'blur':
					x = d[3]
					y = d[4]
					width = d[5]
					height = d[6]
					stddev = d[7]
					self.write('<filter inkscape:collect="always" inkscape:label="%s" style="color-interpolation-filters:sRGB" id="%s" x="%f" y="%f" width="%f" height="%f">\n' % (name, name, x, y, width, height))
					self.indent()
					self.write('<feGaussianBlur inkscape:collect="always" stdDeviation="%f" />\n' % stddev)
					self.outdent()
					self.write('</filter>\n')
			if type == 'roughen':
				self.write('<filter inkscape:label="%s" style="color-interpolation-filters:sRGB" id="%s">\n' % (name, name))
				self.indent()
				if subtype == 'turbulence':
					octaves = d[3]
					freq = d[4]
					scale = d[5]
					self.write('<feTurbulence numOctaves="%d" seed="%d" type="turbulence" baseFrequency="%f" result="turb" />\n' % (octaves, self.seed, freq))
				if subtype == 'noise':
					octaves = d[3]
					freq1 = d[4]
					freq2 = d[5]
					scale = d[6]
					self.write('<feTurbulence numOctaves="%d" seed="%d" type="fractalNoise" baseFrequency="%f %f" result="turb" />\n' % (octaves, self.seed, freq1, freq2))
				self.write('<feDisplacementMap scale="%f" yChannelSelector="G" xChannelSelector="R" in="SourceGraphic" in2="turb" />\n' % scale)
				self.outdent()
				self.write('</filter>\n')
			if type == 'gradient':
				if subtype == 'stops':
					stops = d[3]
					self.write('<linearGradient id="%s" inkscape:collect="always">\n' % name)
					self.indent()
					for stop in stops:
						self.write('<stop offset="%f" style="stop-color:#%s;stop-opacity:%f" />\n' % (stop[0], stop[1], stop[2]))
					self.outdent()
					self.write('</linearGradient>\n')
				if subtype == 'linear':
					xlink = d[3]
					x1 = d[4]
					y1 = d[5]
					x2 = d[6]
					y2 = d[7]
					transform = d[8]
					tag = '<linearGradient id="%s" xlink:href="#%s" x1="%f" y1="%f" x2="%f" y2="%f" ' % (name, xlink, x1, y1, x2, y2)
					if transform != '':
						tag += 'gradientTransform="%s" ' % transform
					tag += 'gradientUnits="userSpaceOnUse" inkscape:collect="always" />\n'
					self.write(tag)
				if subtype == 'radial':
					xlink = d[3]
					cx = d[4]
					cy = d[5]
					fx = d[6]
					fy = d[7]
					r = d[8]
					transform = d[9]
					self.write('<radialGradient id="%s" xlink:href="#%s" cx="%f" cy="%f" fx="%f" fy="%f" r="%f" gradientUnits="userSpaceOnUse" gradientTransform="%s" inkscape:collect="always" />\n' % (name, xlink, cx, cy, fx, fy, r, transform))
			if type == 'texture':
				octaves = d[2]
				freq = d[3]
				blur = d[4]
				self.write('<filter inkscape:label="%s" style="color-interpolation-filters:sRGB" id="%s">\n' % (name, name))
				self.indent()
				self.write('<feTurbulence numOctaves="%d" seed="%d" type="turbulence" baseFrequency="%f" result="result1" />\n' % (octaves, self.seed, freq))
				self.write('<feColorMatrix result="result0" in="SourceGraphic" type="luminanceToAlpha" />\n')
				self.write('<feColorMatrix result="result2" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0.4 0 " />\n')
				self.write('<feComposite in="result2" operator="over" in2="result1" />\n')
				self.write('<feColorMatrix result="result91" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 10 -4 " />\n')
				self.write('<feComposite operator="out" in="SourceGraphic" in2="result91" />\n')
				self.write('<feGaussianBlur stdDeviation="%f" />\n' % blur)
				self.write('<feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 " />\n')
				self.outdent()
				self.write('</filter>\n')

		self.outdent()
		self.write('</defs>\n')
		self.write('\n')

	def write_named_view(self):
		self.write('<sodipodi:namedview\n')
		self.indent(2)
		self.write('id="base"\n')
		self.write('pagecolor="#ffffff"\n')
		self.write('bordercolor="#666666"\n')
		self.write('borderopacity="1.0"\n')
		self.write('inkscape:pageopacity="0.0"\n')
		self.write('inkscape:pageshadow="2"\n')
		self.write('inkscape:zoom="2"\n')
		self.write('inkscape:cx="115.37643"\n')
		self.write('inkscape:cy="285.04449"\n')
		self.write('inkscape:document-units="in"\n')
		self.write('showgrid="true"\n')
		self.write('units="in"\n')
		self.write('inkscape:window-width="1392"\n')
		self.write('inkscape:window-height="836"\n')
		self.write('inkscape:window-x="39"\n')
		self.write('inkscape:window-y="6"\n')
		self.write('inkscape:window-maximized="0"\n')
		self.write('inkscape:snap-grids="true"\n')
		self.write('inkscape:snap-to-guides="true"\n')
		self.write('inkscape:snap-nodes="true"\n')
		self.write('inkscape:object-nodes="true"\n')
		self.write('inkscape:snap-smooth-nodes="true"\n')
		self.write('inkscape:snap-intersection-paths="true"\n')
		self.write('inkscape:object-paths="true"\n')
		self.write('inkscape:snap-bbox="true"\n')
		self.write('inkscape:bbox-nodes="true"\n')
		self.write('inkscape:snap-others="true"\n')
		self.write('inkscape:bbox-paths="false"\n')
		self.write('inkscape:snap-global="true" >\n')
		self.outdent()
		
		self.write('<inkscape:grid\n')
		self.indent()
		self.write('type="xygrid"\n')
		self.write('id="grid3051"\n')
		self.write('empspacing="2"\n')
		self.write('visible="true"\n')
		self.write('enabled="true"\n')
		self.write('snapvisiblegridlinesonly="true"\n')
		self.write('spacingx="0.0625in"\n')
		self.write('spacingy="0.0625in"\n')
		self.write('dotted="false"\n')
		self.write('units="in" />\n')
		self.outdent(2)
		self.write('</sodipodi:namedview>\n')

	def start_layer(self, id, label, hidden=False, locked=True):
		tag = '<g inkscape:groupmode="layer" id="%s" inkscape:label="%s" ' % (id, label)
		if hidden:
			tag += 'style="display:none" '
		else:
			tag += 'style="display:inline" '
		if locked:
			tag += 'sodipodi:insensitive="true" '
		tag += '>\n'
		self.write(tag)
		self.indent()
		
	def end_layer(self):
		self.outdent()
		self.write('</g>\n')
	
	def start_group(self, id='', style='', transform=''):
		tag = '<g '
		if id != '':
			tag += 'id="%s" ' % id
		if style != '':
			tag += 'style="%s" ' % style
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '>\n'
		self.write(tag)
		self.indent()

	def end_group(self):
		self.outdent()
		self.write('</g>\n')
		
	def write_path(self, style, path, id='', transform=''):
		tag = '<path '
		if id != '':
			tag += 'id="%s" ' % id
		if style != '':
			tag += 'style="%s" ' % style
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += 'd="%s" ' % path
		tag += 'inkscape:connector-curvature="0" />\n'
		self.write(tag)
	
	def write_clone(self, link, style):
		self.write('<use xlink:href="#%s" height="100%%" width="100%%" x="0" y="0" style="%s" />\n' % (link, style))

	def write_rect(self, style, x, y, width, height, transform=''):
		tag = '<rect x="%f" y="%f" width="%f" height="%f" style="%s" ' % (x, y, width, height, style)
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write(tag)
	
	def write_circle(self, style, cx, cy, r, transform=''):
		tag = '<circle cx="%f" cy="%f" r="%f" style="%s" ' % (cx, cy, r, style)
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write(tag)
	
	def write_ellipse(self, style, cx, cy, rx, ry, transform=''):
		tag = '<ellipse cx="%f" cy="%f" rx="%f" ry="%f" style="%s" ' % (cx, cy, rx, ry, style)
		if transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write(tag)
	
	def draw_card(self, name, data):
		filename = data[0]
		borders = data[1]
		shallow_water_path = data[2]
		deep_water_path = data[3]
		shoreline_path = data[4]
		grass_path = data[5]
		forest_path = data[6]
		routes_path = data[7]
		textpaths = data[8]
		resources = data[9]

		self.write_defs()
		self.write_named_view()
		
		self.draw_water_layer()		
		self.draw_shallow_water_layer(shallow_water_path)
		self.draw_deep_water_layer(deep_water_path)
		self.draw_shoreline_layers(shoreline_path)
		self.draw_grass_layers(grass_path)
		self.draw_forest_layers(forest_path)
		self.draw_routes_layers(routes_path)
		self.draw_labels_layer(textpaths)
		self.draw_resources_layer(resources)
		
		self.draw_guides(borders)
		self.draw_border_layers()

	def draw_water_layer(self):
		self.start_layer('water_layer', 'Water')
		style = 'fill:#b9deff;fill-opacity:1;stroke:none'
		self.write('<rect id="water" style="%s" x="0" y="0" width="246.6" height="246.6" />\n' % style)
		self.end_layer()

	def draw_shallow_water_layer(self, path):
		self.start_layer('water_medium_layer', 'Water Shallow')
		filter = 'blurWaterShallow'
		style = 'fill:#9bd1ff;fill-opacity:0.70;fill-rule:evenodd;stroke:none;filter:url(#%s)' % filter
		self.write_path(style, path)
		self.end_layer()

	def draw_deep_water_layer(self, path):
		self.start_layer('water_deep_layer', 'Water Deep')
		filter = 'blurWaterDeep'
		style = 'fill:#87c8ff;fill-opacity:0.60;fill-rule:evenodd;stroke:none;filter:url(#%s)' % filter
		self.write_path(style, path)
		self.end_layer()
	
	def draw_shoreline_layers(self, path):
		self.start_layer('water_hilight_layer', 'Water Hilight')
		filter = 'blurWaterHilight'
		style = 'display:inline;fill:#ffffff;fill-opacity:1;stroke:#ffffff;stroke-opacity:1;filter:url(#%s)' % filter
		self.write_clone('shoreline', style)
		self.end_layer()
	
		self.start_layer('land_layer', 'Land')
		style = 'display:inline;fill:#ffddab;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
		self.write_clone('shoreline', style)
		self.end_layer()
	
		self.start_layer('land_texture_layer', 'Land Texture')
		filter = 'textureLand'
		style = 'display:inline;fill:#ffca7d;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;filter:url(#%s)' % filter
		self.write_clone('shoreline', style)
		self.end_layer()
	
		self.start_layer('shoreline_layer', 'Shoreline')
		style = 'display:inline;fill:none;fill-opacity:1;stroke:#5f4c14;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
		self.write_clone('shoreline', style)
		self.end_layer()
	
		self.start_layer('shoreline_master_layer', 'Shoreline Master', hidden=True)
		filter = 'roughenShoreline'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill-opacity:1;fill-rule:evenodd;filter:url(#%s);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate' % filter
		self.write_path(style, path, id='shoreline')
		self.end_layer()

	def draw_grass_layers(self, path):
		self.start_layer('grass_layer', 'Grass')
		style = 'display:inline;fill:#b4e982;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
		self.write_clone('grass', style)
		self.end_layer()
	
		self.start_layer('grass_texture_big_layer', 'Grass Texture Big')
		filter = 'textureGrassBig'
		style = 'display:inline;fill:#a7e46a;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;filter:url(#%s)' % filter
		self.write_clone('grass', style)
		self.end_layer()
	
		self.start_layer('grass_texture_small_layer', 'Grass Texture Small')
		filter = 'textureGrassSmall'
		style = 'display:inline;fill:#8cdd3d;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;filter:url(#%s)' % filter
		self.write_clone('grass', style)
		self.end_layer()
	
		self.start_layer('grass_master_layer', 'Grass Master', hidden=True)
		filter = 'blurGrass'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill-opacity:1;fill-rule:evenodd;filter:url(#%s);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate' % filter
		#style = 'color:#000000;display:inline;overflow:visible;visibility:visible;fill:#b4e982;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:1, 2;stroke-dashoffset:0;stroke-opacity:1;marker:none;filter:url(#%s);enable-background:accumulate' % filter
		self.write_path(style, path, id='grass')
		self.end_layer()

	def draw_forest_layers(self, path):
		outline_filter = 'roughenForest'

		self.start_layer('forest_shadow_layer', 'Forest Shadow')
		self.start_group(style='filter:url(#blurForestShadow)')
		style = 'display:inline;opacity:0.75;fill:#258c1b;fill-opacity:1;filter:url(#%s)' % outline_filter
		self.write_clone('forest', style)
		self.end_group()
		self.end_layer()
		
		self.start_layer('forest_fill_layer', 'Forest Fill')
		style = 'fill:#83d700;fill-opacity:1;stroke:none;stroke-width:1.5;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;filter:url(#%s)' % outline_filter
		self.write_clone('forest', style)
		self.end_layer()
		
		self.start_layer('forest_texture_big_layer', 'Forest Texture Big')
		self.start_group(style='filter:url(#textureForestBig)')
		style = 'fill:#548c00;fill-opacity:1;stroke:none;stroke-width:1.5;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;filter:url(#%s)' % outline_filter
		self.write_clone('forest', style)
		self.end_group()
		self.end_layer()
		
		self.start_layer('forest_texture_small_layer', 'Forest Texture Small')
		self.start_group(style='filter:url(#textureForestSmall)')
		style = 'fill:#78c125;fill-opacity:1;stroke:none;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;filter:url(#%s)' % outline_filter
		self.write_clone('forest', style)
		self.end_group()
		self.end_layer()
	
		self.start_layer('forest_outline_layer', 'Forest Outline')
		style = 'fill:none;fill-opacity:1;stroke:#006800;stroke-width:1.5;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;filter:url(#%s)' % outline_filter
		self.write_clone('forest', style)
		self.end_layer()

		self.start_layer('forest_master_layer', 'Forest Master', hidden=True)
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill-opacity:1;fill-rule:nonzero;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, path, id='forest')
		self.end_layer()
	
	def draw_routes_layers(self, path):
		self.start_layer('routes_layer', 'Routes')
		self.write_path(self.route_style, path)
		self.end_layer()
	
	def normalize_name(self, name):
		norm = name.lower().replace(' ', '_')
		norm = re.sub("[.'-]", '', norm)
		norm = re.sub('â', 'a', norm)
		norm = re.sub('é', 'e', norm)
		if not re.match('^[a-z_]+$', norm):
			error('Invalid id name: %s' % norm)
		return norm

	def draw_labels_layer(self, textpath):
		text = textpath[0]
		path = textpath[1]

		self.start_layer('labels_layer', 'Labels')
		style = "font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:10px;line-height:125%;font-family:CCTreasureTrove;-inkscape-font-specification:'CCTreasureTrove, Normal';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;display:inline;fill:#5d481b;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
		self.write('<text xml:space="preserve" style="%s"><textPath xlink:href="#label-path"\n' % style)
		#style = "-inkscape-font-specification:'CCTreasureTroveAged Mod, Normal';font-family:'CCTreasureTroveAged Mod';font-weight:normal;font-style:normal;font-stretch:normal;font-variant:normal;font-size:8.75px;text-anchor:start;text-align:start;writing-mode:lr;line-height:125%"
		#self.write('style="%s"\n' % style)
		self.write('>%s</textPath></text>\n' % text)
		self.end_layer()
		
		self.start_layer('labels_guide_layer', 'Labels Guide', hidden=True)
		style = 'color:#000000;fill:none;stroke:#000000;stroke-width:1;stroke-opacity:1'
		self.write_path(style, path, id='label-path')
		self.end_layer()

	def draw_resources_layer(self, resources):
		self.start_layer('resources_layer', 'Resources')
		for r in resources:
			type = r[0]
			transform = r[1]
			self.draw_resource[type](id='resource-%s' % type, transform=transform)
		self.end_layer()
			
	def draw_guides(self, guides):
		guide_transform = [
			'',
			'matrix(0,1,-1,0,%g,0)' % (self.page_size),
			'matrix(-1,0,0,-1,%g,%g)' % (self.page_size, self.page_size),
			'matrix(0,-1,1,0,0,%g)' % (self.page_size),
		]

		self.start_layer('edge_guides_layer', 'Edges', hidden=hide_guides)
		for i in xrange(0, 4):
			g = guides[i]
			self.draw_guide(i, g, guide_transform[i])
		self.end_layer()

	def draw_guide_route(self, percent):
		x = self.card_size * percent
		x += self.bleed
		self.write_path(self.route_style, 'm %g,0 0,%g' % (x, -self.guide_height))

	def draw_guide(self, id, pattern, transform):
		land_style = 'fill:#ffd291;stroke:#000000;stroke-width:0.9'
		grass_style = 'fill:#b4e982;stroke:#000000;stroke-width:0.9'
		forest_style = 'fill:#5adc4f;stroke:#000000;stroke-width:0.9'
		shallow_water_style = 'fill:#b9deff;stroke:#000000;stroke-width:0.9'
		water_style = 'fill:#9bceff;stroke:#000000;stroke-width:0.9'
		deep_water_style = 'fill:#73baff;stroke:#000000;stroke-width:0.9'

		width = self.page_size
		height = self.guide_height
		land1 = self.bleed + 78.875
		land2 = self.bleed + 153.625
		grass1 = self.bleed + 71.250
		grass2 = self.bleed + 136.75
		forest1 = self.bleed + 56.375
		forest2_space = 11.25
		forest2a = self.bleed + 32.25
		forest2b = self.bleed + 28.25
		forest2c = self.bleed + 38.25
		forest3 = self.bleed + 106.786

		shallow_water2 = width - land1
		shallow_water1 = width - land2
		water2 = self.bleed + 103.250
		water1 = self.bleed + 47.375
		deep_water2 = self.bleed + 55
		deep_water1 = self.bleed + 25.250

		self.start_group(id='guide%d-%d' % (id, pattern), transform=transform)
		
		if pattern == 0:
			self.write_rect(deep_water_style, 0, -height, width, height)
			self.draw_guide_route(0.5)
			
		if pattern == 1:
			self.write_rect(land_style, width - land1, -height, land1, height)
			self.write_rect(grass_style, width - grass1, -height, grass1, height)
			self.write_rect(forest_style, width - forest1, -height, forest1, height)
			self.write_rect(shallow_water_style, 0, -height, shallow_water2, height)
			self.write_rect(water_style, 0, -height, water2, height)
			self.write_rect(deep_water_style, 0, -height, deep_water2, height)
			self.draw_guide_route(1.0/3.0)

		if pattern == 3:
			self.write_rect(land_style, width - land2, -height, land2, height)
			self.write_rect(grass_style, width - grass2, -height, grass2, height)
			forest_offset = width - forest2a
			self.write_rect(forest_style, forest_offset, -height, forest2a, height)
			forest_offset -= forest2_space + forest2b
			self.write_rect(forest_style, forest_offset, -height, forest2b, height)
			forest_offset -= forest2_space + forest2c
			self.write_rect(forest_style, forest_offset, -height, forest2c, height)
			self.write_rect(shallow_water_style, 0, -height, shallow_water1, height)
			self.write_rect(water_style, 0, -height, water1, height)
			self.write_rect(deep_water_style, 0, -height, deep_water1, height)
			self.draw_guide_route(2.0/3.0)

		if pattern == 4:
			self.write_rect(land_style, 0, -height, land1, height)
			self.write_rect(grass_style, 0, -height, grass1, height)
			self.write_rect(forest_style, 0, -height, forest1, height)
			self.write_rect(shallow_water_style, width - shallow_water2, -height, shallow_water2, height)
			self.write_rect(water_style, width - water2, -height, water2, height)
			self.write_rect(deep_water_style, width - deep_water2, -height, deep_water2, height)
			self.draw_guide_route(2.0/3.0)

		if pattern == 6:
			self.write_rect(land_style, 0, -height, land2, height)
			self.write_rect(grass_style, 0, -height, grass2, height)
			forest_offset = 0
			self.write_rect(forest_style, forest_offset, -height, forest2a, height)
			forest_offset += forest2_space + forest2a
			self.write_rect(forest_style, forest_offset, -height, forest2b, height)
			forest_offset += forest2_space + forest2b
			self.write_rect(forest_style, forest_offset, -height, forest2c, height)
			self.write_rect(shallow_water_style, width - shallow_water1, -height, shallow_water1, height)
			self.write_rect(water_style, width - water1, -height, water1, height)
			self.write_rect(deep_water_style, width - deep_water1, -height, deep_water1, height)
			self.draw_guide_route(1.0/3.0)

		if pattern == 7:
			self.write_rect(grass_style, 0, -height, width, height)
			self.write_rect(forest_style, 0, -height, forest3, height)
			self.write_rect(forest_style, width - forest3, -height, forest3, height)
			self.draw_guide_route(0.5)

		self.end_group()

	def draw_border_layers(self):
		style = 'fill:none;stroke:#000000;stroke-width:0.5;stroke-linecap:butt;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'

		self.start_layer('cut_layer', 'Cut Line', hidden=hide_guides)
		self.write('<rect style="%s" width="224.5" height="224.5" x="11.25" y="11.25" ry="11.338962" />\n' % style)
		self.end_layer()
	
		self.start_layer('page_border_layer', 'Page Border', hidden=hide_guides)
		self.write('<rect style="%s" width="246.6" height="246.6" x="0" y="0" />\n' % style)
		self.end_layer()

	# Resources

	def draw_turtle(self, id='', transform=''):
		self.start_group(id=id, transform=transform)

		style = 'fill:#acf398;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
		# Left Rear Flipper
		self.write_path(style, 'm -13.200987,-100.29637 c 0.383554,0.976603 3.233916,-2.12106 6.131249,-1.42702 1.332863,0.31928 0.882122,-3.09205 -0.399356,-3.57815 -2.371651,-0.89961 -6.659154,2.64419 -5.731893,5.00517 z')
		# Right Rear Flipper
		self.write_path(style, 'm 0.519205,-98.947277 c -1.160888,-0.35295 2.907731,-2.472353 3.949394,-1.850123 1.642844,0.981343 2.297204,4.963396 0.372373,6.157721 -0.745218,0.462395 -0.785725,-3.232509 -4.321767,-4.307598 z')
		# Right Front Flipper
		self.write_path(style, 'm 7.618715,-114.43269 c 1.934345,-0.44611 4.329746,-0.0993 5.914203,1.00302 2.013049,1.40054 2.917028,5.29708 1.897177,7.52728 -0.282844,0.61852 -3.514643,-5.32749 -6.150465,-4.42389 -1.839455,0.63059 -2.536626,0.15372 -3.169919,-1.68481 -0.27477,-0.79769 0.686895,-2.232 1.509004,-2.4216 z')
		# Left Front Flipper
		self.write_path(style, 'm -13.605402,-118.51893 c 1.434388,-2.65109 5.159923,-3.50053 7.13722,-3.29637 1.742717,0.17994 3.474416,1.88524 3.953288,3.57051 0.312727,1.10056 -0.218032,2.84568 -1.315095,3.17046 -1.558665,0.46144 -1.358953,-1.39147 -2.644475,-2.38636 -2.809563,-2.17437 -7.671044,-0.06 -7.130938,-1.05824 z')
		# Head
		self.write_path(style, 'm 1.574508,-116.64822 c -0.973346,-1.40454 -0.400278,-3.52894 -0.15625,-5.22027 0.277861,-1.92582 2.436935,-3.39132 3.77573,-3.50612 0.998071,-0.0856 1.511263,0.0552 2.026651,0.91421 0.545706,0.90951 1.17564,3.12771 0.125,4.74448 -0.918312,1.41314 -1.826689,3.21256 -3.442704,3.69086 -0.965518,0.28577 -1.75489,0.20445 -2.328427,-0.62316 z')
		# Tail
		self.write_path(style, 'm -4.37156,-100.05265 c -1.568711,0.833903 -1.519982,4.156989 -0.84283,4.365801 0.803045,0.247633 2.774585,-2.210096 2.390927,-3.815868 -0.20218,-0.846213 -0.779871,-0.958313 -1.548097,-0.549933 z')
		# Shell
		self.write_path(style, 'm -7.212243,-116.3836 c 1.293667,-1.65845 3.629584,-2.72772 5.073491,-2.91682 3.87448,-0.50741 7.329249,0.88026 10.076271,3.65928 1.485686,1.503 2.189594,3.9511 1.909189,6.04576 -0.610927,4.56371 -3.547497,9.21538 -7.477655,11.614241 -1.864758,1.138194 -4.454815,1.340084 -6.523059,0.636396 -2.202234,-0.749276 -4.339874,-2.571424 -5.09117,-4.772977 -1.613498,-4.72808 -1.039758,-10.32676 2.032933,-14.26588 z')

		# Shell pattern
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:none;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.63;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, 'm -2.061438,-117.34644 -0.59283,-1.87446 m 9.785218,5.41 1.414213,-0.83969 m -3.270369,-3.0494 -0.883883,1.45841 m -3.005204,-2.91681 -0.322303,1.63785 m -4.980998,18.116938 -0.637024,1.851254 m 3.244481,-1.320924 0.145526,1.908392 m -5.139468,-3.85294 -1.276269,1.089694 m 0.0491,-3.679294 -1.793656,0.57452 m 1.06066,-3.30874 -1.531171,0.15311 m 1.679379,-3.00521 -1.861517,-0.2134 m 2.347653,-2.30567 -1.656171,-0.60309 m 2.761025,-2.09275 -1.312881,-0.89415 m 3.166356,-0.9571 -1.315562,-1.55438 m 7.32865,17.857125 0.826745,1.744559 m 1.382964,-3.026194 1.087008,1.317787 m 0.636565,-3.615877 1.440561,1.09413 m 0.238817,-3.48062 1.396368,0.61558 m -0.582567,-3.29357 1.567783,0.29327 m -1.419575,-3.1217 1.723572,-0.18483 m -10.817309,9.66873 0.486136,2.607453 m -4.02167,-3.756503 -1.59099,1.28163 m 5.833631,-13.21406 -0.309359,-2.38648 m 4.507806,3.7565 1.856155,-1.59099 m -10.69499,9.8553 -2.740039,-0.13258 m 3.447145,-3.88908 -3.18198,-1.23745 m 4.861359,-3.22617 -2.607456,-1.45841 m 6.452349,12.1534 2.209709,1.45841 m -0.04419,-5.03814 3.049398,1.19324 m -1.635185,-5.34749 2.872622,0.70711 m -9.766913,-0.83968 -0.486137,-2.78425 2.298097,-1.10485 4.021672,1.41421 0.839688,2.65165 -2.298097,1.19325 z m 4.507806,1.28162 0.928077,3.04939 -2.607455,1.28164 m -4.198448,-1.32583 -0.839689,-2.51907 2.298097,-1.76776 m -2.474873,7.95495 -0.574524,-2.34229 1.546796,-1.19324 4.154252,1.19324 0.530329,2.34229 -2.165513,1.19324 z m 3.310975,-14.48201 c -9.036509,1.02413 -9.686118,18.911215 0.316406,18.4082 7.293571,-1.28851 13.245425,-14.43065 4.082031,-17.65234 -1.373439,-0.61154 -2.89993,-0.86992 -4.398437,-0.75586 z')

		# Eyes
		style = 'fill:#000000;fill-opacity:1;stroke:none'
		self.write_ellipse(style, -83.675232, -91.031174, 0.39348665, 0.53721493, transform='matrix(0.71262218,0.70154802,-0.70154802,0.71262218,0,0)')
		self.write_ellipse(style, 0.87644225, -122.84991, 0.39348665, 0.53721493, transform='matrix(0.99895236,0.04576232,-0.04576232,0.99895236,0,0)')

		self.end_group()

	def draw_squid(self, id='', transform=''):
		self.start_group(id=id, transform=transform)

		# White body fill.
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#ffffff;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, 'm 3.751377,-125.43036 -1.988737,1.32582 -2.342292,2.2981 -1.988737,2.43068 -1.104855,2.2981 -0.707107,1.90035 0,1.14905 1.679379,0 -0.397747,1.98873 -0.574525,2.47488 -0.08839,2.34229 -0.08839,1.72357 0.839689,0.70711 1.767767,0.39775 1.856155,0.0442 1.414214,-0.17678 1.414213,-0.57453 0.309359,-0.83968 0.30936,-2.3423 -0.30936,-2.69584 -0.176776,-2.65165 1.723573,0.53033 0.04419,-2.20971 -0.220971,-3.7565 -0.397748,-3.27037 z')

		style = 'fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'
		self.write_path(style, 'm -11.427734,-116.71094 c -0.926654,0.068 -1.828354,0.58 -2.47461,0.98633 l 0.564453,0.62305 c 0.129027,-0.0692 1.250128,-0.8819 2,-0.93164 0.346707,-0.0382 0.804167,0.0783 1.076172,0.39453 0.868797,0.83085 0.783149,2.35847 0.419922,4.20312 -0.329865,1.37596 -0.389964,2.87205 -0.115234,4.36719 0.175945,1.03446 0.565056,2.09121 1.236328,2.96484 0.238071,-0.17566 0.474836,-0.35332 0.707031,-0.53906 0.01663,-0.0136 0.035924,-0.0238 0.052734,-0.0371 -0.6103851,-0.73211 -0.9647481,-1.69528 -1.1601561,-2.53906 -0.328551,-1.46718 -0.279657,-2.86872 -0.0332,-4.05078 0.451937,-2.07874 0.307063,-3.74395 -0.642578,-4.80469 -0.4323489,-0.47732 -1.0683939,-0.67465 -1.6308589,-0.63672 z')
		self.write_path(style, 'm -3.796875,-104.89258 c -0.9058673,0.74517 -1.9188533,1.2608 -2.7324219,1.16406 -0.2030019,0.0833 -0.4030106,0.17309 -0.5839843,0.29102 -0.166691,0.11469 -0.3464295,0.21948 -0.5195313,0.33008 1.7036649,0.94245 3.731315,0.084 4.8828125,-1.03906 -0.3560506,-0.22586 -0.7057338,-0.47583 -1.046875,-0.7461 z')
		self.write_path(style, 'm 4.1640625,-105.46289 c -0.327423,-0.0235 -0.6594367,-0.0232 -0.9921875,0.002 0.078825,0.37091 0.1521001,0.74306 0.2207031,1.11524 1.064043,-0.1503 2.1844576,0.0295 3.203125,0.45898 0.5236021,0.21983 1.046713,0.50703 1.5820313,0.79883 0.1250671,-0.19964 0.2209286,-0.4272 0.3164062,-0.65625 -0.4965073,-0.32152 -0.99925,-0.64667 -1.5488281,-0.92969 -0.8521322,-0.43734 -1.7989811,-0.71849 -2.78125,-0.78906 z')
		self.write_path(style, 'm 9.625,-103.05469 c -0.082921,0.19334 -0.1803086,0.37972 -0.2832031,0.56446 1.0688811,0.48073 2.1976941,0.84215 3.3593751,1.0332 0.499799,0.10355 1.072452,0.1837 1.636719,0.125 0.45283,-0.10452 0.877972,-0.29289 1.207031,-0.60938 -0.854133,0.55171 -1.887915,0.33226 -2.777344,0.11524 -1.10459,-0.26639 -2.156407,-0.6956 -3.142578,-1.22852 z')
		self.write_path(style, 'm 10.445312,-116.39648 c -0.400021,0.0106 -0.806202,0.0811 -1.207031,0.23632 -0.999585,0.47508 -1.487003,1.70748 -1.054687,2.81641 0.73612,1.87741 1.421348,4.07068 1.230468,6.24023 -0.185513,1.89331 -0.460829,3.94627 -1.800781,5.00196 -0.0014,0.001 -0.0025,0.003 -0.0039,0.004 0.320059,0.10607 0.638919,0.21521 0.96875,0.33985 1.230198,-1.44937 1.504195,-3.41815 1.582031,-5.29297 0.119976,-2.35443 -0.620703,-4.61346 -1.384765,-6.52539 -0.32491,-0.80541 0.06377,-1.75045 0.714844,-1.97071 1.477232,-0.63585 3.318013,0.63156 3.894531,1.04493 0.06075,-0.3217 0.119158,-0.65295 0.167968,-0.99219 -0.763734,-0.42041 -1.907357,-0.9341 -3.107422,-0.90234 z')
		self.write_path(style, 'm 2.6855469,-104.19922 -1.3144531,0.16406 c 0.1478645,1.11047 0.8672943,2.90093 2.7285156,3.58399 1.0655975,0.34295 2.2839122,0.21217 3.3339844,-0.36719 -0.2485489,-0.0678 -0.4969496,-0.13368 -0.75,-0.21289 -0.00137,0 -0.00254,-0.002 -0.00391,-0.002 0,0 -0.00195,0 -0.00195,0 -0.3131724,-0.0869 -0.6261833,-0.19311 -0.9375,-0.31055 -0.4385291,0.0409 -0.8692013,-0.007 -1.2519532,-0.16992 -1.067961,-0.37978 -1.6828409,-1.60142 -1.8027343,-2.68555 z')
		self.write_path(style, 'm -0.46875,-103.85156 c -0.37846744,0.0176 -0.7557959,0.0342 -1.1347656,0.0508 -0.026644,1.35579 -0.083772,2.68828 -0.4941406,3.89453 -0.018811,0.05778 -0.047295,0.112792 -0.068359,0.169922 0.0012,0.469321 0.048794,0.930808 0.1503906,1.380859 0.2763156,-0.394741 0.5250997,-0.814331 0.7148438,-1.271484 0.55095568,-1.351977 0.7212245,-2.820157 0.8320312,-4.224607 z')
		self.write_path(style, 'm -3.1230469,-98.044922 c -0.150339,0.197077 -0.3095867,0.389682 -0.4746093,0.578125 -0.714018,0.796578 -1.6209216,1.450225 -2.6289063,1.658203 -0.2940814,0.05997 -0.6139042,0.05055 -0.90625,-0.02344 -0.4427004,-0.04353 -0.8708449,-0.242919 -1.1113281,-0.654297 0.2442222,0.763823 1.2067903,1.184368 2.09375,1.060547 1.1279747,-0.158128 2.18429,-0.790581 3.0175781,-1.617188 0.093062,-0.09152 0.1811077,-0.189952 0.2714844,-0.285156 -0.1018651,-0.234524 -0.1860307,-0.474028 -0.2617188,-0.716797 z')
		self.write_path(style, 'm 4.025391,-125.87891 c -0.146221,-0.0305 -0.303081,0.0119 -0.398438,0.0742 -2.862666,1.87054 -4.880211,3.59029 -6.738281,6.62891 -0.99964,1.72264 -1.777144,3.35668 -1.810547,5.28516 0.006,0.2998 0.273432,0.52657 0.570313,0.48437 0.492456,-0.0709 0.875763,-0.10517 1.1875,-0.1289 -0.218167,0.7447 -0.421021,1.51009 -0.605469,2.3496 -0.397611,1.80973 -0.653445,4.36221 -0.396485,5.81446 0.19055,1.07692 1.186538,1.26127 1.898438,1.47656 0.7119,0.21529 1.794338,0.36669 2.455078,0.27539 1.69421,-0.23411 3.402492,-0.48676 3.824219,-1.49023 0.761046,-1.81087 0.168822,-5.57059 0.01758,-7.99219 0.372935,0.0863 0.744619,0.19639 1.097656,0.36523 0.33685,0.16216 0.647892,-0.0794 0.638672,-0.45312 0,0 -0.123941,-4.19409 -0.244141,-5.86719 -0.19297,-2.68575 -0.356893,-3.69695 -1.158203,-6.45703 -0.0561,-0.23143 -0.19167,-0.33476 -0.33789,-0.36523 z m -0.402344,0.98243 c 0.58883,2.15877 0.873399,3.54998 1.042969,5.91015 0.10223,1.42282 0.178435,4.57706 0.197265,5.32227 -0.75389,-0.22738 -1.480374,-0.38819 -2.083984,-0.44727 0.003,-0.93743 0.01185,-2.67282 0.09375,-4.53515 0.0553,-1.25832 -0.308848,-0.55533 -0.486328,0.38671 -0.38009,2.01743 -0.460938,3.48013 -0.460938,4.40821 -4e-4,0.25604 0.192656,0.47102 0.447266,0.49804 0.246719,0.026 0.520253,0.0702 0.785156,0.10547 0.293188,2.53888 0.74607,5.39541 0.132813,7.61133 -0.202142,0.73041 -3.4124,1.1779 -5.269532,0.78516 -0.518246,-0.1096 -1.363176,-0.31092 -1.404296,-1.08594 -0.0867,-1.63376 0.06432,-3.31607 0.320312,-4.73438 0.389151,-2.15602 1.088748,-4.27614 1.673828,-5.69726 l 0.941406,-2.46289 c 0.56898,-1.4466 0.362088,-1.65162 -0.632812,0.10156 -0.761329,1.50777 -1.310471,2.82853 -1.765625,4.1875 -0.192605,0.0238 -0.6893,0.0859 -1.246094,0.1543 0.0825,-0.52387 0.194473,-1.14129 0.470703,-1.9043 0.35929,-0.99241 0.811648,-1.98486 1.080078,-2.42383 1.64411,-2.6887 3.560553,-4.51162 6.164063,-6.17968 z')
		self.write_path(style, 'm -2.5373427,-104.18887 c 0.3421635,0.16215 0.6859607,0.32221 1.0313325,0.48012 -0.9340133,2.13702 -1.3535777,4.738056 -0.2199471,6.841436 0,0 -1e-7,10e-7 -1e-7,10e-7 0.4977108,0.912316 0.5028499,2.106189 -0.1345524,2.837592 -4e-7,0 -4e-7,0 -4e-7,0 -0.5079821,0.590086 -1.4642213,0.666608 -1.9748687,0.199639 0.5287582,0.326069 1.2462055,0.121597 1.5702851,-0.288591 0.041842,-0.04156 0.079462,-0.08658 0.111943,-0.134807 0.4857643,-0.603214 0.3594186,-1.599406 -0.074296,-2.305366 -10e-8,0 -10e-8,0 -10e-8,0 -1.4089532,-2.272798 -1.2397643,-5.211664 -0.3098958,-7.630024 z')
		self.write_path(style, 'm 2.3835041,-104.06671 c 0.3174615,-0.24063 0.6405059,-0.47527 0.9692112,-0.70375 0.6369547,1.29737 2.1141119,2.13063 3.6421499,2.7018 1.3112305,0.45566 2.9095093,0.83787 3.7952238,2.02156 0,0 0,0 0,0 0.5932,0.800014 0.736953,1.955226 0.161314,2.691399 -0.466912,0.602328 -1.3710736,0.816403 -1.952572,0.446967 0.6368576,0.257218 1.383809,-0.137615 1.639232,-0.653144 -2e-6,3e-6 0.0051,-0.0078 0.0051,-0.0078 0.434378,-0.572556 0.19779,-1.510827 -0.294284,-2.118239 0,0 0,-10e-7 0,-10e-7 -0.7344896,-0.948692 -2.2010381,-1.119902 -3.6049445,-1.560132 -1.6380276,-0.45356 -3.3202746,-1.28178 -4.3604604,-2.81866 z')
		self.write_path(style, 'm -3.2239027,-105.35575 -0.4962606,1.35092 c -1.0480932,-0.46063 -2.4787863,-0.29871 -3.5206168,0.38222 0,0 -3e-7,0 -3e-7,0 -1.3656955,0.93961 -2.9325976,1.77851 -4.6273276,1.94569 0,0 -1e-6,0 -1e-6,0 -0.765571,0.0695 -1.508698,-0.0986 -2.185433,-0.35854 -0.608035,-0.2156 -1.286316,-0.55176 -1.572326,-1.1699 0.158398,0.10812 0.317934,0.17056 0.477991,0.20184 0.313188,0.27579 0.779492,0.42426 1.22658,0.5645 0.660228,0.18101 1.343102,0.27459 1.967694,0.15219 0,0 10e-7,0 10e-7,0 1.508118,-0.2724 2.8419377,-1.18921 4.0822788,-2.18158 0,0 5e-7,0 5e-7,0 1.2448518,-1.01542 3.0322554,-1.4126 4.64742,-0.88734 z')
		self.write_path(style, 'm 1.6621094,-103.86719 c -0.4185714,0.0443 -0.83767516,0.0868 -1.2558594,0.12696 0.25950609,1.60191 0.8206852,3.24717 1.9023438,4.556636 0.342343,0.41542 0.5590507,0.954197 0.4804687,1.44336 -0.025283,0.246453 -0.1119591,0.496485 -0.2246094,0.751953 0.1634384,0.135566 0.3491558,0.240365 0.546875,0.314453 0.1631599,-0.298951 0.302037,-0.612493 0.3789063,-0.960938 0.1468187,-0.721817 -0.060504,-1.49206 -0.5,-2.099609 -0.8380808,-1.188455 -1.181556,-2.668875 -1.328125,-4.132815 z')
		self.write_path(style, 'm 2.0175781,-95.949219 c -0.1436635,0.248282 -0.2873481,0.51336 -0.3984375,0.822266 -0.027528,0.140925 -0.048361,0.286201 -0.056641,0.433594 -2.467e-4,0.681216 0.4247003,1.144359 0.9003906,1.335937 -0.4098373,-0.294911 -0.6597598,-0.801902 -0.5390625,-1.265625 0.1089883,-0.402944 0.3428298,-0.741718 0.578125,-1.082031 -0.1691941,-0.0673 -0.3310469,-0.147961 -0.484375,-0.244141 z')
		self.write_path(style, 'm -0.60141829,-103.73449 c 0.41989804,0.0218 0.83993975,0.0419 1.26010131,0.06 -0.0659788,1.5874 0.0745189,3.19567 0.54825348,4.721421 0,0 3e-7,0 3e-7,0 0.2210797,0.697025 0.4978677,1.375404 0.9689598,1.905354 0,0 5e-7,0 5e-7,0 0.3845928,0.434985 0.9522601,0.744799 1.5524436,0.724004 1.1452221,-0.0092 1.9169042,-1.552437 1.4518695,-2.768928 0.3599911,0.495931 0.5141682,1.195943 0.3843301,1.874168 -0.2819051,0.74386 -0.8986219,1.34968 -1.7797763,1.509444 -0.8169383,0.06458 -1.5929088,-0.260511 -2.1406711,-0.80816 -0.6154334,-0.618165 -1.00944317,-1.374126 -1.28897248,-2.114375 1.1e-7,0 -2.1e-7,-10e-7 -2.1e-7,-10e-7 -0.63428047,-1.632007 -0.9178233,-3.376937 -0.9565385,-5.102977 z')
		self.write_path(style, 'm -3.3945312,-104.69922 c -0.3552481,1.42085 -1.0184522,2.85835 -2.2050782,3.54883 -0.032141,0.0187 -0.080618,0.0419 -0.1152344,0.0625 0.031118,0.13229 0.066803,0.26506 0.078125,0.39648 0.014507,0.1684 0.00634,0.33743 -0.00195,0.50586 0.1820691,-0.0904 0.3573596,-0.19054 0.5039063,-0.29687 1.372379,-0.86601 2.2647831,-2.35534 2.7050781,-3.9082 -0.321271,-0.10556 -0.6428638,-0.2091 -0.9648437,-0.3086 z')
		self.write_path(style, 'm -6.8574219,-102.06641 c -0.092115,-0.0108 -0.1890786,-0.0102 -0.2910156,0.01 -0.418133,0.0808 -0.80098,0.41965 -0.8750005,0.85742 -0.06307,0.373 0.0048,0.78465 0.3886724,1.06445 0.3364651,0.245274 0.7423581,0.290742 1.1484375,0.22852 -0.00622,-0.17417 -0.017944,-0.33714 -0.03125,-0.48047 -0.00651,-0.0701 -0.03744,-0.18008 -0.0625,-0.28125 -0.1991158,0.0605 -0.3975277,0.0949 -0.5761719,0.041 -0.152411,-0.046 -0.2709456,-0.30962 -0.1972656,-0.49219 0.026637,-0.066 0.0676,-0.12052 0.1113281,-0.16797 0.014137,-0.015 0.029411,-0.0282 0.044922,-0.041 0.032512,-0.0274 0.068145,-0.0477 0.1054687,-0.0645 0.020292,-0.009 0.039261,-0.0199 0.060547,-0.0254 0.053423,-0.0142 0.1092213,-0.0193 0.1660156,-0.01 0.074812,0.0126 0.1488622,0.0453 0.2207032,0.10546 0.198543,0.16628 0.3222775,0.70139 0.3359374,0.88672 0.040162,0.545023 0.1414044,1.206348 -0.2597656,2.146488 0.546965,-0.610901 0.7818213,-1.516606 0.7070313,-2.384768 -0.031496,-0.36561 -0.1332691,-0.73326 -0.3613281,-1.0332 -0.043291,-0.0569 -0.096805,-0.11122 -0.1582032,-0.16016 -0.063737,-0.0508 -0.1366607,-0.0942 -0.2167968,-0.1289 -0.079938,-0.0346 -0.1666628,-0.0594 -0.2597657,-0.0703 z')

		# Eyes
		self.write_ellipse(style, 0.28214264, -107.8961, 0.50823301, 0.86178637)
		self.write_ellipse(style, -1.629467, -107.9845, 0.50823301, 0.86178637)

		#  Ends of long tentacles
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#ffffff;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.72000003;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, 'm 16.079505,-112.80178 c 0,0 -0.534036,-1.98412 -1.352253,-2.375 -1.083027,-0.51738 -2.029029,0.0701 -1.654029,0.82009 0.375,0.75 2.381282,1.33616 3.006282,1.55491 z')
		self.write_path(style, 'm -15.544194,-112.67678 c 0,0 -0.104921,-1.79881 0.731694,-2.49777 0.96875,-0.80936 1.875,-0.15625 1.59375,0.53125 -0.28125,0.6875 -1.825444,1.62277 -2.325444,1.96652 z')

		self.end_group()

	def draw_fish(self, id='', transform=''):
		self.start_group(id=id, transform=transform)

		# Body Fill
		fill_gradient = 'gradientFish'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:url(#%s);fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate' % fill_gradient
		self.write_path(style, 'm 6.75164,-116.27687 c 2.99065,0.60485 4.49367,1.24794 5.89266,2.66121 2.45016,2.47513 3.25045,6.5505 3.25045,6.5505 l -3.54035,0.49898 2.97008,0.83162 c -1.40188,1.23555 -2.8637,2.14124 -4.39572,2.68497 -2.28163,0.80975 -5.89735,1.19916 -8.27072,0.72096 -2.52003,-0.50774 -4.93787,-1.71891 -6.65678,-2.93199 -1.70292,-1.2018 -2.32599,-2.77049 -4.34245,-2.71421 -2.02435,0.0566 -3.06024,1.36024 -6.2744,2.54392 0.98841,-2.25668 1.48644,-4.44986 1.47742,-4.77248 -0.0131,-0.47021 -0.60937,-2.94625 -1.71029,-5.74037 4.56815,1.9526 4.13574,3.93892 6.7876,4.01568 1.65013,0.0477 2.8784,-2.27892 4.84548,-3.01143 0,0 0.0925,-0.76339 -0.85797,-2.09399 2.125,-1.125 5.3749,-2.84347 9.18238,-2.11673 0.63846,0.67205 1.20575,1.59646 1.64258,2.87336 z')
		# Body Outline
		style = 'color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, 'm 3.75195,-119.76758 c -0.55834,-0.0162 -1.08956,0.007 -1.41992,0.0332 -3.44102,0.26924 -4.79186,1.37793 -7.48633,2.26368 0.80029,0.66264 1.38172,1.65445 1.58985,2.40625 -0.74252,0.46927 -1.56885,1.06749 -2.34375,1.66992 -0.78694,0.61179 -1.52805,1.08797 -2.13868,1.07031 -1.213,-0.0351 -1.55439,-0.52183 -2.3789,-1.23633 -1.98577,-1.72081 -3.07464,-2.29632 -5.23438,-3.2207 0.86297,2.18173 2.04317,4.50407 2.07227,6.58984 0.0263,1.88626 -1.13742,3.87948 -1.86328,5.54883 1.62081,-0.53562 3.22001,-1.34059 4.6289,-2.08398 0.89906,-0.47438 1.57632,-0.77317 2.49415,-0.79883 0.89038,-0.0249 1.40182,0.27656 1.98242,0.77734 0.25085,0.21637 0.51534,0.48279 0.79687,0.75586 -0.25647,0.40556 -0.79615,0.53695 -1.76562,1.10352 1.95514,0.58994 2.59141,1.85091 4.15625,2.49414 0.55665,-0.25793 1.08128,-0.52946 1.29882,-1.08594 1.28379,0.64871 2.70563,1.21308 4.19922,1.53906 0.0372,0.49232 -0.0779,0.96218 -0.52343,1.75 1.8525,-0.13727 3.11482,-0.49129 3.85351,-1.48437 1.90282,-0.0616 3.90491,-0.41501 5.41016,-0.94922 1.59542,-0.56623 3.08878,-1.52586 4.54297,-2.77148 0.22554,-0.1932 0.55832,-0.5479 0.15234,-0.66602 l -1.22851,-0.35742 1.51367,-0.22656 c 0.18187,-0.0272 0.35546,-0.2168 0.27734,-0.50586 -0.0502,-0.18564 -0.78361,-4.16347 -3.37305,-6.7793 -1.42433,-1.43886 -3.05654,-2.12894 -5.92382,-2.72852 -0.4724,-1.08092 -0.97717,-2.12518 -1.70508,-2.90429 -0.44021,-0.13092 -1.02565,-0.18691 -1.58399,-0.20313 z m -0.1289,0.86719 c 0.40991,0.0169 0.81105,0.0568 1.19922,0.10547 0.77961,0.94104 1.28338,2.04784 1.60937,2.96875 2.1946,0.39918 4.6041,1.23544 5.89453,2.52734 2.08816,2.09053 2.83239,5.19206 2.98633,5.86133 l -3.01953,0.42578 c -0.44473,0.0627 -0.45389,0.76792 -0.0586,0.87891 l 1.98242,0.55664 c -1.12071,0.87174 -2.24918,1.67981 -3.4375,2.10156 -0.33815,0.12001 -0.71912,0.22666 -1.11524,0.32617 -2.33138,-1.12461 -3.38072,-3.76269 -3.66601,-5.20312 -0.15295,-0.77226 -0.48459,-1.00055 -0.26758,0.46094 0.277,1.86552 1.35587,3.78888 2.74609,4.99218 -1.94553,0.34633 -4.16617,0.4437 -5.72851,0.12891 -2.43884,-0.49138 -4.81456,-1.67957 -6.48633,-2.85938 -0.79723,-0.56263 -1.35875,-1.23084 -2.01953,-1.80078 -0.66079,-0.56995 -1.57913,-0.96766 -2.54883,-0.93164 -0.96571,0.0359 -2.00556,0.34944 -2.93359,0.83789 -0.68049,0.35816 -1.62451,0.79789 -2.58789,1.22461 0.58514,-1.36212 1.15509,-2.85368 1.14062,-3.91797 -0.0229,-1.68436 -0.84568,-3.32406 -1.36523,-4.77929 1.43808,0.75542 2.36518,1.48293 3.00781,2.08984 0.79559,0.75138 1.70527,1.34121 2.9414,1.36523 0.8676,0.0169 1.85414,-0.60951 2.64454,-1.26171 1.07222,-0.88474 2.37395,-1.75346 3.82031,-2.3125 0.84286,-0.32579 2.17657,-0.81342 1.5664,-0.90821 -0.63083,-0.098 -1.90673,0.29013 -2.74804,0.65625 -0.21144,-0.67843 -0.52851,-1.28134 -0.85547,-1.77148 1.86816,-0.59893 2.90957,-1.50638 6.04687,-1.72852 0.42336,-0.0441 0.84204,-0.0501 1.25196,-0.0332 z')

		# Fin
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, 'm 4.14858,-108.59983 c -0.47489,-0.30307 -1.53655,-0.90869 -2.26472,-0.88862 -0.0804,0.002 -0.2543,0.14712 -0.15844,0.31108 0.47438,0.81135 0.88194,1.78963 0.81744,2.88053 -0.01,0.15682 0.0463,0.31282 0.28149,0.29908 0.85805,-0.0503 1.22499,-0.14313 1.82534,-0.42991 0.33162,-0.1584 0.28985,0.0295 -0.17284,0.32399 -0.42638,0.27143 -1.15747,0.57467 -1.60626,0.62419 -0.57111,0.063 -0.86938,-0.30115 -0.85559,-0.49509 0.0664,-0.93438 -0.40775,-2.23989 -0.84996,-3.00389 -0.64912,-1.12144 0.5114,-1.14367 1.04743,-1.03991 0.57353,0.11103 1.54086,0.51965 2.36735,1.37318 0.31578,0.3261 0.0887,0.37724 -0.43124,0.0454 z')

		# Eye
		style = 'opacity:1;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.89999998;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1'
		self.write_ellipse(style, 35.346939, -105.81317, 0.85538602, 1.0929933, transform='matrix(0.97605309,-0.21753245,0.21753245,0.97605309,0,0)')

		self.end_group()

	def draw_coconut(self, id='', transform=''):
		self.start_group(id=id, transform=transform)

		brown_style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#bc8434;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		white_style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#ffffff;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'

		# Big coconut
		self.write_path(brown_style, 'm -4.5080282,-122.99352 c -6.3850178,2.15964 -8.5771578,9.38405 -8.0814268,14.88876 0.55563,6.16983 5.2811628,10.95294 12.64199276,8.10608 3.04329704,-1.17702 6.04119804,-6.34196 6.22442604,-11.57628 0.09818,-2.80474 -0.29778,-5.51103 -1.639173,-7.82455 -1.102579,-1.90162 -3.478014,-3.784 -6.173654,-4.24214 -1.590991,0.97227 -2.972165,0.64813 -2.972165,0.64813 z')
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.89999998;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_ellipse(style, -120.42445, -1.1047294, 0.54040664, 0.75130093, transform='matrix(0.04286687,0.99908079,-0.99908079,0.04286687,0,0)')
		self.write_ellipse(style, -113.37407, -41.165329, 0.53094649, 0.66291261, transform='matrix(0.35065914,0.93650316,-0.93650316,0.35065914,0,0)')
		self.write_ellipse(style, -115.40491, 28.144659, 0.75130093, 0.578731, transform='matrix(-0.21617976,0.97635358,-0.97635358,-0.21617976,0,0)')

		# Broken coconut
		self.write_path(brown_style, 'm 12.470061,-104.40917 c -1.053625,2.46314 -2.7571896,5.66371 -5.3992166,6.959878 -1.8348159,0.900154 -4.8858287,1.355265 -7.29203855,0.574524 -1.47973495,-0.480128 -3.26695685,-2.153861 -3.88908725,-3.579732 -0.9764548,-2.23794 -1.1678327,-4.60408 -0.6812181,-6.72953 0.2499469,-1.09173 1.186875,-3.22454 1.8151019,-4.00521')
		self.write_path(white_style, 'm -4.1031709,-106.48916 c 0.1858925,1.26956 0.9057567,2.15876 1.8143573,3.06473 0.7258639,0.72377 1.43443306,1.23318 2.38813597,1.53034 0.21168639,0.36954 0.58409309,0.82966 0.71913043,1.00496 0.6211732,0.30789 1.2701423,0.41934 1.7697881,0.53351 1.2859005,0.29381 3.2051814,0.30928 4.487449,0 1.4766975,-0.35618 2.9730411,-1.01232 4.0560481,-2.07749 0.799348,-0.78619 1.474351,-1.85192 1.582847,-2.96784 0.19684,-2.02457 0.0097,-3.62122 -1.250374,-5.21803 -0.765762,-0.24844 -1.101356,-0.47744 -2.0001007,-0.72008 -0.7209049,-0.88161 -1.2999824,-1.55958 -2.1970327,-2.39292 -1.8286746,-0.73618 -4.3613695,-0.80559 -6.0281383,-0.27571 -1.72586214,0.54868 -3.34971,1.59922 -4.0200406,2.49515 -1.4298123,1.911 -1.5302056,3.6019 -1.3220696,5.02338 z')
		fill_gradient = 'gradientCoconut'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:url(#%s);fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.72000003;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate' % fill_gradient
		self.write_path(style, 'm 2.5689019,-111.79765 c -1.95421257,0.27864 -3.6605132,1.67502 -3.9378089,3.55663 -0.3092039,2.09813 0.69763676,3.67395 3.1778133,4.47933 0.373786,0.49838 0.6109957,0.84189 0.7612596,1.05028 0.5701086,0.18629 1.6940872,0.30376 2.4051006,0.28378 1.4220267,-0.04 2.5622123,-0.49712 3.5524385,-1.12498 1.980452,-1.2557 2.103312,-3.22456 0.954264,-5.56685 -0.6629126,-0.17678 -1.1503302,-0.34475 -1.6846877,-0.51996 -0.4611538,-0.48593 -0.8524209,-0.92577 -1.6101047,-1.76382 -1.1960277,-0.5413 -2.2986558,-0.51727 -3.6182747,-0.39441 z')

		self.end_group()

	def draw_flower(self, id='', transform=''):
		self.start_group(id=id, transform=transform)

		path = 'm 0.979805,-123.15615 c -1.34145,-0.0198 -3.490295,1.29985 -4.377698,2.97606 -1.515072,-0.52803 -3.118559,-1.35518 -4.387882,-0.66716 -1.336347,0.80617 -3.05964,1.39841 -3.940732,2.52252 -1.019998,1.30134 -0.730979,3.22834 -1.040234,4.88073 -0.323141,1.72658 0.916341,3.62646 2.178426,4.57303 -0.480389,0.70795 -0.991103,1.55651 -1.064241,1.95596 -0.229528,2.03687 -0.85872,3.65897 -0.172551,5.07299 0.650332,1.34017 2.541535,1.62667 4.009752,2.563613 1.703034,0.722622 3.282592,0.820732 5.14182,0.411702 0.446214,0.818061 0.820032,1.55183 1.868672,1.900477 1.652946,0.549562 2.259608,1.57126 3.487169,1.377119 0.904439,-0.143038 1.706298,-0.852325 2.89228,-1.267016 0.956141,-0.334325 1.792353,-1.310625 2.17414,-2.142916 0.601179,-1.310569 0.607842,-2.718729 0.332147,-4.333519 1.085534,0.10069 1.96385,-0.10288 2.218318,-0.26619 1.401585,-1.12214 2.183535,-1.13125 2.967873,-2.1232 0.706103,-0.89301 0.33785,-2.30208 0.524226,-3.63507 0.190729,-1.36412 -0.373016,-3.11292 -1.13861,-3.85099 -0.916057,-1.14581 -2.133316,-1.66052 -3.360406,-2.25547 0.223107,-1.52457 0.238457,-2.83813 -0.583837,-3.68128 -1.009456,-1.03504 -1.391167,-2.66625 -2.553752,-3.32447 -1.410255,-0.79846 -2.9835,-0.29231 -4.911945,-0.66063 -0.08552,-0.0163 -0.173505,-0.025 -0.262935,-0.0263 z'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#ffffff;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, path)
		fill_gradient = 'gradientFlower'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:url(#%s);fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate' % fill_gradient
		self.write_path(style, path)

		filter = 'blurFlowerMiddle'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#c18bff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.89999998;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;filter:url(#%s);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate' % filter
		self.write_circle(style, 60.884876, -69.652748, 9.6685247, transform='matrix(0.8413905,0,0,0.8413905,-50.722984,-50.755482)')
		filter = 'blurFlowerInner'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#4d0b97;fill-opacity:0.73248411;fill-rule:nonzero;stroke:none;stroke-width:0.89999998;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;filter:url(#%s);color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate' % filter
		self.write_circle(style, 60.884876, -69.652748, 4.5872564, transform='matrix(0.8413905,0,0,0.8413905,-50.722984,-50.755482)')

		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(style, 'm 0.639633,-123.613 c -0.245268,-0.007 -0.493489,0.0184 -0.741147,0.0723 -0.495315,0.10775 -0.988873,0.32636 -1.452713,0.61626 -0.897328,0.56081 -1.698239,1.40222 -2.2333,2.34669 -0.538041,-0.29613 -1.168361,-0.58916 -1.843828,-0.75923 -0.402544,-0.10135 -0.817029,-0.16411 -1.217716,-0.14954 -0.400686,0.0146 -0.786664,0.10703 -1.132262,0.31552 -1.283405,0.77424 -3.212955,1.5351 -4.096848,2.84955 -1.036325,1.54115 -0.856398,3.22859 -1.064886,4.82978 -0.121933,0.93647 0.116053,1.93977 0.548877,2.83148 0.383935,0.79099 0.927795,1.48307 1.55953,1.96215 -0.523828,0.48763 -0.918389,1.06735 -0.994221,1.7403 -0.111704,0.99127 -0.114545,1.61006 -0.218564,2.47815 -0.10402,0.86809 -0.307253,2.00443 0.08052,2.80354 0.383523,0.79035 1.112241,1.24077 1.875051,1.60883 0.762811,0.368068 1.743867,0.669437 2.430502,1.107614 1.218636,0.777675 2.913786,1.040634 4.971105,0.514366 0.380578,0.842488 0.837563,1.454964 1.755089,1.760018 0.77292,0.256976 1.299533,0.623573 1.830681,0.935061 0.531149,0.311488 1.321397,0.65032 2.04596,0.535729 1.061295,-0.167845 1.585995,-0.765822 2.695079,-1.153626 0.61183,-0.213931 1.413184,-0.872559 1.889842,-1.446139 0.476655,-0.57358 0.870431,-1.194818 1.082961,-1.658131 0.556087,-1.212262 0.51771,-2.127442 0.179125,-3.446082 0.715918,0.0871 1.419103,0.0384 1.947359,-0.38454 0.67438,-0.53993 1.161498,-1.0671 1.640053,-1.33933 0.478556,-0.27223 0.932552,-0.56407 1.362327,-1.10761 0.433047,-0.54768 0.51727,-1.24584 0.537371,-1.90299 0.02011,-0.65714 -0.02179,-1.32636 0.06411,-1.94078 0.107665,-0.77002 -0.0067,-1.365 -0.266216,-2.1725 -0.259325,-0.8075 -0.625806,-1.53158 -1.09118,-1.98023 -0.663846,-0.63998 -1.599943,-1.39472 -3.03032,-1.93914 0.11665,-0.50066 0.147215,-1.05012 0.09038,-1.59404 -0.08427,-0.80653 -0.342696,-1.59653 -0.862754,-2.12977 -0.452036,-0.4635 -0.790788,-1.10063 -1.165128,-1.73208 -0.374341,-0.63145 -0.949406,-1.37528 -1.631838,-1.76166 -0.804443,-0.45546 -1.651134,-0.45909 -2.476515,-0.44699 -0.82538,0.0121 -1.487089,0.14634 -2.343404,-0.13804 -0.235484,-0.0782 -0.477801,-0.11783 -0.723065,-0.1249 z m -0.02629,0.75923 c 0.180353,0.004 0.347555,0.0466 0.511079,0.0838 1.006924,0.22923 1.7795,0.18938 2.591548,0.17748 0.812049,-0.0119 1.487806,0.005 2.093616,0.34839 0.480153,0.27185 0.994251,0.88183 1.354113,1.48886 0.359862,0.60703 0.716169,1.30186 1.27359,1.87341 0.334308,0.34279 0.580376,0.99176 0.652406,1.68114 0.07203,0.68938 -0.02687,1.41322 -0.248144,1.87012 -0.450738,0.93069 -1.413978,1.86673 -2.379558,2.48966 -1.071525,0.69128 -2.210789,1.32545 -2.704939,1.55789 -0.727729,0.34231 -0.911947,0.74706 -0.437129,0.57517 0.432747,-0.15667 2.273938,-0.86367 3.500316,-1.65485 0.988448,-0.63768 2.112424,-1.45155 2.685219,-2.60633 1.29991,0.49828 2.125357,1.16513 2.750952,1.76823 0.300222,0.28943 0.662715,0.9411 0.895622,1.66635 0.232906,0.72524 0.31971,1.24151 0.236641,1.83561 -0.100468,0.71856 -0.05054,1.4191 -0.06902,2.02295 -0.01848,0.60386 -0.10327,1.11067 -0.376324,1.456 -0.354559,0.44841 -0.683098,0.65751 -1.142122,0.91863 -0.459024,0.26112 -1.011451,0.82613 -1.738654,1.40834 -0.339654,0.27194 -1.05202,0.3145 -1.842185,0.15612 -0.790168,-0.15837 -1.680674,-0.36802 -2.228371,-0.63433 -0.501305,-0.24375 -1.107321,-0.71188 -1.718935,-1.22593 -0.606651,-0.50988 -0.946266,-0.80483 -1.105968,-1.0008 -0.449169,-0.55116 -0.736865,-0.57408 -0.419052,-0.0362 0.128591,0.21765 0.29565,0.55252 0.874258,1.15363 0.578608,0.60111 1.39831,1.334 2.091973,1.67128 0.52965,0.25753 1.278195,0.55106 2.055819,0.7395 0.418548,1.4671 0.497282,2.0902 -0.0493,3.28175 -0.169259,0.368978 -0.542533,0.967084 -0.976146,1.488867 -0.433612,0.521783 -1.213575,1.09568 -1.557886,1.216072 -1.262881,0.441579 -1.81603,1.002528 -2.563612,1.120758 -0.502998,0.07955 -1.051079,-0.15352 -1.543097,-0.442058 -0.492018,-0.288541 -1.09527,-0.708208 -1.975296,-1.000794 -0.906713,-0.30146 -1.303684,-1.017149 -1.521734,-1.990087 -0.240751,-1.074238 -0.284382,-2.018958 -0.03944,-3.252168 0.09422,-0.47435 0.345844,-1.11328 0.616253,-1.75509 0.254524,-0.60411 0.521586,-1.0267 0.657337,-1.20621 0.534373,-0.70663 0.573544,-1.02158 -0.08052,-0.47 -0.09001,0.0759 -0.437166,0.46228 -0.800308,1.04845 -0.388969,0.62787 -0.745556,1.33952 -0.913697,1.96215 -0.320374,1.18635 -0.455037,2.59874 -0.177481,3.837203 0.0049,0.02169 0.01287,0.04249 0.01807,0.06409 -1.86503,0.462081 -3.499403,0.191906 -4.474817,-0.430556 -0.781583,-0.498767 -1.637015,-0.807967 -2.349978,-1.151977 -0.712961,-0.34402 -1.256569,-0.70734 -1.523376,-1.25716 -0.298393,-0.61491 -0.108087,-1.57682 -0.0115,-2.38285 0.09658,-0.80602 0.102383,-1.43749 0.220207,-2.48308 0.06347,-0.56325 0.566474,-1.18992 1.271946,-1.691 0.705472,-0.50107 1.601251,-0.92224 2.259594,-1.04681 0.666145,-0.12605 1.427995,-0.20972 2.239874,-0.1709 0.817343,0.0391 1.389205,0.17406 1.855332,0.30895 0.501887,0.14523 0.706651,0.0181 0.14297,-0.28759 -0.221782,-0.12027 -0.830365,-0.31483 -1.664704,-0.4815 -0.749787,-0.14977 -1.792536,-0.20692 -2.634275,-0.0477 -0.79482,0.1504 -1.828356,0.53709 -2.627702,1.10268 -0.560501,-0.3756 -1.107978,-1.03998 -1.479008,-1.80438 -0.38132,-0.78561 -0.575888,-1.66668 -0.479855,-2.40421 0.225627,-1.73283 0.09276,-3.26127 0.910411,-4.45839 0.799409,-1.17041 2.502142,-1.83231 3.891431,-2.67042 0.418566,-0.25251 1.071917,-0.25586 1.774808,-0.0789 0.70289,0.17697 1.431889,0.52017 1.958862,0.8381 1.177378,0.71033 2.360406,1.81514 2.923503,3.13714 0.225658,0.52978 0.487956,1.31163 0.65898,2.04267 0.180567,0.77183 0.278756,1.12761 0.323738,1.41985 0.0769,0.49959 0.331408,0.76305 0.310592,0.258 -0.0056,-0.13448 -0.02619,-0.62272 -0.11832,-1.39848 -0.09213,-0.77577 -0.372004,-1.76712 -0.649121,-2.54061 -0.498667,-1.39187 -1.517796,-2.50983 -2.729588,-3.34584 0.467794,-0.83001 1.199084,-1.60007 1.983511,-2.09033 0.605002,-0.37812 1.225532,-0.58251 1.766584,-0.57188 z')
		self.write_path(style, 'm 3.794424,-118.09467 c -0.03481,-0.0139 -0.387473,0.76522 -0.773437,1.66992 -0.381703,0.89472 -0.809184,1.94165 -0.982422,2.44336 -0.176438,0.5371 -0.390469,1.30435 -0.589844,2.01172 0.06031,-0.55635 0.109986,-1.12538 0.103516,-1.63477 -0.01279,-1.74744 -0.425929,-3.66291 -0.498047,-3.65039 -0.07275,0.0126 0.183985,1.9486 0.04883,3.63477 -0.07238,0.83501 -0.290636,1.86782 -0.482422,2.63281 -0.354416,-0.68951 -0.858631,-1.64701 -1.449218,-2.51562 -0.780652,-1.11593 -2.309126,-2.07981 -2.347657,-2.02539 -0.04001,0.0565 1.375504,1.16904 1.964844,2.26171 0.304172,0.53913 0.568646,1.10365 0.796875,1.62696 0.372061,0.28889 0.708358,0.56132 0.951172,0.78515 0.450547,0.41534 0.755162,0.86352 0.892578,1.28907 0.0687,0.21277 0.09588,0.4226 0.05859,0.62695 -0.03729,0.20435 -0.155086,0.4041 -0.339844,0.52344 -0.305542,0.19735 -0.71844,0.21836 -1.103516,0.0371 -0.310556,-0.14618 -0.627467,-0.43694 -0.960937,-0.82031 -0.641237,0.0208 -1.474062,0.0584 -2.1875,0.17187 -2.104283,0.29168 -3.519408,1.38936 -3.480469,1.44531 0.03898,0.056 1.530217,-0.86817 3.527344,-0.99804 0.376674,-0.0166 0.788074,-0.008 1.193359,0.01 -0.712154,0.25439 -1.4348,0.51707 -1.767578,0.68164 -2.162568,0.91869 -4.094659,3.07329 -4.046875,3.11914 0.04862,0.0466 2.113703,-1.96681 4.210938,-2.69922 0.365679,-0.10109 1.271937,-0.3498 2.08789,-0.56055 0.07395,-0.0191 0.123337,-0.0305 0.195313,-0.0488 -0.378323,0.25584 -0.792906,0.55853 -1.210938,0.95703 -1.238441,1.16919 -1.630753,2.5038 -1.566406,2.52735 0.06436,0.0236 0.614646,-1.21112 1.859375,-2.1875 0.923232,-0.7175 1.866097,-1.08815 2.203125,-1.16602 0.06017,0.43796 0.121551,1.11761 0.138672,1.69531 -0.0046,1.38515 -0.382684,3.57189 -0.314453,3.58594 0.06715,0.0138 0.587741,-2.14147 0.734375,-3.5625 0.01539,-0.11398 0.0209,-0.24938 0.0332,-0.375 0.06524,0.42004 0.130264,0.87141 0.193359,1.16406 0.346841,2.21188 0.996326,4.22625 1.080079,4.20313 0.08403,-0.0232 -0.38924,-2.07493 -0.556641,-4.26367 -0.0036,-0.21423 -0.0095,-0.56189 -0.01563,-0.86524 0.02034,0.0576 0.04072,0.12785 0.06055,0.18164 0.513637,1.61427 1.790647,3.18206 1.855469,3.13477 0.06636,-0.0484 -1.03386,-1.73019 -1.345704,-3.26758 -0.08436,-0.53103 -0.190887,-1.23418 -0.248046,-1.73242 0.450157,0.021 1.107513,0.0847 1.695312,0.19336 1.164725,0.23043 2.402663,0.98994 2.443359,0.93164 0.03983,-0.0571 -1.105126,-0.96654 -2.326171,-1.36719 -0.325602,-0.11217 -0.655915,-0.18972 -0.984376,-0.27539 0.516501,-0.0598 1.137006,-0.1208 1.621094,-0.15625 2.216152,-0.0729 5.151435,0.70788 5.171875,0.63867 0.02015,-0.0682 -2.871752,-1.01257 -5.171875,-1.08984 -0.536234,-0.0394 -1.221307,-0.0518 -1.767578,-0.0645 0.410869,-0.0906 0.883277,-0.18959 1.404297,-0.30469 1.68587,-0.34236 3.617698,-1.23793 3.589844,-1.30469 -0.02823,-0.0677 -2.017753,0.6758 -3.660157,0.85938 -0.68941,0.0665 -1.333269,0.1164 -1.789062,0.13672 0.05402,-0.18849 0.172573,-0.51714 0.359375,-0.97461 0.257407,-0.63039 0.571071,-1.34083 0.787109,-1.74024 0.257372,-0.46166 0.719406,-1.0516 1.111328,-1.53515 0.390428,-0.48171 0.706164,-0.85041 0.679688,-0.87696 -0.02646,-0.0265 -0.396678,0.28997 -0.845703,0.72461 -0.444283,0.43005 -0.980416,0.99029 -1.320313,1.44141 -0.200435,0.26077 -0.436266,0.65875 -0.669922,1.07031 0.144547,-0.74342 0.306939,-1.55708 0.427735,-2.12304 0.09342,-0.49024 0.445698,-1.55421 0.759765,-2.48047 0.315275,-0.92983 0.597322,-1.73608 0.5625,-1.75 z')
		self.write_path(style, 'm -0.916513,-109.19819 c -0.08002,-0.092 -0.155364,-0.1568 -0.238281,-0.26367 -0.1926,-0.24822 -0.664725,-0.74012 -1.285156,-1.32226 -0.09208,-0.0408 -0.153678,-0.0727 -0.248047,-0.11328 -1.388077,-0.6083 -3.187994,-0.65792 -3.19336,-0.58985 -0.0055,0.0696 1.769599,0.29863 2.992188,0.99219 0.943426,0.53918 1.739463,1.0834 1.972656,1.29687 z')
		self.write_path(style, 'm -7.806877,-115.72644 c 1.94457,0.58391 6.643912,3.73434 8.129359,5.1037 0.836444,0.77108 1.096168,1.65836 0.65443,1.94368 -0.441738,0.28531 -1.060198,0.0838 -1.882086,-0.97545 -0.735118,-0.94742 -4.303093,-4.33376 -7.586861,-5.69825 -0.596704,-0.24795 -0.206304,-0.64136 0.685158,-0.37368 z')

		self.write_circle(style, -16.488615, -113.60835, 0.57845598, transform='matrix(0.99754986,0.06995909,-0.06995909,0.99754986,0,0)')
		self.write_circle(style, -15.173941, -112.97731, 0.57845598, transform='matrix(0.99754986,0.06995909,-0.06995909,0.99754986,0,0)')
		self.write_circle(style, -14.332552, -115.29114, 0.57845598, transform='matrix(0.99754986,0.06995909,-0.06995909,0.99754986,0,0)')
		self.write_circle(style, -15.857573, -115.73812, 0.57845598, transform='matrix(0.99754986,0.06995909,-0.06995909,0.99754986,0,0)')
		self.write_circle(style, -17.356298, -115.73812, 0.57845598, transform='matrix(0.99754986,0.06995909,-0.06995909,0.99754986,0,0)')
		self.write_circle(style, -17.803286, -114.39716, 0.57845598, transform='matrix(0.99754986,0.06995909,-0.06995909,0.99754986,0,0)')

		self.end_group()

	def draw_banana(self, id='', transform=''):
		self.start_group(id=id, transform=transform)

		# Thick outline bananas drawn in back.
		thick_style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#f6ff7d;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.89999998;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(thick_style, 'm 8.78082,-121.13744 c 0.34471,1.36915 0.66512,3.60435 0.73321,4.6643 -0.49421,3.88746 -1.33998,7.74843 -3.32367,10.57326 -2.40596,3.42618 -5.41293,5.37866 -11.11869,7.679247 -0.60011,0.241966 -1.22538,0.289326 -1.46855,0.679535 -0.16319,0.261865 0.37387,1.454696 0.69075,1.620824 0.62648,0.328443 1.07253,0.177853 1.77872,0.218405 2.75809,0.158378 5.05424,-0.146839 8.30722,-1.151769 2.54386,-0.78586 5.74014,-3.251012 7.23795,-5.452222 1.82616,-2.68377 2.69924,-6.37346 2.5117,-9.61419 -0.15399,-2.66107 -2.58676,-5.30143 -2.58676,-5.30143 -0.24357,-1.33177 -0.66717,-2.90679 -1.14995,-4.64892 -0.58055,0.0153 -1.40915,0.37101 -1.61193,0.73296 z')
		self.write_path(thick_style, 'm 7.87879,-120.99354 c 0.0285,1.61295 0.38658,3.34631 0.31301,4.75879 -1.00555,3.30202 -3.33857,6.81255 -5.886,9.14173 -3.35597,3.06847 -7.87513,4.2358 -12.26178,5.43386 -0.6242,0.17048 -1.27338,-0.11771 -1.42138,0.51219 -0.15176,0.64587 0.0489,1.217046 0.31467,1.704455 0.33862,0.621027 0.89583,0.442404 1.59118,0.572223 2.67893,0.500153 5.58439,0.941055 8.23815,0.321149 2.59268,-0.605634 5.07646,-1.926877 7.10245,-3.654337 2.47014,-2.10616 4.44803,-4.97661 5.01611,-8.17267 0.39839,-2.24136 -0.605,-3.85067 -0.89708,-6.10835 -0.2048,-1.58315 0.19285,-2.72685 -0.1333,-4.91236 -0.55377,0.056 -1.33048,0.14727 -1.97603,0.40332 z')
		self.write_path(thick_style, 'm 6.86373,-121.02142 c -0.0162,1.67579 0.0613,3.31817 -0.2121,4.71569 -1.71528,2.99538 -4.19007,5.95351 -7.46659,7.74634 -4.28888,2.34678 -7.01389,2.86781 -11.88451,2.04623 -0.63804,-0.10762 -0.91664,-0.4723 -1.38982,-0.031 -0.50866,0.47443 -0.41626,1.00712 -0.0714,1.61117 0.35071,0.61429 0.52944,0.41897 1.09534,0.84336 1.98511,1.48869 3.74434,2.06677 6.44298,2.04779 2.77975,-0.0196 6.56154,-0.29036 8.90025,-1.56286 2.85139,-1.55146 4.93737,-3.4518 6.15239,-6.46199 0.85208,-2.11101 -0.0744,-4.05058 0.10539,-6.31996 0.12609,-1.59136 0.14328,-2.6534 0.0968,-4.5494 -0.63016,-0.20606 -1.24784,-0.12786 -1.76873,-0.0854 z')
		
		# Lines and redraw front bananas
		line_style = 'color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#737828;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.72000003;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		style = 'color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#f7ff7d;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.72000003;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate'
		self.write_path(line_style, 'm 2.51814,-107.7686 c -2.07228,1.54391 -3.74795,2.09142 -6.33636,2.57335 -1.72347,0.32089 -3.84937,0.49004 -6.70834,0.0497 -0.53792,-0.0828 -0.32892,0.17921 0.20456,0.28719 2.7148,0.54957 5.27205,0.1766 6.8941,-0.0851 2.63047,-0.42445 3.77137,-0.81223 6.04492,-2.32391 0.12768,-0.58475 -0.15949,-0.11588 -0.0988,-0.5012 z')
		self.write_path(style, 'm 7.87879,-120.99354 c 0.0285,1.61295 0.38658,3.34631 0.31301,4.75879 -1.00555,3.30202 -3.33857,6.81255 -5.886,9.14173 -3.35597,3.06847 -7.87513,4.2358 -12.26178,5.43386 -0.6242,0.17048 -1.27338,-0.11771 -1.42138,0.51219 -0.15176,0.64587 0.0489,1.217046 0.31467,1.704455 0.33862,0.621027 0.89583,0.442404 1.59118,0.572223 2.67893,0.500153 5.58439,0.941055 8.23815,0.321149 2.59268,-0.605634 5.07646,-1.926877 7.10245,-3.654337 2.47014,-2.10616 4.44803,-4.97661 5.01611,-8.17267 0.39839,-2.24136 -0.605,-3.85067 -0.89708,-6.10835 -0.2048,-1.58315 0.19285,-2.72685 -0.1333,-4.91236 -0.55377,0.056 -1.33048,0.14727 -1.97603,0.40332 z')
		self.write_path(line_style, 'm 4.80468,-106.35032 c -1.8366,1.79924 -3.59964,2.90171 -6.00807,3.97021 -1.77027,0.7854 -3.77092,1.22784 -6.52266,1.38661 -0.55888,0.0322 -0.28397,0.22297 0.27546,0.20184 2.71946,-0.10273 4.80476,-0.55229 6.63126,-1.36264 2.43383,-1.07977 4.50278,-2.38649 6.25386,-4.13127 0.79789,-0.79502 1.95252,-2.23179 2.69967,-3.4881 0.21909,-0.3684 0.3354,-1.28542 0.2234,-1.22755 -1.02526,2.0653 -2.6769,3.7927 -3.55292,4.6509 z')
		self.write_path(style, 'm 8.78082,-121.13744 c 0.34471,1.36915 0.66512,3.60435 0.73321,4.6643 -0.49421,3.88746 -1.33998,7.74843 -3.32367,10.57326 -2.40596,3.42618 -5.41293,5.37866 -11.11869,7.679247 -0.60011,0.241966 -1.22538,0.289326 -1.46855,0.679535 -0.16319,0.261865 0.37387,1.454696 0.69075,1.620824 0.62648,0.328443 1.07253,0.177853 1.77872,0.218405 2.75809,0.158378 5.05424,-0.146839 8.30722,-1.151769 2.54386,-0.78586 5.74014,-3.251012 7.23795,-5.452222 1.82616,-2.68377 2.69924,-6.37346 2.5117,-9.61419 -0.15399,-2.66107 -2.58676,-5.30143 -2.58676,-5.30143 -0.24357,-1.33177 -0.66717,-2.90679 -1.14995,-4.64892 -0.58055,0.0153 -1.40915,0.37101 -1.61193,0.73296 z')
		self.write_path(line_style, 'm 11.17023,-113.86439 c -0.011,1.77939 -0.15804,3.37671 -0.70318,5.01283 -0.47684,1.43111 -0.94867,2.44937 -1.96984,4.0718 -1.36954,2.17594 -2.93041,3.68885 -5.19121,5.042 -1.55728,0.93208 -2.86824,1.715367 -5.59247,2.278309 -0.52698,0.108898 -1.00078,0.418847 -0.4677,0.345229 2.76772,-0.382229 4.71945,-1.233835 6.39997,-2.314868 2.23928,-1.44048 3.93705,-2.7933 5.38929,-5.10065 1.02607,-1.63022 1.47452,-2.54995 1.94328,-4.06882 0.56259,-1.82288 0.63573,-3.73693 0.46838,-5.5182 -0.0877,-0.93395 -0.2737,-0.2032 -0.27652,0.25237 z')

		self.end_group()

	def draw_pirate(self, id='', transform=''):
		self.start_group(id=id, transform=transform)

		path = "m -107.60416,-273.69223 -7.8991,-1.94695 -6.08951,-5.39484 -2.88489,-7.60683 0.98062,-8.07619 4.6215,-6.69539 7.20363,-3.78076 8.13551,0 7.203628,3.78076 4.621495,6.69539 0.980627,8.07619 -2.88489,7.60683 -6.089513,5.39484 z"
		style = "display:inline;opacity:1;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.72000003;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		self.write_path(style, path, transform="scale(-1,-1)")

		style_white_fill = "color:#000000;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.49999997;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate"
		style_black_fill = "color:#000000;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;direction:ltr;block-progression:tb;writing-mode:lr-tb;baseline-shift:baseline;text-anchor:start;white-space:normal;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.49999997;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate"

		# Skull and crossbones
		self.start_group(transform="translate(6.943425,5.6840535)")

		# Bone 1
		self.start_group(transform="translate(0,-10)")
		self.write_path(style_white_fill, "m 91.84844,289.85155 c 4.41124,3.03993 11.33218,5.63427 19.39618,8.47116 0.51356,0.18067 1.26729,0.0129 1.26729,0.0129 1.03108,0.0262 1.76032,0.59243 1.42127,1.81302 -0.15625,0.5625 -0.60065,0.1875 -1.10065,0.75 -0.59594,0.67043 -0.31337,0.98447 -0.78702,1.45924 -0.37301,0.37389 -0.95237,0.38325 -1.41542,-0.0762 -0.43122,-0.4279 -0.24851,-1.07751 -0.79513,-1.34257 -5.2397,-2.54083 -12.94978,-6.27419 -18.97954,-8.64117 -0.75546,-0.29655 -1.95134,0.5095 -2.69668,0.18835 -0.65522,-0.28232 -1.04679,-1.02773 -0.89579,-1.72503 0.11053,-0.51043 1.25,-0.94464 1.25,-0.94464 l 0.16316,0.45958 c -0.38049,-1.27579 -0.54342,-1.55226 0.0416,-2.29926 0.47038,-0.60064 1.71455,-0.2507 2.18742,0.26834 0.3856,0.42325 0.37162,1.21233 0.94334,1.60632 z")
		self.write_path(style_black_fill, "m 89.94141,287.44531 c -0.54653,-0.13973 -1.02793,0.0475 -1.41993,0.37696 -0.39461,0.33166 -0.45344,0.73455 -0.43554,1.11718 0.009,0.1953 0.0749,0.48278 0.14843,0.71094 0.0247,0.0765 -0.13751,0.0543 -0.37499,0.19141 -0.31892,0.18405 -0.69539,0.49169 -0.78516,0.90624 -0.17772,0.8207 0.18277,1.73389 0.98633,1.96876 0.90806,0.26541 1.87242,-0.46589 2.70312,-0.18553 6.12153,2.06605 13.77428,5.90495 18.93945,8.59375 0.44579,0.23206 0.47891,0.99792 0.75,1.33398 0.47609,0.59019 1.43418,0.58737 1.82423,0.0606 0.41555,-0.56124 0.35263,-0.97015 0.71093,-1.40039 0.19962,-0.2397 0.27907,-0.36717 0.48047,-0.41602 0.10069,-0.0244 0.3919,-0.085 0.64844,-0.32813 0.37646,-0.35676 0.31231,-1.20126 -0.13264,-1.71679 -0.40032,-0.46384 -1.02404,-0.57439 -1.4961,-0.57426 -0.43431,1.2e-4 -0.8621,0.10335 -1.16011,0.002 -8.09046,-2.75143 -14.91003,-5.38426 -19.27539,-8.39258 -0.22086,-0.1522 -0.39434,-0.43852 -0.51171,-0.72461 -0.2365,-0.57649 -0.55594,-1.25663 -1.59983,-1.52351 z m 1.2188,1.80664 c 0.16982,0.38884 0.34852,0.54692 0.5469,0.80468 4.45711,3.07156 11.38831,5.66408 19.45508,8.50195 0.6315,0.22216 1.0547,0.10621 1.35742,0.0683 0.71089,-0.0889 1.08312,0.23005 1.22662,0.42788 0.35341,0.48722 0.19231,1.06561 -0.21479,1.15626 -0.18569,0.0413 -0.61103,0.17616 -0.88477,0.52148 -0.33647,0.42445 -0.37657,1.24201 -0.78515,1.55078 -0.31976,0.24165 -0.75772,0.27891 -1.05469,-0.17966 -0.32208,-0.49734 -0.27651,-1.10107 -0.88672,-1.42774 -5.13397,-2.7485 -12.86209,-6.41107 -18.97265,-8.61133 -0.88412,-0.31835 -1.92323,0.3249 -2.69727,0.23828 -0.58607,-0.0656 -0.8665,-0.91439 -0.74219,-1.48829 0.0208,-0.0959 0.18739,-0.36795 0.46875,-0.52344 0.30948,-0.17102 0.40248,-0.17047 0.44922,-0.0664 0.0857,0.19085 0.13229,0.44867 0.15637,0.72069 0.0197,0.22228 0.17958,-0.0361 0.20117,-0.10743 0.0917,-0.30287 -1.1e-4,-0.84555 -0.0587,-0.98826 -0.35066,-0.85435 -0.24288,-1.31016 0.12868,-1.7077 0.29779,-0.31861 0.72973,-0.39498 1.09186,-0.27481 0.69853,0.2318 0.95425,0.78805 1.21486,1.38476 z")
		self.end_group()

		# Bone 2
		self.start_group(transform="translate(0,-10)")
		self.write_path(style_white_fill, "m 109.41706,289.80736 c -4.41124,3.03993 -11.33218,5.63427 -19.39618,8.47116 -0.51356,0.18067 -1.26729,0.0129 -1.26729,0.0129 -1.03108,0.0262 -1.76032,0.59243 -1.42127,1.81302 0.15625,0.5625 0.60065,0.1875 1.10065,0.75 0.59594,0.67043 0.31337,0.98447 0.78702,1.45924 0.37301,0.37389 0.95237,0.38325 1.41542,-0.0762 0.43122,-0.4279 0.24851,-1.07751 0.79513,-1.34257 5.2397,-2.54083 12.94978,-6.27419 18.97954,-8.64117 0.75546,-0.29655 1.95134,0.5095 2.69668,0.18835 0.65522,-0.28232 1.04679,-1.02773 0.89579,-1.72503 -0.11053,-0.51043 -1.25,-0.94464 -1.25,-0.94464 l -0.16316,0.45958 c 0.38049,-1.27579 0.54342,-1.55226 -0.0416,-2.29926 -0.47038,-0.60064 -1.71455,-0.2507 -2.18742,0.26834 -0.3856,0.42325 -0.37162,1.21233 -0.94334,1.60632 z")
		self.write_path(style_black_fill, "m 111.38756,287.33529 c -0.48664,0.0425 -1.11759,0.35128 -1.31171,0.78554 -0.25532,0.57121 -0.35791,1.10841 -0.80095,1.43578 -4.2638,3.15061 -11.02151,5.86741 -19.11914,8.59765 -0.37569,0.12667 -0.793,0.007 -1.18941,0 -0.55986,-0.009 -1.2909,0.0173 -1.62304,0.38477 -0.33215,0.36747 -0.49179,0.82955 -0.3072,1.49398 0.0492,0.17698 0.19508,0.41555 0.31501,0.50406 0.11993,0.0885 0.24305,0.11618 0.34375,0.14063 0.20139,0.0489 0.34354,0.0657 0.55078,0.29883 0.27206,0.30606 0.32523,0.48899 0.38672,0.70508 0.0615,0.21608 0.13631,0.48917 0.41016,0.76367 0.46295,0.46404 1.23127,0.45987 1.76953,-0.0742 0.27305,-0.27093 0.34319,-0.599 0.41601,-0.83594 0.0728,-0.23693 0.11923,-0.36621 0.31055,-0.45898 5.23957,-2.54077 12.92679,-6.14139 18.94079,-8.50219 0.26425,-0.10373 0.73389,-0.14378 1.22132,-0.0193 0.48743,0.1245 1.01877,0.28217 1.50586,0.0723 0.76885,-0.33126 1.21875,-1.18712 1.04101,-2.00781 -0.0898,-0.41456 -0.51237,-0.7471 -0.8313,-0.93114 -0.23626,-0.13633 -0.30692,-0.13408 -0.29326,-0.2428 0.0341,-0.27151 0.0324,-0.44202 0.0416,-0.63783 0.018,-0.38263 -0.0918,-0.65157 -0.42093,-1.02881 -0.39713,-0.45513 -0.89964,-0.48317 -1.35615,-0.44329 z m 0.96351,0.70764 c 0.31461,0.3192 0.35498,0.60714 0.37427,0.86802 0.0265,0.35796 0.0566,0.77981 -0.21212,1.56266 -0.0629,0.1834 -0.13514,0.41283 0.0458,0.26781 0.21765,-0.17449 0.32969,-0.52131 0.40328,-0.67267 0.0499,-0.10264 0.1234,-0.0467 0.3034,0.0364 0.32381,0.14909 0.5206,0.38204 0.54136,0.65469 0.0446,0.5855 -0.25812,1.17489 -0.79972,1.40825 -0.25824,0.11127 -0.69789,0.0264 -1.18359,-0.0976 -0.48573,-0.12404 -1.03674,-0.15395 -1.52796,0.0389 -6.04551,2.3732 -13.73417,5.97497 -18.974,8.51586 -0.35529,0.17229 -0.49003,0.5006 -0.57031,0.76171 -0.0803,0.26112 -0.13479,0.47195 -0.29297,0.62891 -0.38783,0.38482 -0.77943,0.36186 -1.0625,0.0781 -0.1998,-0.20028 -0.21858,-0.32159 -0.2832,-0.54883 -0.0646,-0.22722 -0.16831,-0.53603 -0.49219,-0.90039 -0.29276,-0.32936 -0.5411,-0.43101 -0.7644,-0.44761 -0.16657,-0.0124 -0.31978,-0.24306 -0.3377,-0.29665 -0.18307,-0.54743 -0.0422,-0.79871 0.17376,-1.01614 0.27893,-0.28078 0.87349,-0.22843 1.22527,-0.2358 0.44842,-0.009 0.77278,0.20066 1.40429,-0.0215 8.06676,-2.83789 14.84782,-5.48941 19.23633,-8.6582 0.53983,-0.38979 0.52785,-0.93704 0.79316,-1.50218 0.22245,-0.47382 0.76204,-0.67588 1.09941,-0.72147 0.2658,-0.0359 0.66161,0.0555 0.90033,0.29773 z")
		self.end_group()
		
		# Skull
		self.start_group()

		# White background
		self.write_path(style_white_fill, "m 95.61696,289.40928 c -0.28542,-0.70119 -0.64431,-0.0511 -1.28032,-1.5943 -0.1555,-0.3773 0.0533,-1.26257 -0.20606,-1.97221 -1.08563,-2.97045 -0.70376,-4.38729 -0.13829,-5.43857 0.90077,-1.67462 2.37389,-2.68893 4.18898,-3.25565 1.68855,-0.52721 3.7114,-0.48187 5.36931,0.13497 1.87949,0.69928 2.96812,1.82798 3.83709,3.63528 0.56796,1.18125 0.75027,1.95911 0.46372,3.37367 -0.0839,0.41394 -0.6938,1.7573 -0.89959,2.67781 -0.13567,0.60688 0.13543,0.88631 0.028,1.10465 -0.68013,1.38226 -0.85951,0.68912 -1.42722,1.53162 -0.82001,1.21692 -0.9135,2.26072 -0.9135,2.26072 -2.62487,0.21736 -5.43031,0.27039 -8.01047,-0.13519 -0.21074,-2.67946 -0.3887,-0.7924 -1.01165,-2.3228 z")
		# Left eye
		self.write_path(style_black_fill, "m 101.77982,284.55725 c 0.004,0.96632 0.45036,2.0941 1.39212,2.05041 0.94176,-0.0437 1.37747,-1.03396 1.36409,-2.0552 -0.0134,-1.02124 -0.49476,-1.92637 -1.40364,-1.94387 -0.90889,-0.0175 -1.3563,0.98234 -1.35257,1.94866 z")
		# Nose
		self.write_path(style_black_fill, "m 100.03721,289.11908 c -0.42377,-0.36462 -0.23973,-1.10247 0.38785,-2.14089 0.0843,-0.13938 0.41827,-0.11168 0.51275,0.021 0.6035,0.84762 0.67744,2.01011 0.33563,2.12543 -0.234,0.079 -0.36489,-0.0838 -0.58623,-0.37016 -0.23681,0.29673 -0.365,0.60983 -0.65,0.36461 z")
		# Right eye
		self.write_path(style_black_fill, "m 96.79629,284.49096 c 0.004,0.96632 0.38407,2.09409 1.34792,2.0725 0.96385,-0.0216 1.44376,-1.01186 1.43038,-2.0331 -0.0134,-1.02124 -0.45057,-1.90429 -1.33735,-1.94387 -0.88677,-0.0396 -1.44468,0.93815 -1.44095,1.90447 z")
		# Outline
		self.write_path(style_black_fill, "m 100.65625,276.60942 c -0.85308,-0.0126 -2.0994,0.19349 -2.75586,0.39844 -1.86941,0.58365 -2.83514,1.247 -3.88476,2.72657 -0.44,0.76902 -1.06058,1.73123 -0.99181,3.39023 0.058,1.39821 1.39651,3.32249 1.12006,4.24558 -0.10938,0.36524 -0.0785,0.6196 0.30526,1.01848 1.20238,1.37095 1.90562,2.41351 1.91019,3.23239 -0.008,0.23436 0.045,0.42743 0.24414,0.44141 2.80929,0.37265 5.12783,0.29481 7.9453,0.08 0.21185,-0.008 0.29297,-0.1875 0.29297,-0.39063 0.19662,-1.54374 0.9314,-2.00835 1.9863,-3.07614 0.28784,-0.27357 0.62427,-0.65332 0.29883,-1.33789 -0.23102,-0.48596 0.92245,-2.47356 1.06055,-3.55859 0.14911,-1.17151 -0.15793,-2.26393 -0.5293,-3.10157 -0.88762,-1.84613 -1.94831,-2.7592 -3.86523,-3.52929 -0.93109,-0.37405 -2.26053,-0.52603 -3.13664,-0.53899 z m -0.043,0.46285 c 1.09915,0.0507 2.08553,0.14066 3.01172,0.51567 1.72448,0.69823 2.70048,1.44439 3.55078,3.21288 0.36939,0.76826 0.69557,1.73619 0.54493,2.99415 -0.2428,1.03053 -1.05425,2.50934 -1.02149,3.02539 0,0 -0.0861,-0.15602 -0.21289,-0.41601 -0.18281,-0.37493 -0.21233,-0.57486 -0.27149,-1.11328 -0.0268,-0.24371 -0.29862,-0.32626 -0.29296,-0.22657 0.0416,0.73466 0.10464,1.0742 0.24804,1.5918 0.10978,0.39625 0.43528,0.73247 0.46485,1.14258 0.009,0.12977 -0.0461,0.34222 -0.13868,0.43359 -1.26028,1.19619 -2.08802,2.47382 -2.17578,3.43356 -2.51398,0.3381 -4.97436,0.2315 -7.47461,-0.0937 -0.14518,-1.85044 -1.10626,-2.38298 -2.14453,-3.76949 -0.18886,-0.25326 0.28842,-0.85838 0.40236,-1.26172 0.1228,-0.43469 0.32716,-0.88898 0.22258,-1.5508 -0.0245,-0.15513 -0.22882,0.13848 -0.28125,0.41603 -0.11651,0.61664 -0.28224,0.85172 -0.51435,1.37048 -0.0721,-1.12896 -0.74529,-2.04641 -0.91036,-3.0504 -0.28321,-1.72251 0.14892,-2.51897 0.80286,-3.6236 0.72882,-1.23113 1.99799,-2.15947 3.63348,-2.63984 0.72356,-0.21252 1.87504,-0.42215 2.55679,-0.39072 z")
		# Teeth Separators
		self.write_path(style_black_fill, "m 97.6294,290.74837 c 0.0146,1.13412 -0.0956,1.27773 -0.0956,1.27773 l 0.61964,-0.048 c 0,0 -0.0652,-0.2374 -0.0975,-1.11199 -0.005,-0.1474 -0.42845,-0.26523 -0.42655,-0.11774 z")
		self.write_path(style_black_fill, "m 99.05443,290.95071 c 0.0466,0.86236 -0.0404,1.24458 -0.0404,1.24458 l 0.53125,-0.0811 c 0,0 -0.054,-0.23486 -0.0422,-1.1341 0.002,-0.1427 -0.40962,-0.22457 -0.4376,-0.0846 z")
		self.write_path(style_black_fill, "m 100.4009,290.99111 c 0.0202,0.9611 -0.0846,1.25563 -0.0846,1.25563 l 0.60859,-0.11428 c 0,0 -0.11429,-0.11132 -0.0532,-1.12305 0.0103,-0.17158 -0.47427,-0.19016 -0.47066,-0.0183 z")
		self.write_path(style_black_fill, "m 101.7947,291.02458 c 0.0146,1.13412 -0.0957,1.1562 -0.0957,1.1562 l 0.61964,-0.048 c 0,0 -0.0653,-0.24845 -0.0974,-1.12304 -0.005,-0.1474 -0.42845,-0.13265 -0.42655,0.0148 z")
		self.write_path(style_black_fill, "m 103.054,291.017 c 0.0466,0.86236 -0.0625,1.112 -0.0625,1.112 l 0.53125,-0.0811 c 0,0 -0.054,-0.16857 -0.0422,-1.06781 0.002,-0.1427 -0.43425,-0.1056 -0.42655,0.0369 z")

		self.end_group()  # end skull

		self.end_group()  # end skull and crossbones
		
		self.end_group()

	def draw_port_circle(self, id='', transform=''):
		self.start_group(id=id, transform=transform)
		
		self.start_group(transform="translate(168.55655,-76.089882)")

		style_black_fill = "opacity:1;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.5;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"

		self.write_path(style_black_fill, "m 117.61371,135.33305 -14.27687,-7.03247 -5.122553,15.06798 -5.122556,-15.06798 -14.276867,7.03247 7.032478,-14.27686 -15.067982,-5.12256 15.067981,-5.12255 -7.032477,-14.276871 14.276866,7.032481 5.122557,-15.067985 5.122553,15.067985 14.27687,-7.032481 -7.03248,14.276861 15.06798,5.12256 -15.06798,5.12256 z")

		rotate = "matrix(0.92387953,-0.38268343,0.38268343,0.92387953,-92.322534,69.370912)"
		path = "m 174.56986,132.36623 -10.89361,-3.15815 -5.51643,9.91029 -5.46979,-9.9361 -10.90834,3.10693 3.15816,-10.89362 -9.91029,-5.51642 9.9361,-5.4698 -3.10693,-10.908329 10.89361,3.158149 5.51643,-9.910281 5.46979,9.936101 10.90834,-3.106932 -3.15816,10.893612 9.91029,5.51643 -9.9361,5.46979 z"
		self.write_path(style_black_fill, path, transform=rotate)
		
		self.end_group()

		circle_style = "opacity:1;fill:#ffffff;fill-opacity:1;stroke:#000000;stroke-width:1.79999995;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
		self.write_circle(circle_style, 266.77084, 39.843746, 19)
		
		self.end_group()
	
	# Load card data
	
	def load_data(self, name):
		layers = [
			'water_medium_layer',
			'water_deep_layer',
			'shoreline_master_layer',
			'grass_master_layer',
			'forest_master_layer',
			'routes_layer',
			'labels_layer',
			'labels_guide_layer',
			'resources_layer',
			'edge_guides_layer',
		]
		borders = []
		layer_data = {}
		label_text = ''
		label_guide = ''
		resources = []
		
		found_layer = {}
		for layer in layers:
			found_layer[layer] = False
		input = open('svg-src/%s.svg' % (name), "r")
		current_layer = ''
		current_resource = ''
		current_extra = ''
		for line in input:
			if re.search(r'inkscape:groupmode="layer"', line):
				current_layer = ''
			for layer in layers:
				if re.search(layer, line):
					current_layer = layer

			# Parse labels and label guides
			if current_layer == 'labels_layer':
				#print 'labels_layer:', line
				#m = re.search(r'>([A-Za-z0-9 \'.-]+)(</tspan>)?</textPath>', line)
				m = re.search(r'>([^<]+)</textPath></text>', line)
				if m:
					label_text = m.group(1)
					#print '\tFound label text:', label_text
					found_layer[current_layer] = True
			elif current_layer == 'labels_guide_layer':
				#print 'labels_guide_layer:', line
				m = re.search(r' d="([^"]+)"', line)
				if m:
					label_guide = m.group(1)
					#print '\tFound label guide:', label_guide
					found_layer[current_layer] = True

			# Parse resources
			elif current_layer == 'resources_layer':
				m = re.search(r'id="resource-([A-Za-z]+)"', line)
				if m:
					res = m.group(1)
					m = re.search(r' transform="(.+)"', line)
					if m:
						resources.append([res, m.group(1)])
						found_layer[current_layer] = True
						#print '\tFound resource:', res
					else:
						current_resource = res
						current_layer = 'resources_layer-transform'
			elif current_layer == 'resources_layer-transform':
				m = re.search(r' transform="(.+)"', line)
				if m:
					resources.append([current_resource, m.group(1)])
					#print '\tFound resource:', current_resource
					current_resource = ''
					current_layer = 'resources_layer'
					found_layer[current_layer] = True

			# Parse the topology guides
			elif current_layer == 'edge_guides_layer':
				# Note assumes guides appear in order in file.
				m = re.search(r'id="guide\d-(\d)"', line)
				if m:
					border = m.group(1)
					borders.append(int(border))
					found_layer[current_layer] = True
			
			# Parse all other layers
			elif current_layer != '':
				m = re.search(r' d="([^"]+)"', line)
				if m:
					if found_layer[current_layer]:
						error('Multiple paths found in %s' % current_layer)
					#print '\tFound data for', current_layer
					layer_data[current_layer] = m.group(1)
					found_layer[current_layer] = True
		input.close()
		
		for layer in layers:
			if not found_layer[layer]:
				error('Unable to find data for %s' % layer)
				return
		if len(borders) != 4:
			print borders
			error('Unable to find all for borders')	
			
		card_data = [name, borders]
		card_data.append(layer_data['water_medium_layer'])
		card_data.append(layer_data['water_deep_layer'])
		card_data.append(layer_data['shoreline_master_layer'])
		card_data.append(layer_data['grass_master_layer'])
		card_data.append(layer_data['forest_master_layer'])
		card_data.append(layer_data['routes_layer'])

		label_data = [label_text, label_guide]

		card_data.append(label_data)
		card_data.append(resources)
		
		# Debugging
		if False:
			print name
			for layer in layers:
				print '\t# %s\n' % layer
				if layer == 'labels_layer':
					print "\t['%s',\t'%s'],\n" % (label_text, label_guide)
				elif layer == 'resources_layer':
					print resources
				elif layer == 'edge_guides_layer':
					print borders
				else:
					print '\t%s\n' % layer_data[layer]

		# Validate loaded data against expected card info
		info = card_info[name]
		target_borders = name[0:4]
		target_pattern = info[0]
		target_resources = info[1]
		target_todo = info[2]
		target_label = info[3]

		if target_borders != ''.join([str(x) for x in borders]):
			print 'Expected borders:', target_borders
			print 'Found borders:', borders
			error('Borders don\'t match expected')

		found_r = ''
		for r in resources:
			found_r += resource_encode[r[0]]
		if ''.join(sorted(target_resources)) != ''.join(sorted(found_r)):
			print 'Expected resources:', target_resources
			print 'Found resources:', resources
			error('Resources don\'t match expected')
		if label_text != target_label:
			print 'Expected label:', target_label
			print 'Found label:', label_text
			error('Label doesn\'t match expected')
			
		return card_data
		
	# Utilities

	def open_output_file(self, name):
		self.out = open('svg-out/%s.svg' % (name), "w")
		self.write_header()

	def close_output_file(self, name):
		self.write_footer()
		self.out.close()

		if self.options['png']:
			cwd = os.getcwd()
			
			# Generate PNG file.
			subprocess.call([
				"/Applications/Inkscape.app/Contents/Resources/bin/inkscape",
				"--file=%s/svg-out/%s.svg" % (cwd, name),
				"--export-png=%s/png-out/%s.png" % (cwd, name),
				"--export-dpi=300",
				"--export-text-to-path",
				"--without-gui"
				])

	def process_card(self, name):
		print name, self.seed

		data = self.load_data(name)

		self.open_output_file(name)
		self.draw_card(name, data)
		self.close_output_file(name)
	
	def gen(self):
		seed_base = 0
		seed_delta = 0
		
		id = self.options['id']
		if id != '' and not id in card_info:
			error('Invalid card id: %s' % id)

		for name in sorted(card_info.keys()):
			seed_delta += 1
			self.seed = seed_base + seed_delta

			# Random seed override
			if len(card_info[name]) >= 5:
				self.seed = card_info[name][4]

			# Process single card
			if id == '' or id == name:
				self.process_card(name)

	def check_res_count(self, desc, res, count):
		rlist = ['f','s','t','B','C','H']
		for r in rlist:
			if not res.count(r) == count:
				print('Failed Validation: %s. Wrong count for %s in %s. Expected %d' % (desc, r, ''.join(sorted(res)), count))
				self.warnings += 1
				
def usage():
	print "Usage: %s <options>" % sys.argv[0]
	print "where <options> are:"
	print "  --png   Generate PNG output files"
	sys.exit(2)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:],
			'p',
			['png', 'id='])
	except getopt.GetoptError:
		usage()

	options = {
		'png': False,
		'id': '',
	}
	
	for opt,arg in opts:
		if opt in ('-p', '--png'):
			options['png'] = True
		if opt in ('--id'):
			options['id'] = arg
			
	islands = IslandsGen(options)
	islands.gen()

if __name__ == '__main__':
	main()
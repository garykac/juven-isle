#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

# XML namespaces to include in <svg> tag.
XML_NAMESPACES = [
	'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
	'xmlns="http://www.w3.org/2000/svg"',
	'xmlns:cc="http://creativecommons.org/ns#"',
	'xmlns:xlink="http://www.w3.org/1999/xlink"',
	'xmlns:dc="http://purl.org/dc/elements/1.1/"',
	'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"',
	'xmlns:svg="http://www.w3.org/2000/svg"',
	'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"',
	]

class SVGGen(object):
	def __init__(self):
		self.out = 0
		self.indent_count = 0

		#self.bleed = 11.25 # = 1/8"
		#self.safe_margin = 11.25 # = 1/8"
					
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
		self.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
		self.write('<svg version="1.1" height="337.5" width="247.5" %s>\n' % ' '.join(XML_NAMESPACES))
		
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

	def write_rect(self, style, x, y, width, height, radius=None, transform=''):
		tag = '<rect x="%g" y="%g" width="%g" height="%g" style="%s" ' % (x, y, width, height, style)
		if radius != None:
			tag += 'ry="%f" ' % radius
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
	
	# Utilities

	def open_output_file(self, name):
		self.out = open(name, "w")
		self.write_header()

	def close_output_file(self):
		self.write_footer()
		self.out.close()

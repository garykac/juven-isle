#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from svgdef import *

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

class SvgGen(object):
	def __init__(self):
		self.reset()

	def reset(self):
		self.state = 'reset'
		
		self.out = 0
		self.indent_count = 0

		# Currently generates Inkscape v0.91 files.
		# Note that Inkscape v0.92 and later use 96dpi.
		self.dpi = 90
		
		self.width = 0
		self.height = 0
		
		self.filename = ''
		
		self.defs = []
	
	def set_size(self, width, height):
		if self.state != 'reset':
			print 'ERROR - set_size() must be called before begin()'
		self.width = width
		self.height = height

	def set_filename(self, filename):
		if self.state != 'reset':
			print 'ERROR - set_filename() must be called before begin()'
		self.filename = filename

	def add_def(self, svg_def):
		if self.state != 'reset':
			print 'ERROR - add_def() must be called before begin()'
		self.defs.append(svg_def)
		
	def begin(self):
		if self.state != 'reset':
			print 'ERROR - Call reset() before begin()'
		self.state = 'begin'
		
		self.out = open(self.filename, "w")
		self.write_header_()
		self.write_defs_()
		self.write_named_view_()

	def end(self):
		if self.state != 'begin':
			print 'ERROR - Call begin() before end()'
		self.state = 'end'

		self.write_footer_()
		self.out.close()
			
	def write_(self, str):
		self.out.write(self.get_indent())
		self.out.write(str)
	
	def write_raw_(self, str):
		self.out.write(str)

	def get_indent(self):
		return '  ' * self.indent_count
		
	def indent_(self, count=1):
		self.indent_count += count
	
	def outdent_(self, count=1):
		self.indent_count -= count
		
	def write_header_(self):
		self.write_('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
		self.write_('<svg version="1.1" height="%g" width="%g" ' % (self.height, self.width))
		# Mark as Inkscape 0.91 so that pixels are interpreted as 90dpi (vs. 96dpi in 0.92 and greater)
		self.write_('inkscape:version="0.91 r13725" ')
		self.write_('%s>\n' % ' '.join(XML_NAMESPACES))
		
		self.write_('<metadata>\n')
		self.indent_()
		self.write_('<rdf:RDF>\n')
		self.indent_()
		self.write_('<cc:Work rdf:about="">\n')
		self.indent_()
		self.write_('<dc:format>image/svg+xml</dc:format>\n')
		self.write_('<dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>\n')
		self.write_('<dc:title/>\n')
		self.write_('<dc:creator>\n')
		self.indent_()
		self.write_('<cc:Agent><dc:title>Gary Kacmarcik</dc:title></cc:Agent>\n')
		self.outdent_()
		self.write_('</dc:creator>\n')
		self.outdent_()
		self.write_('</cc:Work>\n')
		self.outdent_()
		self.write_('</rdf:RDF>\n')
		self.outdent_()
		self.write_('</metadata>\n')
		self.write_('\n')
		
	def write_footer_(self):
		self.write_('\n')
		self.write_('</svg>\n')

	def write_named_view_(self):
		self.write_('<sodipodi:namedview\n')
		self.indent_(2)
		self.write_('id="base"\n')
		self.write_('pagecolor="#ffffff"\n')
		self.write_('bordercolor="#666666"\n')
		self.write_('borderopacity="1.0"\n')
		self.write_('inkscape:pageopacity="0.0"\n')
		self.write_('inkscape:pageshadow="2"\n')
		self.write_('inkscape:zoom="2"\n')
		self.write_('inkscape:cx="115.37643"\n')
		self.write_('inkscape:cy="285.04449"\n')
		self.write_('inkscape:document-units="in"\n')
		self.write_('showgrid="true"\n')
		self.write_('units="in"\n')
		self.write_('inkscape:window-width="1392"\n')
		self.write_('inkscape:window-height="836"\n')
		self.write_('inkscape:window-x="39"\n')
		self.write_('inkscape:window-y="6"\n')
		self.write_('inkscape:window-maximized="0"\n')
		self.write_('inkscape:snap-grids="true"\n')
		self.write_('inkscape:snap-to-guides="true"\n')
		self.write_('inkscape:snap-nodes="true"\n')
		self.write_('inkscape:object-nodes="true"\n')
		self.write_('inkscape:snap-smooth-nodes="true"\n')
		self.write_('inkscape:snap-intersection-paths="true"\n')
		self.write_('inkscape:object-paths="true"\n')
		self.write_('inkscape:snap-bbox="true"\n')
		self.write_('inkscape:bbox-nodes="true"\n')
		self.write_('inkscape:snap-others="true"\n')
		self.write_('inkscape:bbox-paths="false"\n')
		self.write_('inkscape:snap-global="true" >\n')
		self.outdent_()
		
		self.write_('<inkscape:grid\n')
		self.indent_()
		self.write_('type="xygrid"\n')
		self.write_('id="grid3051"\n')
		self.write_('empspacing="2"\n')
		self.write_('visible="true"\n')
		self.write_('enabled="true"\n')
		self.write_('snapvisiblegridlinesonly="true"\n')
		self.write_('spacingx="0.0625in"\n')
		self.write_('spacingy="0.0625in"\n')
		self.write_('dotted="false"\n')
		self.write_('units="in" />\n')
		self.outdent_(2)
		self.write_('</sodipodi:namedview>\n')

	def write_defs_(self):
		self.write_('<defs>\n')
		self.indent_()

		for d in self.defs:
			for line in d.export():
				self.write_(line)
		
		self.outdent_()
		self.write_('</defs>\n')
		self.write_('\n')

	def start_layer(self, id, label, options=None):
		if options == None:
			options = {}
		hidden = options.get('hidden')
		if hidden == None:
			hidden = False
		locked = options.get('locked')
		if locked == None:
			locked = True

		tag = '<g inkscape:groupmode="layer" id="%s" inkscape:label="%s" ' % (id, label)
		if hidden:
			tag += 'style="display:none" '
		else:
			tag += 'style="display:inline" '
		if locked:
			tag += 'sodipodi:insensitive="true" '
		tag += '>\n'
		self.write_(tag)
		self.indent_()
		
	def end_layer(self):
		self.outdent_()
		self.write_('</g>\n')
	
	def start_group(self, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')
		transform = options.get('transform')

		tag = '<g '
		if id != None:
			tag += 'id="%s" ' % id
		if style != None:
			tag += 'style="%s" ' % style
		if transform != None:
			tag += 'transform="%s" ' % transform
		tag += '>\n'
		self.write_(tag)
		self.indent_()

	def end_group(self):
		self.outdent_()
		self.write_('</g>\n')
		
	def path(self, path, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')
		transform = options.get('transform')

		tag = '<path '
		if id != None and id != '':
			tag += 'id="%s" ' % id
		if style != None:
			tag += 'style="%s" ' % style
		if transform != None and transform != '':
			tag += 'transform="%s" ' % transform
		tag += 'd="%s" ' % path
		tag += 'inkscape:connector-curvature="0" />\n'
		self.write_(tag)
	
	def clone(self, link, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')

		tag = '<use '
		if id != None and id != '':
			tag += 'id="%s" ' % id
		tag += 'xlink:href="#%s" height="100%%" width="100%%" x="0" y="0" ' % link
		if style != None:
			tag += 'style="%s" ' % style
		tag += '/>\n'
		self.write_(tag)

	def rect(self, x, y, width, height, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')
		radius = options.get('radius')
		transform = options.get('transform')
		
		tag = '<rect '
		if id != None and id != '':
			tag += 'id="%s" ' % id
		tag += 'x="%g" y="%g" width="%g" height="%g" ' % (x, y, width, height)
		if style != None:
			tag += 'style="%s" ' % (style)
		if radius != None:
			tag += 'ry="%f" ' % radius
		if transform != None and transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write_(tag)
	
	def circle(self, cx, cy, r, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')
		transform = options.get('transform')

		tag = '<circle '
		if id != None and id != '':
			tag += 'id="%s" ' % id
		tag += 'cx="%f" cy="%f" r="%f" ' % (cx, cy, r)
		if style != None:
			tag += 'style="%s" ' % (style)
		if transform != None and transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write_(tag)
	
	def ellipse(self, cx, cy, rx, ry, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')
		transform = options.get('transform')

		tag = '<ellipse '
		if id != None and id != '':
			tag += 'id="%s" ' % id
		tag += 'cx="%f" cy="%f" rx="%f" ry="%f" ' % (cx, cy, rx, ry)
		if style != None:
			tag += 'style="%s" ' % (style)
		if transform != None and transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write_(tag)

	def text(self, x, y, text, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')
		transform = options.get('transform')

		tag = '<text xml:space="preserve" '
		if id != None and id != '':
			tag += 'id="%s" ' % id
		tag += 'x="%g" y="%g" ' % (x, y)
		if style != None:
			tag += 'style="%s" ' % (style)
		if transform != None and transform != '':
			tag += 'transform="%s" ' % transform
		tag += '\n>%s</text>' % text
		self.write_(tag)

	def text_path(self, text, path_id, options=None):
		if options == None:
			options = {}
		style = options.get('style')
		id = options.get('id')
		transform = options.get('transform')
		textpath_style = options.get('textpath-style')

		tag = '<text xml:space="preserve" style="%s">' % style
		tag += '<textPath '
		if textpath_style != None:
			tag += 'style="%s" ' % textpath_style
		tag += 'xlink:href="#%s"\n' % path_id
		tag += '>%s</textPath></text>\n' % text
		self.write_(tag)

	def image(self, x, y, width, height, link, options=None):
		if options == None:
			options = {}
		id = options.get('id')
		transform = options.get('transform')
	
		tag = '<image '
		if id != None and id != '':
			tag += 'id="%s" ' % id
		tag += 'x="%g" y="%g" width="%g" height="%g" ' % (x, y, width, height)
		tag += 'xlink:href="%s" ' % link
		if transform != None and transform != '':
			tag += 'transform="%s" ' % transform
		tag += '/>\n'
		self.write_(tag)

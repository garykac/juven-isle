#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SvgDef(object):
	def __init__(self):
		self.type = '?'
		self.name = ''

	def export(self):
		return []

class SvgDefTexture(SvgDef):
	def __init__(self, name, octaves, seed, freq, blur):
		self.type = 'texture'
		self.name = name

		self.octaves = octaves
		self.seed = seed
		self.freq = freq
		self.blur = blur

	def export(self):
		tag = []
		tag.append('<filter inkscape:label="%s" style="color-interpolation-filters:sRGB" id="%s">\n' % (self.name, self.name))
		tag.append('  <feTurbulence numOctaves="%d" seed="%d" type="turbulence" baseFrequency="%f" result="result1" />\n' % (self.octaves, self.seed, self.freq))
		tag.append('  <feColorMatrix result="result0" in="SourceGraphic" type="luminanceToAlpha" />\n')
		tag.append('  <feColorMatrix result="result2" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0.4 0 " />\n')
		tag.append('  <feComposite in="result2" operator="over" in2="result1" />\n')
		tag.append('  <feColorMatrix result="result91" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 10 -4 " />\n')
		tag.append('  <feComposite operator="out" in="SourceGraphic" in2="result91" />\n')
		tag.append('  <feGaussianBlur stdDeviation="%f" />\n' % self.blur)
		tag.append('  <feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 " />\n')
		tag.append('</filter>\n')
		return tag

class SvgDefFilterBlur(SvgDef):
	def __init__(self, name, x, y, width, height, stddev):
		self.type = 'filter'
		self.name = name

		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.stddev = stddev

	def export(self):
		tag = []
		tag.append('<filter inkscape:collect="always" inkscape:label="%s" style="color-interpolation-filters:sRGB" id="%s" x="%f" y="%f" width="%f" height="%f">\n' % (self.name, self.name, self.x, self.y, self.width, self.height))
		tag.append('  <feGaussianBlur inkscape:collect="always" stdDeviation="%f" />\n' % self.stddev)
		tag.append('</filter>\n')
		return tag

class SvgDefRoughenTurbulence(SvgDef):
	def __init__(self, name, octaves, seed, freq, scale):
		self.type = 'roughen-turbulence'
		self.name = name

		self.octaves = octaves
		self.seed = seed
		self.freq = freq
		self.scale = scale

	def export(self):
		tag = []
		tag.append('<filter inkscape:label="%s" style="color-interpolation-filters:sRGB" id="%s">\n' % (self.name, self.name))
		tag.append('  <feTurbulence numOctaves="%d" seed="%d" type="turbulence" baseFrequency="%f" result="turb" />\n' % (self.octaves, self.seed, self.freq))
		tag.append('  <feDisplacementMap scale="%f" yChannelSelector="G" xChannelSelector="R" in="SourceGraphic" in2="turb" />\n' % self.scale)
		tag.append('</filter>\n')
		return tag

class SvgDefRoughenNoise(SvgDef):
	def __init__(self, name, octaves, seed, freq1, freq2, scale):
		self.type = 'roughen-noise'
		self.name = name

		self.octaves = octaves
		self.seed = seed
		self.freq1 = freq1
		self.freq2 = freq2
		self.scale = scale

	def export(self):
		tag = []
		tag.append('<filter inkscape:label="%s" style="color-interpolation-filters:sRGB" id="%s">\n' % (self.name, self.name))
		tag.append('  <feTurbulence numOctaves="%d" seed="%d" type="fractalNoise" baseFrequency="%f %f" result="turb" />\n' % (self.octaves, self.seed, self.freq1, self.freq2))
		tag.append('  <feDisplacementMap scale="%f" yChannelSelector="G" xChannelSelector="R" in="SourceGraphic" in2="turb" />\n' % self.scale)
		tag.append('</filter>\n')
		return tag

class SvgDefGradientStops(SvgDef):
	def __init__(self, name, stops):
		self.type = 'roughen-noise'
		self.name = name

		self.stops = stops

	def export(self):
		tag = []
		tag.append('<linearGradient id="%s" inkscape:collect="always">\n' % self.name)
		for stop in self.stops:
			tag.append('  <stop offset="%f" style="stop-color:#%s;stop-opacity:%f" />\n' % (stop[0], stop[1], stop[2]))
		tag.append('</linearGradient>\n')
		return tag

class SvgDefGradientLinear(SvgDef):
	def __init__(self, name, xlink, x1, y1, x2, y2, transform):
		self.type = 'roughen-noise'
		self.name = name

		self.xlink = xlink
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.transform = transform

	def export(self):
		tag = '<linearGradient id="%s" xlink:href="#%s" x1="%f" y1="%f" x2="%f" y2="%f" ' % (self.name, self.xlink, self.x1, self.y1, self.x2, self.y2)
		if self.transform != '':
			tag += 'gradientTransform="%s" ' % self.transform
		tag += 'gradientUnits="userSpaceOnUse" inkscape:collect="always" />\n'
		return [tag]

class SvgDefGradientRadial(SvgDef):
	def __init__(self, name, xlink, cx, cy, fx, fy, r, transform):
		self.type = 'roughen-noise'
		self.name = name

		self.xlink = xlink
		self.cx = cx
		self.cy = cy
		self.fx = fx
		self.fy = fy
		self.r = r
		self.transform = transform

	def export(self):
		tag = '<radialGradient id="%s" xlink:href="#%s" cx="%f" cy="%f" fx="%f" fy="%f" r="%f" gradientUnits="userSpaceOnUse" gradientTransform="%s" inkscape:collect="always" />\n' % (self.name, self.xlink, self.cx, self.cy, self.fx, self.fy, self.r, self.transform)
		return [tag]

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

DIR = "svg-2.5in-822px"
CWD = os.getcwd()

for file in os.listdir(DIR):
	if file.endswith(".svg"):
		(base, ext) = os.path.splitext(file)
		base_split = base.split('-')
		src = os.path.join(CWD, DIR, file)
		dst = '%s.png' % os.path.join(CWD, DIR, '_export', base_split[0])

		if not os.path.exists(dst) or (os.path.getmtime(src) > os.path.getmtime(dst)):
			print 'Exporting', file

			# Generate PNG file.
			subprocess.call([
				"/Applications/Inkscape.app/Contents/Resources/bin/inkscape",
				"--file=%s" % src,
				"--export-png=%s" % dst,
				"--export-dpi=300",
				"--export-text-to-path",
				"--without-gui"
				])
		else:
			print 'Skipping', file


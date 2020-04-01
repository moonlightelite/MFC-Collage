#!/usr/bin/python2

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import re
import tempfile
import requests
import argparse
from PIL import Image
from photocollage.collage import Page, Photo
from photocollage.render import RenderingTask, build_photolist, QUALITY_BEST

url = "https://myfigurecollection.net/profile/{0}/collection/"
img_url = "https://static.myfigurecollection.net/pics/figure/large/{0}.jpg"
img_url_big = "https://static.myfigurecollection.net/pics/figure/big/{0}.jpg"

def run(args):
  tmp_file = []
  tmp_file_photo = []
  p = requests.get(url.format(args.user)).content
  url_re = re.compile(r'\<a href="\/item\/(\d+)"')
  fig_ids = re.findall(url_re, p)

  for i in fig_ids:
    u = img_url.format(i)
    q = requests.get(u).content
    print("Downloading " + u)
    if not q or len(q) < 300:
      print("Retrying " + u)
      u = img_url_big.format(i)
      q = requests.get(u).content
    fp = tempfile.NamedTemporaryFile()
    fp.write(q)
    tmp_file.append(fp)

  tmp_file_photo = build_photolist(tmp_file)

  pa = Page(1800,4,8)
  for t in tmp_file_photo:
    pa.add_cell(t)

  pa.adjust()
  t = RenderingTask(pa, output_file=args.output, quality=QUALITY_BEST)
  t.start()
  print("Done")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Generate collage.')
  parser.add_argument('-u', '--user', help='MFC user name')
  parser.add_argument('-o', '--output', help='Output file')
  args = parser.parse_args()

  run(args)




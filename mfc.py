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

import os,sys
import re
import tempfile
import requests
import argparse
import math
from PIL import Image
from photocollage.collage import Page, Photo
from photocollage.render import RenderingTask, build_photolist, QUALITY_BEST

owned_url = "https://myfigurecollection.net/users.v4.php?mode=view&username={0}&tab=collection&page=1&status=2&output=2&current=keywords&rootId=0&categoryId=-1&sort=category&order=asc"
ordered_url = "https://myfigurecollection.net/users.v4.php?mode=view&username={0}&tab=collection&rootId=0&status=1"
img_url = "https://static.myfigurecollection.net/pics/figure/large/{0}.jpg"
img_url_big = "https://static.myfigurecollection.net/pics/figure/big/{0}.jpg"

def run(args):
  tmp_file = []
  tmp_file_photo = []
  if args.user:
    if args.mode == "owned":
      url = owned_url
    elif args.mode == "ordered":
      url = ordered_url
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
      with open("/tmp/{0}".format(i), "wb") as fd:
        fd.write(q)
      tmp_file.append(fp)
  elif args.input:
    for r, d, f in os.walk(args.input):
      for file in f:
        tmp_file.append(open(os.path.join(r, file), 'rb'))

  total_x = total_y = 0
  harmonic_mean_sum = 0
  for i in tmp_file:
    with Image.open(i.name) as img:
      total_x += img.size[0]
      total_y += img.size[1]
      ratio = (1 / (float(total_y) / total_x))
      harmonic_mean_sum += ratio
  harmonic_mean = len(tmp_file) / harmonic_mean_sum
  print(harmonic_mean)

  tmp_file_photo = build_photolist(tmp_file)
  pa = Page(min(4800, total_y / 2), harmonic_mean * 3, int(math.sqrt(len(tmp_file))))
  for t in tmp_file_photo:
    pa.add_cell(t)

  pa.adjust()
  t = RenderingTask(pa, output_file=args.output, quality=QUALITY_BEST)
  t.start()
  print("Done")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Generate collage.')
  parser.add_argument('-u', '--user', help='MFC user name')
  parser.add_argument('-m', '--mode', help='"owned" or "ordered"')
  parser.add_argument('-o', '--output', help='Output file')
  parser.add_argument('-i', '--input', help='Input Folder')
  args = parser.parse_args()

  run(args)




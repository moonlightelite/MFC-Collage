# mfc_collage
MFC collage for everyone

Need
- https://github.com/adrienverge/PhotoCollage
- https://pypi.org/project/Pillow/
- Python 2 (3 should work but not tested)

Usage:
```
$ ./mfc.py -h
usage: mfc.py [-h] [-u USER] [-m MODE] [-o OUTPUT] [-i INPUT]

Generate collage.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  MFC user name
  -m MODE, --mode MODE  "owned" or "ordered"
  -o OUTPUT, --output OUTPUT
                        Output file
  -i INPUT, --input INPUT
                        Input Folder
```

Q: Photos are clipped!

A: *Shrugged* 

Q: Why Python 2 and not 3 you stupid-

A: *Shrugged*

Q: Photo quality is bad!

A: Try using Pillow instead of PIL

Example output:

<img src="https://i.imgur.com/kV0ZkUc.jpg" data-canonical-src="https://i.imgur.com/kV0ZkUc.jpg" width="200">

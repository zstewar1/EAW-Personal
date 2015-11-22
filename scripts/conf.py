import pathlib

scriptdir = pathlib.Path(__file__).resolve().parent
moddir = scriptdir.parent.parent
srcdir = moddir / 'Source/data'
outdir = scriptdir.parent / 'data'

srcxml = srcdir / 'xml'
outxml = outdir / 'xml'

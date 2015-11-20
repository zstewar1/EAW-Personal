import pathlib

scriptdir = pathlib.Path(__file__).resolve().parent
moddir = scriptdir.parent.parent
srcdir = moddir / 'Source/Data'
outdir = scriptdir.parent / 'data'

srcxml = srcdir / 'XML'
outxml = outdir / 'xml'

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

DATA=[('imageformats',['C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qjpeg4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qgif4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qico4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qmng4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qsvg4.dll',
    'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qtiff4.dll'
    ]), ('', ['EY-logo-Social.png'])]

setup(
    options = {'py2exe': { 'compressed': True,"includes":["sip"]}},
    windows = [{'script': "C:\Python27\Lib\site-packages\Programs\DataReformer\v1.7\DataCleansingProgram.py"}],
    zipfile = None,
    data_files = DATA,
)

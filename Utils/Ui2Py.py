import os
import sys
import subprocess
import time
today = time.strftime('%Y/%m/%d',time.localtime()).lower()

def generate(fname=None, version='V1.0', output_py=None):
    # call uic to create .py file from .ui
    root, ext = os.path.splitext(fname)

    if not output_py:
        output_py = fname.replace(ext, '_' + ext[1:]) + '.py'

    if ext == '.ui':
       cmd = ['pyuic5', '-x', fname, '-o', output_py]
       subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE).communicate()
    elif ext == '.css':
        with open(fname) as css, open(output_py, 'wb') as out:
            out.write("style = '''\n")
            out.write(css.read())
            out.write("'''\n")

if __name__ == '__main__':
    generate(fname='..\\UI\\ml.ui')
    print ('DONE')

import os

os.environ["OCTAVE_EXECUTABLE"] = (
    r"D:\Octavio\GNU Octave\Octave-10.3.0\mingw64\bin\octave-cli.exe"
)

from oct2py import Oct2Py

oc = Oct2Py()
print(oc.eval("1+1"))
oc.exit()

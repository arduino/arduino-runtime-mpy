#!/bin/bash
#
# Install Arduino Runtime to a MicroPython board using mpremote.
# This script accepts an optional argument to compile .py files to .mpy.
# Simply run the script with the optional argument:
#
# ./install.sh mpy


PKGDIR="arduino"
SRCDIR=$PKGDIR
LIBDIR="lib"

# File system operations such as "mpremote mkdir" or "mpremote rm"
# will generate an error if the folder exists or if the file does not exist.
# These errors can be ignored.
# 
# Traceback (most recent call last):
#   File "<stdin>", line 2, in <module>
# OSError: [Errno 17] EEXIST

echo "Creating $LIBDIR on board"
mpremote mkdir "${LIBDIR}"
echo "Creating $LIBDIR/$PKGDIR on board"
mpremote mkdir "/${LIBDIR}/${PKGDIR}"

ext="py"
if [ "$1" = "mpy" ]; then
  ext=$1
  echo "* * *"
  echo ".py files will be compiled to .mpy"
  echo "* * *"
fi

for py in $SRCDIR/*; do
    f_name=`basename $py`
    if [ "$ext" = "mpy" ]; then
      echo "Compiling $SRCDIR/$f_name to $SRCDIR/${f_name%.*}.$ext"
      mpy-cross "$SRCDIR/$f_name"
    fi
    
    echo "Deleting files from board"
    mpremote rm ":/${LIBDIR}/$PKGDIR/${f_name%.*}.py"
    mpremote rm ":/${LIBDIR}/$PKGDIR/${f_name%.*}.mpy"

    echo "Copying $SRCDIR/${f_name%.*}.$ext to :/${LIBDIR}/$PKGDIR/${f_name%.*}.$ext"
    mpremote cp $SRCDIR/${f_name%.*}.$ext ":/${LIBDIR}/$PKGDIR/${f_name%.*}.$ext" 
done

if [ "$ext" = "mpy" ]; then
  echo "cleaning up mpy files"
  rm $SRCDIR/*.mpy
fi

echo "resetting target board"
mpremote reset
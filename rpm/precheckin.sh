#!/bin/sh
ARCHS="armv7l armv7hl mipsel"

echo -n "arch i486 targets " > baselibs.conf
for x in $ARCHS; do
	cp -v sb2-tools-qt5-template-rpmlintrc sb2-tools-qt5-$x-rpmlintrc
	sed "s/@ARCH@/$x/g" sb2-tools-qt5-template.spec | sed "s/ExclusiveArch: nothing/ExclusiveArch: %{ix86}/g" > sb2-tools-qt5-$x.spec	
	echo -n "$x:inject " >> baselibs.conf
done

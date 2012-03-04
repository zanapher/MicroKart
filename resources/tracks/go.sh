#!/bin/bash
for i in ??t.gif; do convert $i ${i/gif/pgm}; done
for i in ??s.gif; do convert $i ${i/gif/pgm}; done
for i in ??b.gif; do convert $i ${i/gif/pgm}; done
for i in ??bm.pgm; do convert $i ${i/pgm/gif}; done
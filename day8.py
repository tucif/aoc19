#!/usr/bin/env python3
import fileinput
from io import StringIO
from collections import Counter
import logging

def main():
  logging.basicConfig(level=logging.INFO)
  image = read_image_from_input()
  layercounter = find_fewest_zeroes(image)
  result = phase_one(layercounter)
  logging.info(f"{result=}")
  decode_image(image)


def decode_image(image):
  final_image = [None] * len(image[0])
  for l, layer in enumerate(image):
    for p, pixel in enumerate(layer):
      if pixel != '2' and final_image[p] is None:
        final_image[p] = pixel

  logging.info("Final image:")
  print_layer(final_image)
      
def print_layer(layer, width=25):
  for i,pixel in enumerate(layer):
    print(pixel.replace('0', ' '), end=' ')
    if (i+1)%width == 0:
      print()



def phase_one(layer):
  return layer['1'] * layer['2']
  

def find_fewest_zeroes(image):
  fewest_zeroes = None
  layer_with_fewest = None
  for layerdata in image:
    layer = Counter(layerdata)
    zeroes_in_layer = layer['0']
    if fewest_zeroes is None or zeroes_in_layer < fewest_zeroes:
      fewest_zeroes = zeroes_in_layer
      layer_with_fewest = layer
  logging.debug(f"{layer_with_fewest=}")
  logging.debug(f"{fewest_zeroes=}")
  return layer_with_fewest


def read_image_from_input():
  buf = StringIO(fileinput.input().readline())
  layers = []
  while True:
    layer = buf.read(150).rstrip()
    if layer:
      layers.append(layer)
    else:
      break

  logging.info(f"Found {len(layers)} layers")
  return layers
    
  

if __name__ == '__main__':
  main()

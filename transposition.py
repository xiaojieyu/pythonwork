# Transposition Cipher Program

import sys
import argparse
import math

def encryptMessage(key, message):
  print key
  # Each string in ciphertext represents a column in the grid.
  ciphertext = [''] * key

  # Loop through each column in ciphertext.
  for col in range(key):
    pointer = col

    # keep looping until pointer goes past the length of the message.
    while pointer < len(message):
      # Place the character at pointer in message at then end of the
      # current column in the ciphertext list
      ciphertext[col] += message[pointer]
      # move pointer over
      pointer += key

  # Convert the ciphertext list into a single string value and return it.
  return ''.join(ciphertext)

def decryptMessage(key, message):
  numOfColumns = math.ceil(len(message)/float(key))
  numOfRows = key
  numOfShadedBoxes = numOfColumns * numOfRows - len(message)

  plaintext = [''] * int(numOfColumns)

  col = 0
  row = 0

  for symbol in message:
    plaintext[col] += symbol
    print col, row, plaintext[col]
    col += 1

    if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows -
                                 numOfShadedBoxes):
      col = 0
      row += 1

  return ''.join(plaintext)


def main():

  parser = argparse.ArgumentParser("Transposition Cipher Program")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-d", "--decrypt", help="decrypt cipher text")
  group.add_argument("-e", "--encrypt", help="encrypt cipher text")

  parser.add_argument("-k", "--key", type=int, help="secret key")
  parser.add_argument("--verbose", help="increase output verbosity", action="store_true")

  args = parser.parse_args()

  myMessage = 'Common sense is not so common.'
  myKey = 8

  if args.key:
    myKey = args.key

  if args.encrypt:
    myMessage = args.encrypt
    ciphertext = encryptMessage(myKey, myMessage)

    # Print the encrypted string in ciphertext to the screen, with
    # a | (called "pipe" character) after it in case there are spaces at
    # the end of the encrypted message.
    print(ciphertext + '|')

  if args.decrypt:
    plaintext = decryptMessage(myKey, args.decrypt)
    print (plaintext + '|')

if __name__ == "__main__":
  main()

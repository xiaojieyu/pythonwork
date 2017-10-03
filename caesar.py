# Caesar Cipher

import sys
import argparse

# every possible symbol that can be encrypted
LETTERS = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]\
^_`abcdefghijklmnopqrstuvwxyz{|}~'

# the default encryption/decryption key
default_key = 13

def caesar_cipher(message, key, mode):
  ''' encrypt or decrypt message with caesar algorithm '''
  translated = ''

  #run the encryption/decryption code on each symbol in the message string
  for symbol in message:
    if symbol in LETTERS:
      # get the encrypted (or decrypted) number for this symbol
      num = LETTERS.find(symbol)
      if mode == 'encrypt':
        num += key
      elif mode == 'decrypt':
        num -= key

      # handle the wrap-around if num is larger than the length of
      # LETTERS or less than 0
      if num >= len(LETTERS):
        num -= len(LETTERS)
      elif num < 0:
        num += len(LETTERS)

      # add encrypted/decrypted number's symbol at the end of translated
      translated += LETTERS[num]

    else:
      # just add the symbol without encrypting/decrypting
      translated += symbol

  return translated

def brute_force_caesar(message):
  for key in range(len(LETTERS)):
    translated =  caesar_cipher(message, key, 'decrypt')
    print "Key #%2d:"%key, translated


def main():
  parser = argparse.ArgumentParser("Caesar Cipher Program")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-d", "--decrypt", help="decrypt cipher text")
  group.add_argument("-e", "--encrypt", help="encrypt cipher text")
  group.add_argument("-b", "--bruteforce", help="brute force decrypt cipher\
                     text")
  parser.add_argument("-k", "--key", type=int, help="secret key")
  parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()

  if args.verbose:
    print "verbosity turned on"

  if args.key:
    key = args.key
  else:
    key = default_key

  if args.encrypt:
    print "message: %s" % args.encrypt
    print "cipher :", caesar_cipher(args.encrypt, key, 'encrypt')

  if args.decrypt:
    print "cipher : %s" % args.decrypt
    print "message: ", caesar_cipher(args.decrypt, key, 'decrypt')

  if args.bruteforce:
    print "brute force: %s" % args.decrypt
    print brute_force_caesar(args.bruteforce)

if __name__ == "__main__":
  main()


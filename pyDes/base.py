#!/usr/bin/env python
# encoding: utf-8

"""
   @author: Eric Wong
  @license: MIT Licence
  @contact: ericwong@zju.edu.cn
     @file: core.py
     @time: 2018-12-30 11:10
"""

import struct

from .core import derive_keys, encode_block
class DesKey(object):
    """A class for encryption using DES Key"""
    def __init__(self, key):
        self.round_keys_as_int = guard_key(key)
        self.__decryption_key = self.round_keys_as_int[::-1]
        self.__key = key

    def encrypt(self, message):
        """Encrypts the message with the key object.

        :param message: {bytes} The message to be encrypted
        :param initial: {union[bytes, int, long, NoneType]} The initial value, using CBC Mode when is not None
        :param padding: {any} Uses PKCS5 Padding when TRUTHY
        :return: {bytes} Encrypted bytes
        """
        return handle(message, self.round_keys_as_int, encryption=True)

    def decrypt(self, message, initial=None, padding=False):
        """Decrypts the encrypted message with the key object.

        :param message: {bytes} The message to be decrypted
        :param initial: {union[bytes, int, long, NoneType]} The initial value, using CBC Mode when is not None
        :param padding: {any} Uses PKCS5 Padding when TRUTHY
        :return: {bytes} Decrypted bytes
        """
        return handle(message, self.__decryption_key, initial, padding, 0)

    def __hash__(self):
        return hash((self.__class__, self.round_keys_as_int))


def encode(block, key, encryption):
    for k in key:
        block = encode_block(block, k, encryption)
        encryption = not encryption

    return block


def guard_key(key: bytes):
    if(len(key) != 8):
        raise ValueError("Key size should be 8 bytes")
    return tuple(derive_keys(key)),

def guard_message(message):
    assert isinstance(message, bytes), "The message should be bytes"
    assert len(message) % 8 == 0, "The message length should be multiple of 8"
    return message


def guard_initial(initial):
    if initial is not None:
        if isinstance(initial, bytearray):
            initial = bytes(initial)
        if isinstance(initial, bytes):
            assert len(initial) & 7 == 0, "The initial value should be of length 8(as `bytes` or `bytearray`)"
            return struct.unpack(">Q", initial)[0]
        # assert isinstance(initial, number_type), "The initial value should be an integer or bytes object"
        assert -1 < initial < 1 << 32, "The initial value should be in range [0, 2**32) (as an integer)"
    return initial


def handle(message, key, encryption):
    message = guard_message(message)

    blocks = []
    for i in range(0, len(message), 8):
        block = struct.unpack(">Q", message[i: i + 8])[0]
        blocks.append(block)

    encoded_blocks = []
    for block in ecb(blocks, key, encryption):
        encoded_blocks.append(block)

    ret = b""
    for block in encoded_blocks:
        ret += struct.pack(">Q", block)

    if not encryption:
        ret = ret[:-ord(ret[-1:])]

    return ret


def ecb(blocks, key, encryption):
    for block in blocks:
        yield encode(block, key, encryption)

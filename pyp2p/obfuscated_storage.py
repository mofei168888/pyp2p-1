#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

import logging
import uuid
import random
import string
import pickle
from Crypto.Cipher import AES
from Crypto import Random
KEY_LEN = 24

class ObfuscatedStorage(object):
    """

        Implements a permanent storage that is not human readable

    """

    def __init__(self, filename="store.lock"):
        """
        """
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("storage")

        self.filename = filename

    def make_key(self, length):
        """ Make a key """
        generator = random.Random() 
        generator.seed(uuid.getnode())
        return str().join(generator.choice(string.hexdigits) 
                         for _ in range(length))

    def encrypt(self, data, key):
        """ Encrypt data"""
        init_vector = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, init_vector)
        crypto = init_vector + cipher.encrypt(data)
        self.logger.debug("Encrypting with key %s, init vector:%s" % (key, init_vector))

        return crypto

    def decrypt(self, data, key):
        """ Decode cipher"""
        init_vector = data[:AES.block_size]
        data = data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CFB, init_vector)
        msg = cipher.decrypt(data)
        self.logger.debug("Decrypting with key %s, init vector:%s" % (key, init_vector))
        return msg

    def store(self, data):
        """ write data in storage
        """

        self.logger.info("Storing data %s" % data)

        data = pickle.dumps(data)
        data = self.encrypt(data, self.make_key(KEY_LEN))

        with open(self.filename, 'wb') as store:
            store.write(data) 

    def retrieve(self):
        self.logger.info("Retreiving data...")

        with open(self.filename, 'rb') as store:
            raw = store.read()

        serialized = self.decrypt(raw, self.make_key(KEY_LEN))
        payload = pickle.loads(serialized)

        self.logger.debug("Retreived %s" % payload)
        return payload

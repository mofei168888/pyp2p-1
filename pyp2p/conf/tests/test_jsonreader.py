#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Legrand France
# All rights reserved

import os
from nose.tools import assert_equal
from pyp2p.conf.jsonreader import JSONConfReader


class TestJSONConfReader:

    def setup(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        conf_filename = os.path.join(current_dir, "conf.json")
        self.conf_reader = JSONConfReader(conf_filename)

    def test_conf_reader(self):

        current = self.conf_reader.conf["current"]
        assert_equal("iot.legrand.net", current)

        assert_equal("p2pserver.cloudapp.net",
                     self.conf_reader.conf["domains"][current]["server"])
        assert_equal("5222",
                     self.conf_reader.conf["domains"][current]["port"])

#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *

def givenIHaveCreatedAConsultation(node, text, questions=False, included=False):
  print("givenIHaveCreatedAConsultation")
  print(node, text, questions, included)

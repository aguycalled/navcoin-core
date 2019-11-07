#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *

def thenTheAnswersShouldBeSupported(node=None, 
consultHash=None,
supportedAnswers=None):
  print("thenTheAnswersShouldBeSupported")

  if (node is None 
  or consultHash is None 
  or supportedAnswers is None 
  or len(supportedAnswers) is 0):
    print('thenTheAnswersShouldBeSupported: invalid parameters')
    assert(False)

  try:
    consult = node.getconsultation(consultHash)
  except JSONRPCException as e:
    print(e.error)
    assert(False)  

  for answer in consult["answers"]:
    if (answer["hash"] in supportedAnswers):
      assert_equal(answer["state"], 1)
    else:
      assert_equal(answer["state"], 0)

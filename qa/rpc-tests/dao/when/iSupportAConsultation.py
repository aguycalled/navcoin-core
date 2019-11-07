#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *
from dao.when.iEndTheVotingCycle import whenIEndTheVotingCycle

def whenISupportAConsultation(node=None,
consultHash=None,
endCycleBefore=False,
endCycleAfter=False):
  print("whenISupportAConsultation")

  if (node is None 
  or consultHash is None):
    print('whenISupportAConsultation: invalid parameters')
    assert(False)

  if (endCycleBefore):
    whenIEndTheVotingCycle(node)

  try:
    node.support(consultHash)
  except JSONRPCException as e:
    print(e.error)
    assert(False) 

  slow_gen(node, 1)

  if (endCycleAfter):
    whenIEndTheVotingCycle(node)

#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *
from dao.when.iEndTheVotingCycle import whenIEndTheVotingCycle

def whenISupportAnswers(
node=None, 
consultHash=None, 
answersToSupport=None, 
endCycleBefore=False, 
endCycleAfter=False):
  print("whenISupportAnswers")

  if (node is None 
  or consultHash is None 
  or answersToSupport is None 
  or answersToSupport is None 
  or len(answersToSupport) is 0):
    print('whenISupportAnswers: invalid parameters')
    assert(False)

  if (endCycleBefore):
    whenIEndTheVotingCycle(node)

  for answerHash in answersToSupport:
    try:
      node.support(answerHash)
    except JSONRPCException as e:
      print(e.error)
      assert(False)  

  slow_gen(node, 1)

  try:
    consult = node.getconsultation(consultHash)
  except JSONRPCException as e:
    print(e.error)
    assert(False)  

  for answer in consult["answers"]:
    if (answer["hash"] in answersToSupport):
      assert(answer["support"] > 0)
    else:
      assert(answer["support"] == 0)

  if (endCycleAfter):
    whenIEndTheVotingCycle(node)

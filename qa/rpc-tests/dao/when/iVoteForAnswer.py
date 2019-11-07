#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *
from dao.when.iEndTheVotingCycle import whenIEndTheVotingCycle

def whenIVoteForAnswer(node=None, 
consultHash=None, 
answerHash=None,
 vote=None):
  print("whenIVoteForAnswer")

  if (node is None 
  or consultHash is None 
  or answerHash is None 
  or vote is None):
    print('whenIVoteForAnswer: invalid parameters')
    assert(False)

  try:
    node.consultationvote(answerHash, vote)
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
    if (answer["hash"] == answerHash):
      assert(answer["votes"] > 0)
    else:
      assert(answer["votes"] == 0)


#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *

def whenIEndTheVotingCycle(node=None):
  print("whenIEndTheVotingCycle")

  if node is None:
    print('whenIEndTheVotingCycle: invalid parameters')
    assert(False)

  try:
    blocksPerCycle = node.cfundstats()["consensus"]["blocksPerVotingCycle"]  
    assert(isinstance(blocksPerCycle, int) and blocksPerCycle > 0)
  except JSONRPCException as e:
    print(e.error)
    assert(False)

  try:
    blockCount = node.getblockcount()
    assert(isinstance(blockCount, int) and blockCount > 0)
  except JSONRPCException as e:
    print(e.error)
    assert(False)

  blocksLeft = blocksPerCycle - blockCount % blocksPerCycle

  print(blockCount, blocksLeft)

  slow_gen(node, blocksLeft)

  try:
    newBlockCount = node.getblockcount()
    assert(isinstance(blockCount, int) and newBlockCount > blockCount)
    assert_equal(newBlockCount % blocksPerCycle, 0)
  except JSONRPCException as e:
    print(e.error)
    assert(False)

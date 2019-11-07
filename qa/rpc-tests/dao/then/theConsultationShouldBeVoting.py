#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *

def thenTheConsultationShouldBeVoting(node=None, 
consultHash=None):
  print("thenTheConsultationShouldBeVoting")

  if (node is None 
  or consultHash is None):
    print('thenTheConsultationShouldBeVoting: invalid parameters')
    assert(False)

  try:
    consult = node.getconsultation(consultHash)
  except JSONRPCException as e:
    print(e.error)
    assert(False)  
    
  assert_equal(consult["state"], 1)


#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *

def thenTheConsultationShouldBeAnswered(node=None,
consultHash=None,
expectedAnswerHash=None):
  print("thenTheConsultationShouldBeAnswered")

  if (node is None 
  or consultHash is None 
  or expectedAnswerHash is None):
    print('thenTheConsultationShouldBeAnswered: invalid parameters')
    assert(False)

  try:
    consult = node.getconsultation(consultHash)
  except JSONRPCException as e:
    print(e.error)
    assert(False)  
    
  assert_equal(consult["state"], 3)

  try:
    consultAnswer = node.getconsultationanswer(consultHash)
  except JSONRPCException as e:
    print(e.error)
    assert(False)  
  
  print(consult, consultAnswer)

  # TODO find out how to check the outcome / result of the consultation


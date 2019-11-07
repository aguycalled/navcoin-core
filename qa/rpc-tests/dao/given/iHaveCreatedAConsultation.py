#!/usr/bin/env python3
# Copyright (c) 2019 The NavCoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Expanded helper routines for regression testing of the NAV Coin community fund
#

from test_framework.util import *

def givenIHaveCreatedAConsultation(node=None, 
text=None, 
questions=None, 
withAnswers=False):
  print("givenIHaveCreatedAConsultation")

  if (node is None 
  or text is None):
    print('givenIHaveCreatedAConsultation: invalid parameters')
    assert(False)

  if questions is None:
    try:
      return node.createconsultation(text)["hash"]
    except JSONRPCException as e:
      print(e.error)
      assert(False)

  if (withAnswers is True 
  and questions is not None):
    try:
      hash = node.createconsultationwithanswers(text, questions)["hash"]
      slow_gen(node, 1)
    except JSONRPCException as e:
      print(e.error)
      assert(False)
  
  if (withAnswers is False 
  and questions is not None): 
    try:
      hash = node.createconsultation(text)["hash"]
      slow_gen(node, 1)
    except JSONRPCException as e:
      print(e.error)
      assert(False)

    slow_gen(node, 1)
    
    for question in questions:
      try:
        node.proposeanswer(hash, question)
      except JSONRPCException as e:
        print(e.error)
        assert(False)

    slow_gen(node, 1)

  consult = node.getconsultation(hash)

  for answer in consult["answers"]:
    assert(answer["string"] in questions)
  
  return hash




  


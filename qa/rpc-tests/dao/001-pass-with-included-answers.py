#!/usr/bin/env python3
# Copyright (c) 2019 The Navcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import sys, os #include the parent folder so the test_framework is available
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

from test_framework.test_framework import NavCoinTestFramework
from test_framework.cfund_util import *

from dao.given import *
from dao.when import *
from dao.then import *

import time

class DAO001PassWithIncludedAnswers(NavCoinTestFramework):
  """It should pass a consultation with included answers"""

  def __init__(self):
      super().__init__()
      self.setup_clean_chain = True
      self.num_nodes = 1

  def setup_network(self, split=False):
      self.nodes = []
      self.nodes = start_nodes(self.num_nodes, self.options.tmpdir, [["-debug=dao"],["-debug=dao"]])

  def run_test(self):

      self.nodes[0].staking(False)
      activate_softfork(self.nodes[0], "consultations")

      answers = ["A001", "A002", "A003"]
      
      consultHash = givenIHaveCreatedAConsultation(self.nodes[0], "C001", answers, True)

      answers = self.nodes[0].getconsultation(consultHash)["answers"]

      answersToSupport = [
        answers[0]["hash"],
        answers[1]["hash"],
        answers[2]["hash"],
      ]

      whenISupportAnswers(self.nodes[0], consultHash, answersToSupport, True)

      whenIEndTheVotingCycle(self.nodes[0])

      thenTheAnswersShouldBeSupported(self.nodes[0], consultHash, answersToSupport)

      whenISupportAConsultation(self.nodes[0], consultHash)

      whenIEndTheVotingCycle(self.nodes[0])

      thenTheConsultationShouldBeSupported(self.nodes[0], consultHash)

      whenIEndTheVotingCycle(self.nodes[0])

      thenTheConsultationShouldBeVoting(self.nodes[0], consultHash)

      whenIVoteForAnswer(self.nodes[0], consultHash, answers[1]["hash"], "yes")

      whenIEndTheVotingCycle(self.nodes[0])

      slow_gen(self.nodes[0], 30) # TODO find out why i have to generate 30 blocks here

      whenIEndTheVotingCycle(self.nodes[0])
      
      thenTheConsultationShouldBeAnswered(self.nodes[0], consultHash, answers[1]["hash"])

if __name__ == '__main__':
    DAO001PassWithIncludedAnswers().main()

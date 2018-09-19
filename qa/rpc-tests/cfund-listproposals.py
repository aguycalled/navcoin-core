#!/usr/bin/env python3
# Copyright (c) 2018 The Navcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import NavCoinTestFramework
from test_framework.util import *

import time


class CommunityFundProposalsTest(NavCoinTestFramework):
    """Tests the voting procedures of the Community fund."""

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 1

    def setup_network(self, split=False):
        self.nodes = start_nodes(self.num_nodes, self.options.tmpdir)
        self.is_network_split = False

    def run_test(self):
        # Get cfund parameters
        blocks_per_voting_cycle = self.nodes[0].cfundstats()["consensus"]["blocksPerVotingCycle"]

        # Make sure the cfund is active
        self.activate_cfund()

        # Donate to fund
        self.nodes[0].donatefund(100)

        # Create proposals
        created_proposals = {
            "pure_yes": self.nodes[0].createproposal(self.nodes[0].getnewaddress(), 1, 3600, "pure_yes")["hash"],
            "pure_no": self.nodes[0].createproposal(self.nodes[0].getnewaddress(), 1, 3600, "pure_no")["hash"],
            "no_vote": self.nodes[0].createproposal(self.nodes[0].getnewaddress(), 1, 3600, "no_vote")["hash"],
            "50_50_vote": self.nodes[0].createproposal(self.nodes[0].getnewaddress(), 1, 3600, "50_50_vote")["hash"],
        }
        self.slow_gen(1)

        # Verify the proposals are now in the proposals list with matching hashes
        desc_lst = []
        for proposal in self.nodes[0].listproposals():
            desc_lst.append(proposal['description'])
            assert (created_proposals[proposal['description']] == proposal['hash'])
        assert (set(desc_lst) == set(created_proposals.keys()))

        # Move to the end of the 0th voting cycle
        self.end_cycle()

        # Verify we are still in the 0th voting cycle for all the created proposals
        desc_lst = []
        for proposal in self.nodes[0].listproposals():
            desc_lst.append(proposal['description'])
            assert (proposal['votingCycle'] == 0)
        assert (set(desc_lst) == set(created_proposals.keys()))

        # Move to the 1st voting cycle
        self.slow_gen(1)

        # Verify we are in voting cycle 1 for all the created proposals
        desc_lst = []
        for proposal in self.nodes[0].listproposals():
            desc_lst.append(proposal['description'])
            assert (proposal['votingCycle'] == 1)
        assert (set(desc_lst) == set(created_proposals.keys()))

        # Vote for proposals and move to 50% of the voting cycle
        self.nodes[0].proposalvote(created_proposals["pure_yes"], "yes")
        self.nodes[0].proposalvote(created_proposals["pure_no"], "no")
        self.nodes[0].proposalvote(created_proposals["50_50_vote"], "yes")
        self.slow_gen(int(blocks_per_voting_cycle/2))

        # Vote for proposals and move to end of the 1st voting cycle
        self.nodes[0].proposalvote(created_proposals["50_50_vote"], "no")
        self.start_new_cycle()

        # Verify proposal status for all the created proposals
        desc_lst = []
        for proposal in self.nodes[0].listproposals():
            desc_lst.append(proposal['description'])
            if proposal['description'] == "pure_yes":
                assert (proposal['votingCycle'] == 1)
                assert (proposal['status'] == 'accepted')
                assert (proposal['state'] == 1)
            elif proposal['description'] == "pure_no":
                assert (proposal['votingCycle'] == 1)
                assert (proposal['status'] == 'rejected')
                assert (proposal['state'] == 2)
            elif proposal['description'] in ["50_50_vote", "no_vote"]:
                assert (proposal['votingCycle'] == 2)
                assert (proposal['status'] == 'pending')
                assert (proposal['state'] == 0)
            else:
                assert False
        assert (set(desc_lst) == set(created_proposals.keys()))

    def activate_cfund(self):
        self.slow_gen(100)
        # Verify the Community Fund is started
        assert (self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "started")

        self.slow_gen(100)
        # Verify the Community Fund is locked_in
        assert (self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "locked_in")

        self.slow_gen(100)
        # Verify the Community Fund is active
        assert (self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "active")

    def end_cycle(self):
        # Move to the end of the cycle
        self.slow_gen(self.nodes[0].cfundstats()["votingPeriod"]["ending"] - self.nodes[0].cfundstats()["votingPeriod"]["current"])

    def start_new_cycle(self):
        # Move one past the end of the cycle
        self.slow_gen(self.nodes[0].cfundstats()["votingPeriod"]["ending"] - self.nodes[0].cfundstats()["votingPeriod"]["current"] + 1)

    def slow_gen(self, count):
        total = count
        blocks = []
        while total > 0:
            now = min(total, 10)
            blocks.extend(self.nodes[0].generate(now))
            total -= now
            time.sleep(0.1)
        return blocks


if __name__ == '__main__':
    CommunityFundProposalsTest().main()

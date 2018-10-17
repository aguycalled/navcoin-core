#!/usr/bin/env python3
# Copyright (c) 2018 The Navcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import NavCoinTestFramework
from test_framework.util import *

import time

class CommunityFundProposalStateRawTXTest(NavCoinTestFramework):
    """Tests the state transition of proposals of the Community fund."""

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 1

    def setup_network(self, split=False):
        self.nodes = start_nodes(self.num_nodes, self.options.tmpdir)
        self.is_network_split = False

    def run_test(self):
        slow_gen(self.nodes[0], 100)
        # Verify the Community Fund is started
        assert(self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "started")

        slow_gen(self.nodes[0], 100)
        # Verify the Community Fund is locked_in
        assert(self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "locked_in")

        slow_gen(self.nodes[0], 100)
        # Verify the Community Fund is active
        assert(self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "active")

        proposalid0 = self.nodes[0].createproposal(self.nodes[0].getnewaddress(), 1, 3600, "test")["hash"]
        print(proposalid0)
        slow_gen(self.nodes[0], 100)

        self.start_new_cycle()

        time.sleep(0.2)

        #send a vote
        resultList = self.send_raw_propsal_vote_request(proposalid0)
        blocks = resultList[0]
        voteHash = resultList[1]

        decodedTx = self.get_transaction_from_block(blocks[0])

        assert (self.is_vote_hash_in_vout(decodedTx, voteHash))

        print(self.nodes[0].listproposals())



        for x in range(0, 580):
            self.send_raw_propsal_vote_request(proposalid0)



            print(self.nodes[0].listproposals())
            print(self.nodes[0].listproposals())

        # # Proposal initial state at beginning of cycle
        #
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 0)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "pending")
        #
        # # Vote enough yes votes, without enough quorum
        #
        # total_votes = self.nodes[0].cfundstats()["consensus"]["minSumVotesPerVotingCycle"]
        # min_yes_votes = self.nodes[0].cfundstats()["consensus"]["votesAcceptProposalPercentage"]/100
        # yes_votes = int(total_votes * min_yes_votes) + 1
        #
        # self.nodes[0].proposalvote(proposalid0, "yes")
        # self.slow_gen(yes_votes)
        # self.nodes[0].proposalvote(proposalid0, "no")
        # self.slow_gen(total_votes - yes_votes)
        # self.nodes[0].proposalvote(proposalid0, "remove")
        #
        # # Should still be in pending
        #
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 0)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "pending")
        #
        # self.start_new_cycle()
        # time.sleep(0.2)
        #
        # # Proposal initial state at beginning of cycle
        #
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 0)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "pending")
        #
        # # Vote enough quorum, but not enough positive votes
        # total_votes = self.nodes[0].cfundstats()["consensus"]["minSumVotesPerVotingCycle"] + 1
        # yes_votes = int(total_votes * min_yes_votes)
        #
        # self.nodes[0].proposalvote(proposalid0, "yes")
        # self.slow_gen(yes_votes)
        # self.nodes[0].proposalvote(proposalid0, "no")
        # self.slow_gen(total_votes - yes_votes)
        # self.nodes[0].proposalvote(proposalid0, "remove")
        #
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 0)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "pending")
        #
        # self.start_new_cycle()
        # time.sleep(0.2)
        #
        # # Proposal initial state at beginning of cycle
        #
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 0)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "pending")
        #
        # # Vote enough quorum and enough positive votes
        #
        # total_votes = self.nodes[0].cfundstats()["consensus"]["minSumVotesPerVotingCycle"] + 1
        # yes_votes = int(total_votes * min_yes_votes) + 1
        #
        # self.nodes[0].proposalvote(proposalid0, "yes")
        # self.slow_gen(yes_votes)
        # self.nodes[0].proposalvote(proposalid0, "no")
        # blocks = self.slow_gen(total_votes - yes_votes)
        # self.nodes[0].proposalvote(proposalid0, "remove")
        #
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 0)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "accepted waiting for end of voting period")
        #
        # time.sleep(0.2)
        #
        # # Revert last vote and check status
        #
        # self.nodes[0].invalidateblock(blocks[-1])
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 0)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "pending")
        # self.nodes[0].cfundstats()
        #
        # # Vote again
        #
        # self.nodes[0].proposalvote(proposalid0, "yes")
        # self.slow_gen(1)
        # self.nodes[0].proposalvote(proposalid0, "remove")
        #
        #
        # # Move to a new cycle...
        # time.sleep(0.2)
        #
        # self.start_new_cycle()
        # blocks=self.slow_gen(1)
        #
        # # Proposal must be accepted waiting for fund now
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 4)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "accepted waiting for enough coins in fund")
        #
        # # Check the available and locked funds
        # assert(self.nodes[0].cfundstats()["funds"]["available"] == self.nodes[0].cfundstats()["consensus"]["proposalMinimalFee"])
        # assert(self.nodes[0].cfundstats()["funds"]["locked"] == 0)
        #
        # # Donate to the fund
        # self.nodes[0].donatefund(1)
        # self.slow_gen(1)
        #
        # # Check the available and locked funds
        # assert (self.nodes[0].cfundstats()["funds"]["available"] == 1+self.nodes[0].cfundstats()["consensus"]["proposalMinimalFee"])
        # assert (self.nodes[0].cfundstats()["funds"]["locked"] == 0)
        #
        # # Move to the end of the cycle
        # self.start_new_cycle()
        #
        # # Validate that the proposal is accepted
        # assert(self.nodes[0].getproposal(proposalid0)["state"] == 1)
        # assert(self.nodes[0].getproposal(proposalid0)["status"] == "accepted")
        #
        # # Check the available and locked funds
        # assert (self.nodes[0].cfundstats()["funds"]["available"] == self.nodes[0].cfundstats()["consensus"]["proposalMinimalFee"])
        # assert (self.nodes[0].cfundstats()["funds"]["locked"] == 1)


    def get_transaction_from_block(self, blochHash):

        block = self.nodes[0].getblock(blochHash)

        tx = self.nodes[0].gettransaction(block['tx'][0])

        decodedTx = self.nodes[0].decoderawtransaction(tx['hex'])

        return decodedTx

    def is_vote_hash_in_vout(self, decodedTx, voteHash):

        vout = decodedTx['vout']

        isInVout = False
        for tx in vout:
            if tx['scriptPubKey']['hex'] == voteHash:
                isInVout = True

        return isInVout

    def send_raw_propsal_vote_request(self, hash):



        revHash = ""
        for x in range(-1, -len(hash), -2):
            revHash += hash[x-1] + hash[x]


        print(hash + " -> " + revHash)


        voteHash = "6ac1c2c4"+revHash

        print(voteHash)

        raw_vote_tx = self.nodes[0].createrawtransaction(
            [],
            {voteHash: 0},
            "", 0
        )


        d = self.nodes[0].coinbaseoutputs([raw_vote_tx])

        #print(d)

        blocks = slow_gen(self.nodes[0], 1)

        return [blocks, voteHash]


        # Modify version
        # raw_proposal_tx = "04" + raw_proposal_tx[2:]
        #
        # # Fund raw transaction
        # raw_proposal_tx = self.nodes[0].fundrawtransaction(raw_proposal_tx)['hex']
        #
        # # Sign raw transaction
        # raw_proposal_tx = self.nodes[0].signrawtransaction(raw_proposal_tx)['hex']

        # Send raw transaction
        #return self.nodes[0].sendrawtransaction(raw_proposal_tx)



    def start_new_cycle(self):
        # Move to the end of the cycle
        slow_gen(self.nodes[0], self.nodes[0].cfundstats()["votingPeriod"]["ending"] - self.nodes[0].cfundstats()["votingPeriod"]["current"])
        


if __name__ == '__main__':
    CommunityFundProposalStateRawTXTest().main()

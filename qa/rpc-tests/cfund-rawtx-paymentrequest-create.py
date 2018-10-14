#!/usr/bin/env python3
# Copyright (c) 2018 The Navcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import NavCoinTestFramework
from test_framework.util import *

import json


class CommunityFundCreatePaymentrequestRawTX(NavCoinTestFramework):
    """Tests the state transition of payment requests of the Community fund."""

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 1

    def setup_network(self, split=False):
        self.nodes = start_nodes(self.num_nodes, self.options.tmpdir)
        self.is_network_split = False

    def run_test(self):
        # Make sure cfund is active
        self.activate_cfund()

        # Donate to the cfund
        self.nodes[0].donatefund(100)

        # Get address
        address = self.nodes[0].getnewaddress()

        # Create a proposal
        proposalid0 = self.nodes[0].createproposal(address, 10, 3600, "test")["hash"]
        self.start_new_cycle()

        # Accept the proposal
        self.nodes[0].proposalvote(proposalid0, "yes")
        self.start_new_cycle()

        # Proposal should be accepted
        assert (self.nodes[0].getproposal(proposalid0)["state"] == 1)
        assert (self.nodes[0].getproposal(proposalid0)["status"] == "accepted")

        # Create a good payment request
        good_payreq_hash = self.send_raw_paymentrequest(1, address, proposalid0, "good_payreq")

        # Create payment request with negative amount
        try:
            self.send_raw_paymentrequest(-10, address, proposalid0, "negative_amount")
            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert("bad-cfund-payment-request" in e.error['message'])

        # Create payment request with amount too large
        try:
            self.send_raw_paymentrequest(1000, address, proposalid0, "too_large_amount")
            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert("bad-cfund-payment-request" in e.error['message'])

        # Create payment request with boolean description
        try:
            self.send_raw_paymentrequest(1, address, proposalid0, True)
            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert ("bad-cfund-payment-request" in e.error['message'])

#        # Create payment request with string amount
#        try:
#            self.send_raw_paymentrequest('1', address, proposalid0, 'string_amount')
#        except JSONRPCException as e:
#            assert ("bad-cfund-payment-request" in e.error['message'])

        # Generate block
        slow_gen(self.nodes[0], 1)

        # Check there exists only 1 good payment request
        assert (len(self.nodes[0].listproposals()[0]['paymentRequests']) == 1)

        self.start_new_cycle()

        # # Verify nothing changed
        assert (float(self.nodes[0].getproposal(proposalid0)["notPaidYet"]) == 10)
        assert (float(self.nodes[0].cfundstats()["funds"]["locked"]) == 10)

        # Accept payment request
        self.nodes[0].paymentrequestvote(good_payreq_hash, "yes")
        self.start_new_cycle()
        slow_gen(self.nodes[0], 10)

        # Check the payment request is paid out
        assert (float(self.nodes[0].getproposal(proposalid0)["notPaidYet"]) == 9)
        assert (float(self.nodes[0].cfundstats()["funds"]["locked"]) == 9)


        # Create multiple payment requests
        try:
            self.send_raw_paymentrequest(4, address, proposalid0, "sum_to_too_large_amount0")
            self.send_raw_paymentrequest(4, address, proposalid0, "sum_to_too_large_amount1")
            self.send_raw_paymentrequest(4, address, proposalid0, "sum_to_too_large_amount2")

            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert("bad-cfund-payment-request" in e.error['message'])


        # Create payment request to somebody else's address

        address_3rd_party = self.nodes[0].getnewaddress()
        try:
            self.send_raw_paymentrequest(1, address_3rd_party, proposalid0, "3rd_party_address")
            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert("bad-cfund-payment-request" in e.error['message'])


        # Create and test for expired and rejected proposals

        proposalid1_rejected = self.nodes[0].createproposal(address, 10, 3600, "test_rejected")["hash"]
        proposalid2_expired_timeout = self.nodes[0].createproposal(address, 10, 1, "test_expired_timeout")["hash"]
        proposalid3_expired_no_votes = self.nodes[0].createproposal(address, 10, 3600, "test_expired_no_votes")["hash"]
        self.start_new_cycle()

        # Reject Proposal 1 and accept Proposal 2
        self.nodes[0].proposalvote(proposalid1_rejected, "no")
        self.nodes[0].proposalvote(proposalid2_expired_timeout, "yes")
        self.start_new_cycle()

        # Proposal 1 should be rejected
        assert (self.nodes[0].getproposal(proposalid1_rejected)["state"] == 2)
        assert (self.nodes[0].getproposal(proposalid1_rejected)["status"] == "rejected")

        # Create a payment request for a rejected proposal
        try:
            self.send_raw_paymentrequest(1, address, proposalid1_rejected, "rejected_payreq")
            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert ("bad-cfund-payment-request" in e.error['message'])

        time.sleep(1)
        slow_gen(self.nodes[0], 10)

        # Proposal 2 should be expired
        assert (self.nodes[0].getproposal(proposalid2_expired_timeout)["status"] == "expired waiting for end of voting period")

        self.start_new_cycle()

        # Create a payment request for an expired proposal
        try:
            self.send_raw_paymentrequest(1, address, proposalid2_expired_timeout, "expired_payreq")
            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert ("bad-cfund-payment-request" in e.error['message'])

        # Let Proposal 3 expire
        self.start_new_cycle()
        self.start_new_cycle()
        self.start_new_cycle()

        # Proposal 3 should be expired
        assert (self.nodes[0].getproposal(proposalid3_expired_no_votes)["state"] == 3)
        assert (self.nodes[0].getproposal(proposalid3_expired_no_votes)["status"] == "expired")

        # Create a payment request for an expired proposal
        try:
            self.send_raw_paymentrequest(1, address, proposalid3_expired_no_votes, "expired_payreq")
            raise ValueError("Error should be thrown for invalid rawtx (prequest)")
        except JSONRPCException as e:
            assert ("bad-cfund-payment-request" in e.error['message'])


    def send_raw_paymentrequest(self, amount, address, proposal_hash, description):
        amount = amount * 100000000
        privkey = self.nodes[0].dumpprivkey(address)
        message = "I kindly ask to withdraw " + str(amount) + "NAV from the proposal " + proposal_hash + ". Payment request id: " + str(description)
        signature = self.nodes[0].signmessagewithprivkey(privkey, message)

        # Create a raw payment request
        raw_payreq_tx = self.nodes[0].createrawtransaction(
            [],
            {"6ac1": 1},
            json.dumps({"v": 2, "h": proposal_hash, "n": amount, "s": signature, "i": description})
        )

        # Modify version for payreq creation
        raw_payreq_tx = "05" + raw_payreq_tx[2:]

        # Fund raw transacion
        raw_payreq_tx = self.nodes[0].fundrawtransaction(raw_payreq_tx)['hex']

        # Sign raw transacion
        raw_payreq_tx = self.nodes[0].signrawtransaction(raw_payreq_tx)['hex']

        # Send raw transacion
        tx_hash = self.nodes[0].sendrawtransaction(raw_payreq_tx)

        return tx_hash

    def activate_cfund(self):
        slow_gen(self.nodes[0], 100)
        # Verify the Community Fund is started
        assert (self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "started")

        slow_gen(self.nodes[0], 100)
        # Verify the Community Fund is locked_in
        assert (self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "locked_in")

        slow_gen(self.nodes[0], 100)
        # Verify the Community Fund is active
        assert (self.nodes[0].getblockchaininfo()["bip9_softforks"]["communityfund"]["status"] == "active")

    def end_cycle(self):
        # Move to the end of the cycle
        slow_gen(self.nodes[0], self.nodes[0].cfundstats()["votingPeriod"]["ending"] - self.nodes[0].cfundstats()["votingPeriod"][
            "current"])

    def start_new_cycle(self):
        # Move one past the end of the cycle
        slow_gen(self.nodes[0], self.nodes[0].cfundstats()["votingPeriod"]["ending"] - self.nodes[0].cfundstats()["votingPeriod"][
            "current"] + 1)


if __name__ == '__main__':
    CommunityFundCreatePaymentrequestRawTX().main()

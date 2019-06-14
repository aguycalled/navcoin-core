#!/usr/bin/env python3
# Copyright (c) 2018 The Navcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import decimal
import sys
from test_framework.test_framework import NavCoinTestFramework
from test_framework.staticr_util import *

class ColdStakingSpending(NavCoinTestFramework):
    """Tests spending and staking to/from a spending wallet."""
    # set up num of nodes
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 4
    # set up nodes
    def setup_network(self, split=False):
        self.setup_nodes()
        connect_nodes(self.nodes[0], 1)
        connect_nodes(self.nodes[0], 2)
        connect_nodes(self.nodes[0], 3)
        self.is_network_split = False

    def run_test(self):

        # Turn off staking
        self.nodes[0].staking(False)
        self.nodes[1].staking(False)
        self.nodes[2].staking(False)
        self.nodes[3].staking(False)

        # Make it to the static rewards fork!
        activate_staticr(self.nodes[0])
        self.sync_all()

        # declare transaction-related constants
        BLOCK_REWARD = 50
        SPEND_AMOUNT = 100000
        RAW_FEE = 0.001

        # Get spending key from node 1
        spending_address_public_key = self.nodes[1].getnewaddress()
        spending_address_private_key = self.nodes[1].dumpprivkey(spending_address_public_key)

        # Get the staking key from node 2
        staking_address_public_key = self.nodes[2].getnewaddress()
        staking_address_private_key = self.nodes[2].dumpprivkey(staking_address_public_key)

        # Import both keys to node 3
        self.nodes[3].importprivkey(spending_address_private_key)
        # self.nodes[3].importprivkey(staking_address_private_key)

        # generate coldstaking address
        coldstaking_address = self.nodes[0].getcoldstakingaddress(staking_address_public_key, spending_address_public_key)

        """check wallet balance and staking weight"""

        # get wallet balance 
        balance_before_send = self.nodes[0].getbalance()
    
        # Send funds to the cold staking address
        coldstaing_txid = self.nodes[0].sendtoaddress(coldstaking_address, self.nodes[0].getbalance(), "", "", "", True)
        self.nodes[0].generate(1)
        self.sync_all()

        # Check the funds arrived at node 1
        node_1_received = [n for n in self.nodes[1].listunspent(0) if n["address"] == coldstaking_address]
        assert(len(node_1_received) == 1)
        assert_equal(coldstaing_txid, node_1_received[0]["txid"])
        assert(node_1_received[0]["confirmations"] == 1)

        # Check balances are correct on each node (balance should have moved to nodes 1 and 3)
        assert_equal(self.nodes[0].getbalance(), BLOCK_REWARD)
        assert(balance_before_send - 1 <= self.nodes[1].getbalance() <= balance_before_send)
        assert_equal(self.nodes[2].getbalance(), 0)
        assert(balance_before_send - 1 <= self.nodes[3].getbalance() <= balance_before_send)

        """test spending from wallet with only the spending key"""

        balance_before_send_spending = self.nodes[1].getbalance()
        node_0_address_spending = self.nodes[0].getnewaddress()
        spending_txid = self.nodes[1].sendtoaddress(node_0_address_spending, SPEND_AMOUNT)

        self.nodes[1].generate(1)
        self.sync_all()

        # Check the funds arrived at node 0
        node_0_received = [n for n in self.nodes[0].listunspent(0) if n["address"] == node_0_address_spending]
        assert(len(node_0_received) == 1)
        assert_equal(spending_txid, node_0_received[0]["txid"])
        assert(node_0_received[0]["confirmations"] == 1)
        assert(node_0_received[0]["amount"] == SPEND_AMOUNT)

        # Send all remaining coins back to the cold staking address
        self.nodes[1].sendtoaddress(coldstaking_address, self.nodes[1].getbalance(), "", "", "", True)
        self.nodes[1].generate(1)
        self.sync_all()

        # Check the coldstaking balance is correct
        assert(balance_before_send_spending - SPEND_AMOUNT - 1 <= self.nodes[1].getbalance() <= balance_before_send_spending - SPEND_AMOUNT)
        assert_equal(self.nodes[1].getbalance(), self.nodes[3].getbalance())

        """test spending from wallet with only the staking key"""

        node_0_address_staking = self.nodes[0].getnewaddress()
        
        try:
            staking_txid = self.nodes[2].sendtoaddress(node_0_address_staking, SPEND_AMOUNT)
            staking_sent = True
        except Exception as e:
            staking_sent = False
            print("Sending from Staking Failed: ", e)

        # Check the funds arrived at node 0
        node_0_received = [n for n in self.nodes[0].listunspent(0) if n["address"] == node_0_address_staking]
        assert(len(node_0_received) == 0)

        # Confirm spending from node 2 failed
        assert(staking_sent == False)
        
        """test spending from wallet with both the staking and spending keys"""

        balance_before_send_both = self.nodes[3].getbalance()
        node_0_address_both = self.nodes[0].getnewaddress()
        
        both_txid = self.nodes[3].sendtoaddress(node_0_address_both, SPEND_AMOUNT)
    
        self.nodes[3].generate(1)
        self.sync_all()

        # Check the funds arrived at node 0
        node_0_received = [n for n in self.nodes[0].listunspent(0) if n["address"] == node_0_address_both]
        assert(len(node_0_received) == 1)
        assert_equal(both_txid, node_0_received[0]["txid"])
        assert(node_0_received[0]["confirmations"] == 1)
        assert(node_0_received[0]["amount"] == SPEND_AMOUNT)

        # Send all remaining coins back to the cold staking address
        self.nodes[3].sendtoaddress(coldstaking_address, self.nodes[3].getbalance(), "", "", "", True)
        self.nodes[3].generate(1)
        self.sync_all()

        # Check the coldstaking balance is correct
        assert(balance_before_send_both - SPEND_AMOUNT - 1 <= self.nodes[1].getbalance() <= balance_before_send_both - SPEND_AMOUNT)
        assert_equal(self.nodes[1].getbalance(), self.nodes[3].getbalance())

        """send raw tx from wallet with spending key"""

        balance_before_send_raw_spending = self.nodes[1].getbalance()
        node_0_address_raw_spending = self.nodes[0].getnewaddress()
        spending_unspent = [n for n in self.nodes[1].listunspent(0) if n["address"] == coldstaking_address]

        change_amount_spending = float(decimal.Decimal(spending_unspent[0]["amount"]) - decimal.Decimal(SPEND_AMOUNT) - decimal.Decimal(RAW_FEE))

        inputs = [{ "txid" : spending_unspent[0]["txid"], "vout" : spending_unspent[0]["vout"]}]
        outputs = {node_0_address_raw_spending : SPEND_AMOUNT, coldstaking_address: change_amount_spending}
        rawtx = self.nodes[1].createrawtransaction(inputs, outputs)
        signresult = self.nodes[1].signrawtransaction(rawtx)
        assert(signresult["complete"])

        spending_raw_txid = self.nodes[1].sendrawtransaction(signresult['hex'])

        self.nodes[1].generate(1)
        self.sync_all()

        # Check the funds arrived at node 0
        node_0_received = [n for n in self.nodes[0].listunspent(0) if n["address"] == node_0_address_raw_spending]
        assert(len(node_0_received) == 1)
        assert_equal(spending_raw_txid, node_0_received[0]["txid"])
        assert(node_0_received[0]["confirmations"] == 1)
        assert(node_0_received[0]["amount"] == SPEND_AMOUNT)

        # Check the change remains in the cold staking address
        assert_equal(float(self.nodes[1].getbalance()), change_amount_spending)
        assert_equal(float(self.nodes[3].getbalance()), change_amount_spending)

        """send raw tx from wallet with both keys"""

        balance_before_send_raw_both = self.nodes[3].getbalance()
        node_0_address_raw_both = self.nodes[0].getnewaddress()
        both_unspent = [n for n in self.nodes[1].listunspent(0) if n["address"] == coldstaking_address]

        change_amount_both = float(decimal.Decimal(balance_before_send_raw_both) - decimal.Decimal(SPEND_AMOUNT) - decimal.Decimal(RAW_FEE))

        inputs = [{ "txid" : both_unspent[0]["txid"], "vout" : both_unspent[0]["vout"]}]
        outputs = {node_0_address_raw_both : SPEND_AMOUNT, coldstaking_address: change_amount_both}
        rawtx = self.nodes[3].createrawtransaction(inputs, outputs)
        signresult = self.nodes[3].signrawtransaction(rawtx)
        assert(signresult["complete"])

        both_raw_txid = self.nodes[3].sendrawtransaction(signresult['hex'])

        self.nodes[3].generate(1)
        self.sync_all()

        # Check the funds arrived at node 0
        node_0_received = [n for n in self.nodes[0].listunspent(0) if n["address"] == node_0_address_raw_both]
        assert(len(node_0_received) == 1)
        assert_equal(both_raw_txid, node_0_received[0]["txid"])
        assert(node_0_received[0]["confirmations"] == 1)
        assert(node_0_received[0]["amount"] == SPEND_AMOUNT)
        
        # Check the change remains in the cold staking address
        assert_equal(float(self.nodes[1].getbalance()), float(change_amount_both + BLOCK_REWARD))
        assert_equal(float(self.nodes[3].getbalance()), change_amount_both)

        """try to send raw tx from wallet with only the staking key"""

        balance_before_send_raw_staking = self.nodes[1].getbalance()
        node_0_address_raw_staking = self.nodes[0].getnewaddress()
        staking_unspent = [n for n in self.nodes[1].listunspent(0) if n["address"] == coldstaking_address]

        change_amount_staking = float(decimal.Decimal(staking_unspent[0]["amount"]) - decimal.Decimal(SPEND_AMOUNT) - decimal.Decimal(RAW_FEE))

        inputs = [{ "txid" : staking_unspent[0]["txid"], "vout" : staking_unspent[0]["vout"]}]
        outputs = {node_0_address_raw_staking : SPEND_AMOUNT, coldstaking_address: change_amount_staking}
        
        try:
            rawtx = self.nodes[2].createrawtransaction(inputs, outputs)
            signresult = self.nodes[2].signrawtransaction(rawtx)
            both_raw_txid = self.nodes[2].sendrawtransaction(signresult['hex'])
            staking_raw_sent = True
        except Exception as e:
            staking_raw_sent = False
            print("Sending from Staking Raw Failed: ", e)
        
        # Check the funds arrived at node 0
        node_0_received = [n for n in self.nodes[0].listunspent(0) if n["address"] == node_0_address_raw_staking]
        assert(len(node_0_received) == 0)

        # Confirm spending from node 2 failed
        assert(staking_sent == False)
        assert(self.nodes[1].getbalance() == balance_before_send_raw_staking)

if __name__ == '__main__':
    ColdStakingSpending().main()

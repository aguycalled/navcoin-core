#!/usr/bin/env python3
# Copyright (c) 2014-2015 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Test timestampindex generation and fetching
#

import time

from test_framework.test_framework import NavCoinTestFramework
from test_framework.util import *


class TimestampIndexTest(NavCoinTestFramework):

    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 4
        self.extra_args = [["-debug"], ["-debug", "-timestampindex"], ["-debug"], ["-debug", "-timestampindex"]]

    def setup_network(self):
        self.setup_nodes()
        connect_nodes(self.nodes[0], 1)
        connect_nodes(self.nodes[0], 2)
        connect_nodes(self.nodes[0], 3)

        self.is_network_split = False
        self.sync_all()

    def run_test(self):
        print("Mining 25 blocks...")
        blockhashes = slow_gen(self.nodes[0], 25)
        print("Mining 25 blocks...")
        blockhashes.extend(slow_gen(self.nodes[0], 25))
        print("Mining 25 blocks...")
        blockhashes.extend(slow_gen(self.nodes[0], 25))
        self.sync_all()
        low = self.nodes[1].getblock(blockhashes[0])["time"]
        high = low + 76

        print("Checking timestamp index...")
        hashes = self.nodes[1].getblockhashes(high, low)

        assert_equal(len(hashes), len(blockhashes))

        assert_equal(hashes, blockhashes)

        print("Passed\n")


if __name__ == '__main__':
    TimestampIndexTest().main()

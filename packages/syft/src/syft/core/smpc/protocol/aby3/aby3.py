"""ABY3 Protocol.

ABY3 : A Mixed Protocol Framework for Machine Learning.
https://eprint.iacr.org/2018/403.pdf
"""
# stdlib
from functools import reduce
from typing import Any
from typing import List

# relative
from ....tensor.smpc.mpc_tensor import MPCTensor
from ....tensor.smpc.utils import get_nr_bits


class ABY3:
    """ABY3 Protocol Implementation."""

    def __eq__(self, other: Any) -> bool:
        """Check if "self" is equal with another object given a set of attributes to compare.

        Args:
            other (Any): Object to compare

        Returns:
            bool: True if equal False if not.
        """
        if type(self) != type(other):
            return False

        return True

    @staticmethod
    def bit_injection(x: MPCTensor, ring_size: int) -> MPCTensor:
        """Perform ABY3 bit injection for conversion of binary share to arithmetic share.

        Args:
            x (MPCTensor) : MPCTensor with shares of bit.
            ring_size (int) : Ring size of arithmetic share to convert.

        Returns:
            arith_share (MPCTensor): Arithmetic shares of bit in input ring size.

        Raises:
            ValueError: If input tensor is not binary shared.
            ValueError: If the exactly three parties are not involved in the computation.
        """
        shape = x.shape
        parties = x.parties
        nr_parties = len(parties)
        ring_size = 2 ** 32  # TODO: Should extract from global context for general case

        decomposed_shares = [
            share.bit_decomposition(share, ring_size, False) for share in x.child
        ]
        # List which contains the share of a single bit
        res_shares: List[MPCTensor] = []

        bit_shares = list(map(lambda x: x.get_tensor_list(0)), decomposed_shares)  # type: ignore
        bit_shares = list(map(lambda x: [x[i] for i in range(nr_parties)], bit_shares))
        bit_shares = zip(bit_shares)  # type: ignore
        for bit_sh in bit_shares:
            mpc = MPCTensor(shares=bit_sh, shape=shape, parties=parties)
            res_shares.append(mpc)

        arith_share = reduce(lambda x, y: x + y - (x * y * 2), res_shares)

        return arith_share

    @staticmethod
    def full_adder(a: List[MPCTensor], b: List[MPCTensor]) -> List[MPCTensor]:
        """Perform bit addition on MPCTensors using a full adder.

        Args:
            a (List[MPCTensor]): MPCTensor with shares of bit.
            b (List[MPCTensor]): MPCTensor with shares of bit.

        Returns:
            result (List[MPCTensor]): Result of the operation.

        TODO: Should modify ripple carry adder to parallel prefix adder.
        """
        ring_size = 2 ** 32
        ring_bits = get_nr_bits(ring_size)
        c = 0  # carry bits of addition.
        result: List[MPCTensor] = []
        for idx in range(ring_bits):
            s = a[idx] + b[idx] + c
            c = a[idx] * b[idx] + c * (a[idx] + b[idx])
            result.append(s)
        return result

    @staticmethod
    def bit_decomposition(x: MPCTensor) -> List[MPCTensor]:
        """Perform ABY3 bit decomposition for conversion of arithmetic share to binary share.

        Args:
            x (MPCTensor): Arithmetic shares of secret.

        Returns:
            bin_share (List[MPCTensor]): Returns binary shares of each bit of the secret.

        TODO : Should be modified to use parallel prefix adder when multiprocessing
        functionality is integrated
        """
        nr_parties = len(x.parties)
        ring_size = 2 ** 32  # Should extract this info better
        ring_bits = get_nr_bits(ring_size)
        shape = x.shape
        parties = x.parties
        # List which contains the share of each share.
        res_shares: List[List[MPCTensor]] = [[] for _ in range(nr_parties)]

        decomposed_shares = [
            share.bit_decomposition(share, 2, True) for share in x.child
        ]

        for idx in range(ring_bits):
            bit_shares = list(map(lambda x: x.get_tensor_list(idx), decomposed_shares))
            bit_shares = list(
                map(lambda x: [x[i] for i in range(nr_parties)], bit_shares)
            )
            bit_shares = zip(bit_shares)  # type: ignore
            for i, bit_sh in enumerate(bit_shares):
                mpc = MPCTensor(shares=bit_sh, shape=shape, parties=parties)
                res_shares[i].append(mpc)

        bin_share = reduce(ABY3.full_adder, res_shares)

        return bin_share

# MIT License

# Copyright (c) 2020 Baking Bad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Union

import base58

def tb(l):
    return b''.join(map(lambda x: x.to_bytes(1, 'big'), l))

base58_encodings = [
    #    Encoded   |               Decoded             |
    # prefix | len | prefix                      | len | Data type
    (b"B", 51, tb([1, 52]), 32, "block hash"),
    (b"o", 51, tb([5, 116]), 32, "operation hash"),
    (b"Lo", 52, tb([133, 233]), 32, "operation list hash"),
    (b"LLo", 53, tb([29, 159, 109]), 32, "operation list list hash"),
    (b"P", 51, tb([2, 170]), 32, "protocol hash"),
    (b"Co", 52, tb([79, 199]), 32, "context hash"),
    (b"tz1", 36, tb([6, 161, 159]), 20, "ed25519 public key hash"),
    (b"tz2", 36, tb([6, 161, 161]), 20, "secp256k1 public key hash"),
    (b"tz3", 36, tb([6, 161, 164]), 20, "p256 public key hash"),
    (b"KT1", 36, tb([2, 90, 121]), 20, "originated address"),
    # FIXME: replace with tb()
    (b"txr1", 37, b'\x01\x80x\x1f', 20, "tx_rollup_l2_address"),
    (b"id", 30, tb([153, 103]), 16, "cryptobox public key hash"),
    (b'expr', 54, tb([13, 44, 64, 27]), 32, u'script expression'),
    (b"edsk", 54, tb([13, 15, 58, 7]), 32, "ed25519 seed"),
    (b"edpk", 54, tb([13, 15, 37, 217]), 32, "ed25519 public key"),
    (b"spsk", 54, tb([17, 162, 224, 201]), 32, "secp256k1 secret key"),
    (b"p2sk", 54, tb([16, 81, 238, 189]), 32, "p256 secret key"),
    (b"edesk", 88, tb([7, 90, 60, 179, 41]), 56, "ed25519 encrypted seed"),
    (b"spesk", 88, tb([9, 237, 241, 174, 150]), 56, "secp256k1 encrypted secret key"),
    (b"p2esk", 88, tb([9, 48, 57, 115, 171]), 56, "p256_encrypted_secret_key"),
    (b"sppk", 55, tb([3, 254, 226, 86]), 33, "secp256k1 public key"),
    (b"p2pk", 55, tb([3, 178, 139, 127]), 33, "p256 public key"),
    (b"SSp", 53, tb([38, 248, 136]), 33, "secp256k1 scalar"),
    (b"GSp", 53, tb([5, 92, 0]), 33, "secp256k1 element"),
    (b"edsk", 98, tb([43, 246, 78, 7]), 64, "ed25519 secret key"),
    (b"edsig", 99, tb([9, 245, 205, 134, 18]), 64, "ed25519 signature"),
    (b"spsig", 99, tb([13, 115, 101, 19, 63]), 64, "secp256k1 signature"),
    (b"p2sig", 98, tb([54, 240, 44, 52]), 64, "p256 signature"),
    (b"sig", 96, tb([4, 130, 43]), 64, "generic signature"),
    (b'Net', 15, tb([87, 82, 0]), 4, "chain id"),
    (b'nce', 53, tb([69, 220, 169]), 32, 'seed nonce hash'),
    (b'btz1', 37, tb([1, 2, 49, 223]), 20, 'blinded public key hash'),
    (b'vh', 52, tb([1, 106, 242]), 32, 'block_payload_hash'),
]


def scrub_input(v: Union[str, bytes]) -> bytes:
    if isinstance(v, bytes):
        pass
    elif isinstance(v, str):
        try:
            _ = int(v, 16)
        except ValueError:
            v = v.encode('ascii')
        else:
            if v.startswith('0x'):
                v = v[2:]
            v = bytes.fromhex(v)
    else:
        raise TypeError("a bytes-like object is required (also str), not '%s'" % type(v).__name__)
    return v

def base58_decode(v: bytes) -> bytes:
    """Decode data using Base58 with checksum + validate binary prefix against known kinds and cut in the end.

    :param v: Array of bytes (use string.encode())
    :returns: bytes
    """
    try:
        prefix_len = next(
            len(encoding[2]) for encoding in base58_encodings if len(v) == encoding[1] and v.startswith(encoding[0])
        )
    except StopIteration as e:
        raise ValueError('Invalid encoding, prefix or length mismatch.') from e

    return base58.b58decode_check(v)[prefix_len:]

def _validate(v: Union[str, bytes], prefixes: list):
    if isinstance(v, str):
        v = v.encode()
    v = scrub_input(v)
    if any(map(v.startswith, prefixes)):
        base58_decode(v)
    else:
        raise ValueError('Unknown prefix.')

def validate_pkh(v: Union[str, bytes]):
    """Ensure parameter is a public key hash (starts with b'tz1', b'tz2', b'tz3')

    :param v: string or bytes
    :raises ValueError: if parameter is not a public key hash
    """
    return _validate(v, prefixes=[b'tz1', b'tz2', b'tz3'])

def is_pkh(v: Union[str, bytes]) -> bool:
    """Check if value is a public key hash."""
    try:
        validate_pkh(v)
    except (ValueError, TypeError):
        return False
    return True

def is_kt(v: Union[str, bytes]) -> bool:
    """Check if value is a KT address."""
    try:
        _validate(v, prefixes=[b'KT1'])
    except (ValueError, TypeError):
        return False
    return True

def is_address(v: Union[str, bytes]) -> bool:
    """Check if value is a tz/KT address"""
    if isinstance(v, bytes):
        v = v.decode()
    address = v.split('%')[0]
    return is_kt(address) or is_pkh(address)
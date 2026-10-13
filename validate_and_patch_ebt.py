#!/usr/bin/env python3
"""Generate the hardware-tested D625 EBT v2 patch offline. No USB operations."""
import argparse
import hashlib
from pathlib import Path

ORIGINAL_SHA256 = '10bc066b7f99256f87b05e82b5087c5c6f815a3e865dc094169176fcc69706f7'
PATCHED_SHA256 = 'c2c787a409ef6fd3ea01f9225dca4f40d81cf5164de631f9bb067bf4ff43541b'
IMAGE_SIZE = 860160
PATCHES = (
    (0xec5e, bytes.fromhex('88b1'), bytes.fromhex('11e0')),
    (0x125e4, bytes.fromhex('1bd0'), bytes.fromhex('1be0')),
)


def validate_and_patch(original: bytes) -> bytes:
    if len(original) != IMAGE_SIZE or hashlib.sha256(original).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('Input is not the verified live D625 bootloader; refusing to patch')
    candidate = bytearray(original)
    for offset, expected, replacement in PATCHES:
        if original[offset:offset + len(expected)] != expected:
            raise ValueError(f'Unexpected instruction at {offset:#x}')
        candidate[offset:offset + len(replacement)] = replacement
    candidate = bytes(candidate)
    if hashlib.sha256(candidate).hexdigest() != PATCHED_SHA256:
        raise ValueError('Output SHA256 mismatch; refusing to write')
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Use separate input and output files to preserve the original')
    try:
        candidate = validate_and_patch(args.input.read_bytes())
        with args.output.open('xb') as stream:
            stream.write(candidate)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
    print(f'Original SHA256: {ORIGINAL_SHA256}')
    print(f'Patched SHA256:  {PATCHED_SHA256}')
    print(f'Wrote {args.output} ({len(candidate)} bytes; 3 changed bytes)')


if __name__ == '__main__':
    main()

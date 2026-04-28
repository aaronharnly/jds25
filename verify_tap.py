"""Parse and verify a ZX Spectrum .tap file. Prints the block table and checksum status."""
import sys, struct, os

def parse(tap_path):
    data = open(tap_path, "rb").read()
    pos = 0
    n = 0
    while pos < len(data):
        if pos + 2 > len(data):
            print(f"ERROR: truncated at byte {pos}")
            return
        block_len = struct.unpack("<H", data[pos:pos+2])[0]
        pos += 2
        if pos + block_len > len(data):
            print(f"ERROR: block {n} declares {block_len} bytes but only {len(data)-pos} remain")
            return
        block = data[pos:pos+block_len]
        pos += block_len

        flag = block[0]
        payload = block[1:-1]
        chk = block[-1]
        # XOR checksum across flag+payload
        calc = 0
        for b in block[:-1]:
            calc ^= b
        ok = "OK" if calc == chk else f"BAD (expected {chk:02X}, got {calc:02X})"

        if flag == 0x00 and len(payload) == 17:
            ftype = payload[0]
            fname = payload[1:11].decode('ascii', errors='replace').rstrip()
            data_len = struct.unpack("<H", payload[11:13])[0]
            p1 = struct.unpack("<H", payload[13:15])[0]
            p2 = struct.unpack("<H", payload[15:17])[0]
            type_name = {0:"BASIC", 1:"NUM ARRAY", 2:"CHR ARRAY", 3:"CODE"}.get(ftype, f"?{ftype}")
            extra = ""
            if ftype == 0:
                extra = f" autostart_line={p1} prog_len={p2}"
            elif ftype == 3:
                extra = f" load_addr={p1} (=0x{p1:04X})"
            print(f"[{n}] HEADER  type={type_name:10s} name='{fname}'  data_len={data_len:5d}{extra}  chk={ok}")
        else:
            kind = "DATA  " if flag == 0xFF else f"FLG{flag:02X}"
            print(f"[{n}] {kind}  bytes={len(payload):5d}  chk={ok}")
        n += 1
    print(f"\nTotal: {n} blocks, {len(data)} bytes.")

if __name__ == "__main__":
    parse(sys.argv[1] if len(sys.argv) > 1 else "card.tap")

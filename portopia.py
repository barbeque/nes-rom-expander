import sys

def inject_header(target_bytes, new_header):
    padded_header = [ 0 ] * 16
    for i in range(0, len(new_header)):
        padded_header[i] = new_header[i]

    assert(len(padded_header) == 16), "Header must be 16 bytes long"
    return bytearray(padded_header) + bytearray(target_bytes)

def copy_source(source_bytes, target_bytes, copy_from, copy_to):
    # will continue to copy bytes until it hits the end of the buf
    # sort of a hack, who cares
    for i in range(0, len(source_bytes) - copy_from):
        target_bytes[copy_to + i] = source_bytes[copy_from + i]
    return target_bytes

if len(sys.argv) < 2:
    print('Usage: {} [ROM to expand]', sys.argv[0])
    sys.exit(1)

with open(sys.argv[1]) as f:
    bytes = bytearray(f.read())

print('ROM length = %d' % len(bytes))

# detect iNES header (16 bytes)
if(bytes[0] == ord('N') and bytes[1] == ord('E') and bytes[2] == ord('S') and bytes[3] == 0x1a):
    print('iNES header detected')
    bytes = bytes[16:]
    print('ROM length after header removal = %d' % len(bytes))

# produce target bytes
target_bytes = [0] * 0x12000 # from SIZE directive


# TODO: parse & follow ROM Expander Pro instructions (hardcoded for now)
target_bytes = copy_source(bytes, target_bytes, 0x0, 0x0)
target_bytes = copy_source(bytes, target_bytes, 0x0, 0x4000)
target_bytes = copy_source(bytes, target_bytes, 0x0, 0x8000)
target_bytes = inject_header(target_bytes, [0x4E, 0x45, 0x53, 0x1A, 0x04, 0x01, 0x40, 0x40])

# interpret the SIZE directive
assert(len(target_bytes) == (0x12000 + 16)), ("ROM (%d bytes) isn't the length I expected after patching!" % len(target_bytes))

print('Expanded.')
assert(target_bytes[0] == 0x4e), "Must be an iNES header"

with open('The Portopia Serial Murder Case.nes', 'wb') as o:
    o.write(target_bytes)

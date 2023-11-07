
def bits_para_hex(bit_string): #transforma bit em hex
            hex_string = ''
            for i in range(0, len(bit_string), 4):
                nibble = bit_string[i:i+4]
                nibble_hex = hex(int(nibble, 2))[2:]
                hex_string += nibble_hex
            return hex_string



def create_matriz(message): #mensagem e senha para 4x4
    matriz = [[0 for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            matriz[i][j] = message[0:8]
            message = message[8:]
    return matriz

def shift_rows(state): 
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state

def sub_bytes(state, s_box):
    for i in range(4):
        for j in range(4):
            byte = state[i][j]
            row = int(byte[:4], 2)
            col = int(byte[4:], 2)
            substituted_byte = s_box[row * 16 + col]
            state[i][j] = f'{substituted_byte:08b}'

    return state

def mix_columns(state): # funcao que mistura as colunas
    mix_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]


    for j in range(4):
        column = [int(state[i][j], 2) for i in range(4)]
        mixed_column = mix_column(column)
        for i in range(4):
            state[i][j] = format(mixed_column[i], '08b') 

    return state

def mix_column(column):
    mixed_column = []
    for i in range(4):
        mixed_column.append(galois_multiply(column[0], 0x02) ^
                            galois_multiply(column[1], 0x03) ^
                            galois_multiply(column[2], 0x01) ^
                            galois_multiply(column[3], 0x01))
        column = column[1:] + [column[0]]  

    return mixed_column



def galois_multiply(a, b): # mutiplicacao Galois
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80  
        a = (a << 1) & 0xFF
        if carry:
            a ^= 0x1B  
        b >>= 1

    return p



def key_expansion(key, s_box): #funcao das subchaves de expancao
    round_constants = ['00000001', 
                        '00000010', 
                        '00000100', 
                        '00001000', 
                        '00010000', 
                        '00100000', 
                        '01000000', 
                        '10000000', 
                        '00011011', 
                        '00110110']
    expanded_key = [key]
    for i in range(10):
        prev_key = expanded_key[-1]
        new_key = []
        temp = prev_key[1:] + [prev_key[0]]
        new_key = sub_bytes(temp, s_box)
        round_constant = round_constants[i]
        new_key[0][0] = format(int(new_key[0][0], 2) ^ int(round_constant, 2), '08b')
        for i in range(4):
            for j in range(4):
                new_key[i][j] = format(int(new_key[i][j], 2) ^ int(prev_key[i][j], 2), '08b')
        expanded_key.append(new_key)
    return expanded_key


def add_round_key(state, key): # funcao da chave de rodada
    for i in range(4):
        for j in range(4):
            state[i][j] = format(int(state[i][j], 2) ^ int(key[i][j], 2), '08b')

    return state

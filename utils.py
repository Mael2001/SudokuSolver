def intToHex(i):
    if i < 10:
        return str(i)
    if i == 10: return 'A'
    if i == 11: return 'B'
    if i == 12: return 'C'
    if i == 13: return 'D'
    if i == 14: return 'E'
    if i == 15: return 'F'
    if i == 16: return 'X'

def hexToInt(i):
    if i in '1234567890':
        return int(i)
    if i == 'A': return 10
    if i == 'B': return 11
    if i == 'C': return 12
    if i == 'D': return 13
    if i == 'E': return 14
    if i == 'F': return 15
    if i == 'X': return 16

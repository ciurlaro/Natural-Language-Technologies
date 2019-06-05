import sys


#
#
#
def letter_to_int(letter):
    alphabet = list('abcdefghijklmnopqrstuvwxyz \'0123456789')
    return alphabet.index(letter.lower()) + 1


#
# 
def map_2_hundred(accumulator):
    if accumulator < 1:
        a = "1-100"
        print('annotazione coppie 1-100 del file iurlaro_output.txt')
    elif accumulator < 2:
        a = "101-200"
        print('annotazione coppie 101-200 del file iurlaro_output.txt')
    elif accumulator < 3:
        a = "201-300"
        print('annotazione coppie 201-300 del file iurlaro_output.txt')
    elif accumulator < 4:
        a = "301-400"
        print('annotazione coppie 301-400 del file iurlaro_output.txt')
    else:  # 4
        a = "401-500"
        print('annotazione coppie 401-500 del file iurlaro_output.txt')
    return a


#
# 
# 
# ================================================================
#  Mappa un cognome su uno dei 5 insiemi di coppie da annotare
# ================================================================


def cognome() -> str:
    if len(sys.argv) < 2:
        input_name = input("Inserimento cognome (senza spazi): ")
    elif len(sys.argv) == 2:
        input_name = sys.argv[1]
    else:
        print('\n\n\nUSAGE to run the program\n',
              '\npython script_name your_surname\npython script_name\n\n')
        sys.exit(1)

    accumulator = 0
    for i, c in enumerate(input_name):
        accumulator += letter_to_int(c)

    return map_2_hundred(accumulator % 5)

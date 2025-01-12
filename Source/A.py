"""
Removes the non alphabetic characters.
Capital letters to small letters.
"""
def clean_text(text):
    return ''.join(char.lower() for char in text if char.isalpha())

"""
This returns an ordering of which key length is most likely to be it.
We don't rule out any key.
"""
KasiskyThresh = 4
def kasisky(text):
    freq = []
    n = len(text)
    for i in range(6):
        freq.append([0, i])
    seq_dict = {}
    for j in range(3, 7):
        for i in range(n - j + 1):
            res = text[i:i + j]
            if res in seq_dict:
                seq_dict[res].append(i)
            else:
                seq_dict[res] = [i]
    for v in seq_dict:
        if(len(seq_dict[v]) >= KasiskyThresh):
            for i in range(1, len(seq_dict[v])):
                d = seq_dict[v][i] - seq_dict[v][i - 1]
                for k in range(1, 6):
                    if(d % k == 0):
                        freq[k][0] += 1
    # print(freq)
    freq.sort()
    freq.reverse()
    L = []
    for k in freq:
        if(k[1] != 0):
            L.append(k[1])
    # print(L)
    return L

"""
Given a text it just computes ic for it.
"""
def compute_ic(text):
    n = len(text)
    frequency = [0] * 26
    for char in text:
        frequency[ord(char) - ord('a')] += 1
    ic = 0.0
    for f in frequency:
        ic += f * (f - 1)
    ic /= n * (n - 1) 
    return ic

"""
Given a key length , it divides the texts into various groups and computes average ic for it.
"""
def average_ic(text, keyword_length):
    # The text is assumed to be cleaned.
    groups = ['' for _ in range(keyword_length)]
    n = len(text)
    for i in range(n):
        char = text[i]
        groups[i % keyword_length] += char
    ic_sum = 0.0
    for group in groups:
        ic_sum += compute_ic(group)
    average_ic = ic_sum / keyword_length
    return average_ic

"""
This function , goes over the possible keys we get from kasisky and computes ic from them.
It then further refines the possible keys by taking the one whose ic is close to english_ic.
"""
def ic(text):
    english_ic = 0.068
    L = []
    Order = kasisky(text)
    for i in Order:
        X = [average_ic(text, i), i]
        X[0] = abs(X[0] - english_ic)
        L.append(X)
    L.sort()
    LX = []
    for X in L:
        LX.append(X[1])
    return LX

"""
English frequency distribution
"""
g = [
    
    0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002,
    0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091,
    0.028, 0.010, 0.023, 0.001, 0.020, 0.001
]
abc = "abcdefghijklmnopqrstuvwxyz"

"""
Given a key_word length it will find the actual key 
"""
def mutual_ic(text, keyword_length):
    groups = ['' for _ in range(keyword_length)]
    n = len(text)
    for i in range(n):
        char = text[i]
        groups[i % keyword_length] += char
    shifts = [0] * keyword_length
    for j in range(keyword_length):
        group = groups[j]
        frequency = [0] * 26
        for char in group:
            frequency[ord(char) - ord('a')] += 1
        mx = 0.0
        for shift in range(26):
            dot_prod = 0.0
            for i in range(26):
                dot_prod += frequency[i] * g[(i + shift) % 26]
            if(mx < dot_prod):
                mx = dot_prod
                shifts[j] = shift
    res = ""
    for i in range(n):
        j = ord(text[i]) - ord('a')
        j += shifts[i % keyword_length]
        j %= 26
        res += abc[j]
    key_string = ""
    for i in range(keyword_length):
        idx = (26 - shifts[i]) % 26
        key_string += abc[idx]
        # key_string += abc[shifts[i]]
    return [key_string, res]

"""
Finds the decoded text given a key length. 
"""
def main_helper(cypher_text, keyword_length):
    cleaned_cypher_text = clean_text(cypher_text)
    decoded_cleaned_text = mutual_ic(cleaned_cypher_text, keyword_length)[1]
    ans = ""
    n = len(cypher_text)
    j = 0
    for i in range(n):
        char = cypher_text[i]
        if(char.isalpha()):
            ans += decoded_cleaned_text[j]
            j += 1
        else:
            ans += char
    return [mutual_ic(cleaned_cypher_text, keyword_length)[0] , ans]

"""
Final Main function
"""
def main(cypher_text):
    cleaned_cypher_text = clean_text(cypher_text)
    L = ic(cleaned_cypher_text)
    key_string =  main_helper(cypher_text, L[0])
    print("key := ", key_string[0])
    print("Actual Text := ", key_string[1])

"""
Function used for testing from our side. 
"""
def vigenere_cipher_encode(text, keyword):
    original_text = text
    text = clean_text(text)
    keyword = clean_text(keyword)
    encoded_text = []
    keyword_length = len(keyword)
    for i, char in enumerate(text):
        shift = ord(keyword[i % keyword_length]) - ord('a')
        idx = ord(char) - ord('a')
        idx += shift 
        idx %= 26
        encoded_char = abc[idx]
        encoded_text.append(encoded_char)
    j = 0
    n = len(original_text)
    encoded_string = ""
    for i in range(n):
        char = original_text[i]
        if(char.isalpha()):
            encoded_string += encoded_text[j]
            j += 1
        else:
            encoded_string += char
    return encoded_string

with open('A.in', 'r') as file:
    cypher_text = file.read()
main(cypher_text)
# Give it a text , will generate a test case for you. 
# def Generator(text):
#     t1 = vigenere_cipher_encode(text, "Hello")
#     print(t1)
# Text = ""
# Generator(Text)
# We also have to print the actual key used.
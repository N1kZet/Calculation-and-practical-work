 
alphabet = {
    'а': 1, 'б': 2, 'в': 3, 'г': 4, 'д': 5, 'е': 6, 'ё': 7,
    'ж': 8, 'з': 9, 'и': 10, 'й': 11, 'к': 12, 'л': 13,
    'м': 14, 'н': 15, 'о': 16, 'п': 17, 'р': 18, 'с': 19,
    'т': 20, 'у': 21, 'ф': 22, 'х': 23, 'ц': 24, 'ч': 25,
    'ш': 26, 'щ': 27, 'ъ': 28, 'ы': 29, 'ь': 30, 'э': 31,
    'ю': 32, 'я': 33
}


reverse_alphabet = {v: k for k, v in alphabet.items()}


word = "гадалка"
p = 11
q = 17


n = p * q
phi = (p - 1) * (q - 1)


d = 7  


def find_e(d, phi):
    for e in range(2, phi):
        if (e * d) % phi == 1:
            return e

e = find_e(d, phi)

print("Открытый ключ (e, n):", (e, n))
print("Закрытый ключ (d, n):", (d, n))


M = [alphabet[ch] for ch in word]
print("Числовое представление:", M)

C = [pow(m, e, n) for m in M]
print("Зашифрованное сообщение:", C)


M_decrypted = [pow(c, d, n) for c in C]
print("Расшифрованные числа:", M_decrypted)

decrypted_word = ''.join(reverse_alphabet[m] for m in M_decrypted)
print("Расшифрованное слово:", decrypted_word)
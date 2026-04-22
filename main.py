import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Шифрование - Вариант 6")
        self.root.geometry("750x650")
        self.root.resizable(True, True)

        # Данные варианта
        self.word = "гадалка"
        self.p = 11
        self.q = 17

        # Кодировка букв (русский алфавит, а=1)
        self.alphabet = {
            'а': 1, 'б': 2, 'в': 3, 'г': 4, 'д': 5, 'е': 6, 'ё': 7,
            'ж': 8, 'з': 9, 'и': 10, 'й': 11, 'к': 12, 'л': 13, 'м': 14,
            'н': 15, 'о': 16, 'п': 17, 'р': 18, 'с': 19, 'т': 20, 'у': 21,
            'ф': 22, 'х': 23, 'ц': 24, 'ч': 25, 'ш': 26, 'щ': 27, 'ъ': 28,
            'ы': 29, 'ь': 30, 'э': 31, 'ю': 32, 'я': 33
        }
        self.rev_alphabet = {v: k for k, v in self.alphabet.items()}

        # Генерация ключей RSA
        self.generate_keys()

        # Создание интерфейса
        self.create_widgets()

        # Автоматический расчет
        self.calculate()

    def generate_keys(self):
        """Генерация открытого и закрытого ключей RSA"""
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        # Выбираем e = 7 (взаимно простое с phi)
        self.e = 7

        # Находим d (обратное к e по модулю phi)
        self.d = self.mod_inverse(self.e, self.phi)

    def mod_inverse(self, a, m):
        """Нахождение обратного числа по модулю m (расширенный алгоритм Евклида)"""
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            a, m = m, a % m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def mod_pow(self, base, exp, mod):
        """Быстрое возведение в степень по модулю"""
        result = 1
        base = base % mod
        while exp > 0:
            if exp & 1:
                result = (result * base) % mod
            base = (base * base) % mod
            exp >>= 1
        return result

    def text_to_numbers(self, text):
        """Преобразование текста в числовую последовательность"""
        numbers = []
        for ch in text.lower():
            if ch in self.alphabet:
                numbers.append(self.alphabet[ch])
            else:
                raise ValueError(f"Недопустимый символ: {ch}")
        return numbers

    def numbers_to_text(self, numbers):
        """Преобразование числовой последовательности в текст"""
        text = ""
        for num in numbers:
            if num in self.rev_alphabet:
                text += self.rev_alphabet[num]
            else:
                text += "?"
        return text

    def encrypt(self, numbers):
        """Шифрование числовой последовательности"""
        encrypted = []
        for m in numbers:
            c = self.mod_pow(m, self.e, self.n)
            encrypted.append(c)
        return encrypted

    def decrypt(self, encrypted_numbers):
        """Расшифрование числовой последовательности"""
        decrypted = []
        for c in encrypted_numbers:
            m = self.mod_pow(c, self.d, self.n)
            decrypted.append(m)
        return decrypted

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        title = tk.Label(self.root, text="RSA Асимметричное Шифрование", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Информация о варианте
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(info_frame, text=f"Вариант 6 | Слово: {self.word} | p = {self.p}, q = {self.q}",
                 font=("Arial", 10, "bold"), fg="blue").pack()

        # Ключи
        keys_frame = tk.LabelFrame(self.root, text="Ключи RSA", font=("Arial", 10, "bold"))
        keys_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(keys_frame, text=f"n = p × q = {self.p} × {self.q} = {self.n}").pack(anchor=tk.W, padx=5)
        tk.Label(keys_frame, text=f"φ(n) = (p-1)(q-1) = {self.p-1} × {self.q-1} = {self.phi}").pack(anchor=tk.W, padx=5)
        tk.Label(keys_frame, text=f"Открытая экспонента e = {self.e}").pack(anchor=tk.W, padx=5)
        tk.Label(keys_frame, text=f"Закрытая экспонента d = {self.d} (e×d ≡ 1 mod φ(n))").pack(anchor=tk.W, padx=5)
        tk.Label(keys_frame, text=f"Открытый ключ: {{{self.e}, {self.n}}}").pack(anchor=tk.W, padx=5)
        tk.Label(keys_frame, text=f"Закрытый ключ: {{{self.d}, {self.n}}}").pack(anchor=tk.W, padx=5)

        # Основная таблица
        table_frame = tk.LabelFrame(self.root, text="Результаты шифрования и расшифрования", font=("Arial", 10, "bold"))
        table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Создание Treeview для таблицы
        columns = ("Буква", "Код M", "Шифрование (M^e mod n)", "Расшифрование (C^d mod n)", "Результат")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar для таблицы
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Кнопки управления
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Выполнить расчет", command=self.calculate, bg="lightgreen", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Итоговые результаты
        result_frame = tk.LabelFrame(self.root, text="Результат", font=("Arial", 10, "bold"))
        result_frame.pack(pady=5, padx=10, fill=tk.X)

        self.result_text = ScrolledText(result_frame, height=6, font=("Courier", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def calculate(self):
        """Основной расчет"""
        # Очистка таблицы и текста
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.result_text.delete(1.0, tk.END)

        try:
            # Преобразование слова в числа
            numbers = self.text_to_numbers(self.word)

            # Шифрование
            encrypted = self.encrypt(numbers)

            # Расшифрование
            decrypted = self.decrypt(encrypted)

            # Восстановление текста
            decrypted_text = self.numbers_to_text(decrypted)

            # Заполнение таблицы
            for i, (ch, m, c, m_dec) in enumerate(zip(self.word, numbers, encrypted, decrypted)):
                self.tree.insert("", tk.END, values=(ch.upper(), m, c, m_dec, self.rev_alphabet.get(m_dec, "?")))

            # Формирование результата
            result = "=" * 60 + "\n"
            result += "РЕЗУЛЬТАТЫ РАСЧЕТА\n"
            result += "=" * 60 + "\n\n"

            result += f"Исходное слово: {self.word}\n"
            result += f"Числовые коды (M): {numbers}\n\n"

            result += f"Зашифрованные коды (C = M^{self.e} mod {self.n}):\n"
            result += f"{encrypted}\n\n"

            result += f"Расшифрованные коды (M = C^{self.d} mod {self.n}):\n"
            result += f"{decrypted}\n\n"

            result += f"Расшифрованное слово: {decrypted_text}\n\n"

            result += "=" * 60 + "\n"
            result += "Проверка пройдена: исходное слово совпадает с расшифрованным ✓\n"
            result += "=" * 60

            if decrypted_text == self.word:
                self.result_text.insert(tk.END, result)
                messagebox.showinfo("Успех", "Шифрование и расшифрование выполнены успешно!")
            else:
                self.result_text.insert(tk.END, "ОШИБКА: Расшифрованное слово не совпадает с исходным!")
                messagebox.showerror("Ошибка", "Расшифрованное слово не совпадает с исходным!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")


def main():
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()


main()
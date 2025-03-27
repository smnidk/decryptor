import flet as ft
import os
import binascii
from aes_modified import string_to_key, encrypt, decrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from aes_modified import string_to_key, encrypt, decrypt
from caesar import caesar_encrypt, caesar_decrypt
from vigenere import vigenere_encrypt, vigenere_decrypt
from quadratic_cipher import quadratic_encrypt, quadratic_decrypt
from aes import aes_encrypt, aes_decrypt

def main(page: ft.Page):
    page.title = "Encryptor"
    page.window_width = 400
    page.window_height = 500

    # Функция для обновления полей ввода ключей
    def update_key_inputs(e=None):
        """Обновляет поля для ввода ключей в модифицированном AES."""
        num_keys = int(input_fields["num_keys"].value) if input_fields["num_keys"].value.isdigit() else 0
        while len(key_inputs) < num_keys:
            key_input = ft.TextField(label=f"Введите ключ {len(key_inputs) + 1}:")
            key_inputs.append(key_input)
            # Добавляем поле для ключа перед результатом
            scroll_column.controls.insert(-2, key_input)
        while len(key_inputs) > num_keys:
            key_input = key_inputs.pop()
            scroll_column.controls.remove(key_input)
        for i, key_input in enumerate(key_inputs):
            key_input.visible = True
            key_input.label = f"Введите ключ {i + 1}:"
        page.update()

    # Функция для генерации случайных ключей в формате hex
    def generate_keys(e):
        method = method_combo.value
        if method == "AES":
            key = binascii.hexlify(os.urandom(16)).decode()
            input_fields["key"].value = key
        elif method == "Модифицированный AES":
            for key_input in key_inputs:
                key = binascii.hexlify(os.urandom(16)).decode()
                key_input.value = key
        page.update()

    # Поля ввода
    key_inputs = []
    input_fields = {
        "key": ft.TextField(label="Введите ключ:"),
        "param": ft.TextField(label="Введите параметры:"),
        "a": ft.TextField(label="Введите a:"),
        "b": ft.TextField(label="Введите b:"),
        "c": ft.TextField(label="Введите c:"),
        "m": ft.TextField(label="Введите m:"),
        "num_keys": ft.TextField(label="Введите количество ключей:", on_change=update_key_inputs),
        "depth": ft.TextField(label="Введите глубину:"),
        "rsa_key": ft.TextField(label="Введите путь к RSA ключу:"),
    }

    # Методы шифрования и их параметры
    methods = {
        "Цезарь": {"param": "Введите сдвиг:"},
        "Виженер": {"key": "Введите ключ:"},
        "Квадратичный шифр": {"a": "Введите a:", "b": "Введите b:", "c": "Введите c:", "m": "Введите m:"},
        "AES": {"key": "Введите ключ:"},
        "Модифицированный AES": {"num_keys": "Введите количество ключей:", "depth": "Введите глубину:", "rsa_key": "Введите путь к RSA ключу:"},
    }

    def update_params(e):
        """Обновляет видимость полей ввода в зависимости от выбранного метода."""
        method = method_combo.value
        for field in input_fields.values():
            field.visible = False
            field.label = ""

        if method in methods:
            for param, label in methods[method].items():
                input_fields[param].visible = True
                input_fields[param].label = label

        if method == "Модифицированный AES":
            update_key_inputs()
        else:
            # Очистка полей ввода ключей при переключении метода
            key_inputs.clear()
            scroll_column.controls = [
                action_label,
                action_combo,
                method_label,
                method_combo,
                text_label,
                text_input,
                *input_fields.values(),
                result_label,
                result_output,
                process_button,
                generate_button,  # Добавляем кнопку генерации ключей
            ]

        page.update()

    def process(e):
        """Обрабатывает шифрование или дешифрование."""
        action = action_combo.value
        method = method_combo.value
        text = text_input.value

        try:
            if method == "Цезарь":
                shift = int(input_fields["param"].value)
                result = caesar_encrypt(text, shift) if action == "Шифрование" else caesar_decrypt(text, shift)
            elif method == "Виженер":
                key = input_fields["key"].value
                if not key:
                    raise ValueError("Ключ не может быть пустым. Пожалуйста, введите ключ.")
                result = vigenere_encrypt(text, key) if action == "Шифрование" else vigenere_decrypt(text, key)
            elif method == "Квадратичный шифр":
                a = int(input_fields["a"].value)
                b = int(input_fields["b"].value)
                c = int(input_fields["c"].value)
                m = int(input_fields["m"].value)
                if action == "Шифрование":
                    result = quadratic_encrypt(text, a, b, c, m)
                else:
                    # Убираем пробелы и преобразуем строку в список чисел
                    encrypted = [int(x.strip()) for x in text.split(",") if x.strip()]
                    result = quadratic_decrypt(encrypted, a, b, c, m, "")
            elif method == "AES":
                key = input_fields["key"].value
                if not key:
                    raise ValueError("Ключ не может быть пустым. Пожалуйста, введите ключ.")
                result = aes_encrypt(text, key) if action == "Шифрование" else aes_decrypt(text, key)
            elif method == "Модифицированный AES":
                num_keys = int(input_fields["num_keys"].value)
                depth = int(input_fields["depth"].value)
                rsa_key_path = input_fields["rsa_key"].value
                if not rsa_key_path:
                    raise ValueError("Путь к RSA ключу не может быть пустым. Пожалуйста, введите путь к RSA ключу.")
                keys = [string_to_key(key_input.value) for key_input in key_inputs]
                if any(not key for key in keys):
                    raise ValueError("Все ключи должны быть заполнены. Пожалуйста, введите все ключи.")
                
                # Загрузка RSA ключа
                with open(rsa_key_path, 'rb') as f:
                    rsa_key = RSA.import_key(f.read())
                cipher_rsa = PKCS1_OAEP.new(rsa_key)
                
                if action == "Шифрование":
                    # Шифрование AES-ключей
                    encrypted_aes_keys = [cipher_rsa.encrypt(key) for key in keys]
                    encrypted_keys_block = b''.join(encrypted_aes_keys)
                    
                    # Шифрование данных
                    encrypted_data = encrypt(text.encode(), keys, depth)
                    final_output = encrypted_keys_block + encrypted_data
                    result = binascii.hexlify(final_output).decode()
                else:
                    try:
                        encrypted_data = bytes.fromhex(text)
                        rsa_block_size = rsa_key.size_in_bytes()
                        encrypted_keys_size = num_keys * rsa_block_size

                        if len(encrypted_data) < encrypted_keys_size:
                            raise ValueError("Недостаточно данных для извлечения ключей.")
                        
                        encrypted_keys_block = encrypted_data[:encrypted_keys_size]
                        encrypted_data = encrypted_data[encrypted_keys_size:]
                        
                        # Извлечение и расшифрование AES-ключей
                        encrypted_aes_keys = [encrypted_keys_block[i*rsa_block_size:(i+1)*rsa_block_size] for i in range(num_keys)]
                        aes_keys = [cipher_rsa.decrypt(enc_key) for enc_key in encrypted_aes_keys]
                        
                        # Дешифрование данных
                        decrypted_data = decrypt(encrypted_data, aes_keys, depth)
                        result = decrypted_data.decode(errors="ignore")
                    except ValueError:
                        result = "Ошибка: Введенный текст не является допустимой шестнадцатеричной строкой. Пожалуйста, введите корректный текст."
            else:
                result = "Неверный метод шифрования. Пожалуйста, выберите корректный метод."
        except ValueError as ve:
            result = f"Ошибка: {str(ve)}"
        except Exception as e:
            result = f"Произошла ошибка: {str(e)}. Пожалуйста, проверьте введенные данные и попробуйте снова."

        result_output.value = result
        page.update()

    # Элементы интерфейса
    action_label = ft.Text("Выберите действие:")
    action_combo = ft.Dropdown(options=[ft.dropdown.Option("Шифрование"), ft.dropdown.Option("Дешифрование")])

    method_label = ft.Text("Выберите метод шифрования:")
    method_combo = ft.Dropdown(
        options=[ft.dropdown.Option(method) for method in methods.keys()],
        on_change=update_params,
    )

    text_label = ft.Text("Введите текст:")
    text_input = ft.TextField(multiline=True)

    result_label = ft.Text("Результат:")
    result_output = ft.TextField(read_only=True, multiline=True)

    process_button = ft.ElevatedButton(text="Выполнить", on_click=process)

    generate_button = ft.ElevatedButton(text="Сгенерировать ключи", on_click=generate_keys)

    # Создаем колонку с прокруткой
    scroll_column = ft.Column(
        controls=[
            action_label,
            action_combo,
            method_label,
            method_combo,
            text_label,
            text_input,
            *input_fields.values(),
            result_label,
            result_output,
            process_button,
            generate_button,  # Добавляем кнопку генерации ключей
        ],
        scroll=True,  # Включаем прокрутку
        expand=True,  # Растягиваем колонку на всю доступную высоту
    )

    # Добавляем колонку на страницу
    page.add(scroll_column)

    update_params(None)  # Инициализация параметров

ft.app(target=main)
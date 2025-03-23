import flet as ft
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
    }

    # Методы шифрования и их параметры
    methods = {
        "Цезарь": {"param": "Введите сдвиг:"},
        "Виженер": {"key": "Введите ключ:"},
        "Квадратичный шифр": {"a": "Введите a:", "b": "Введите b:", "c": "Введите c:", "m": "Введите m:"},
        "AES": {"key": "Введите ключ:"},
        "Модифицированный AES": {"num_keys": "Введите количество ключей:", "depth": "Введите глубину:"},
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
                result = vigenere_encrypt(text, key) if action == "Шифрование" else vigenere_decrypt(text, key)
            elif method == "Квадратичный шифр":
                a = int(input_fields["a"].value)
                b = int(input_fields["b"].value)
                c = int(input_fields["c"].value)
                m = int(input_fields["m"].value)
                if action == "Шифрование":
                    result = quadratic_encrypt(text, a, b, c, m)
                else:
                    encrypted = list(map(int, text.split(",")))
                    result = quadratic_decrypt(encrypted, a, b, c, m)
            elif method == "AES":
                key = input_fields["key"].value
                result = aes_encrypt(text, key) if action == "Шифрование" else aes_decrypt(text, key)
            elif method == "Модифицированный AES":
                num_keys = int(input_fields["num_keys"].value)
                depth = int(input_fields["depth"].value)
                keys = [string_to_key(key_input.value) for key_input in key_inputs]
                if action == "Шифрование":
                    result = encrypt(text.encode(), keys, depth).hex()
                else:
                    encrypted = bytes.fromhex(text)
                    result = decrypt(encrypted, keys, depth).decode(errors="ignore")
            else:
                result = "Неверный метод шифрования"
        except Exception as e:
            result = f"Ошибка: {str(e)}"

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
        ],
        scroll=True,  # Включаем прокрутку
        expand=True,  # Растягиваем колонку на всю доступную высоту
    )

    # Добавляем колонку на страницу
    page.add(scroll_column)

    update_params(None)  # Инициализация параметров

ft.app(target=main)
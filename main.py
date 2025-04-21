import flet as ft
from aes_modified import encrypt, decrypt, generate_random_key
from caesar import caesar_encrypt, caesar_decrypt
from vigenere import vigenere_encrypt, vigenere_decrypt
from quadratic_cipher import quadratic_encrypt, quadratic_decrypt
from aes import aes_encrypt, aes_decrypt


def main(page: ft.Page):
    page.title = "Encryptor/Decryptor"
    page.window_width = 450
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Функция для проверки ввода чисел
    def validate_numeric_input(e):
        if not e.control.value.isdigit():
            e.control.value = "".join(filter(str.isdigit, e.control.value))
        page.update()

    # Функция для обновления полей ввода ключей
    def update_key_inputs(e=None):
        method = method_combo.value
        if method != "Модифицированный AES":
            while key_inputs:
                key_input = key_inputs.pop()
                scroll_column.controls.remove(key_input)
            return

        num_keys = (
            int(input_fields["num_keys"].value)
            if input_fields["num_keys"].value.isdigit()
            else 0
        )
        while len(key_inputs) < num_keys:
            key_input = ft.TextField(
                label=f"Ключ {len(key_inputs) + 1}:",
                hint_text="Введите hex-строку (32 символа)",
                width=300,
            )
            key_inputs.append(key_input)
            scroll_column.controls.insert(-3, key_input)
        while len(key_inputs) > num_keys:
            key_input = key_inputs.pop()
            scroll_column.controls.remove(key_input)
        page.update()

    # Поля ввода
    key_inputs = []
    input_fields = {
        "key": ft.TextField(label="Ключ:", width=300),
        "param": ft.TextField(
            label="Сдвиг:", on_change=validate_numeric_input, width=150
        ),
        "a": ft.TextField(label="a:", on_change=validate_numeric_input, width=100),
        "b": ft.TextField(label="b:", on_change=validate_numeric_input, width=100),
        "c": ft.TextField(label="c:", on_change=validate_numeric_input, width=100),
        "m": ft.TextField(
            label="m:", hint_text="≥256", on_change=validate_numeric_input, width=150
        ),
        "num_keys": ft.TextField(
            label="Ключей:", on_change=update_key_inputs, width=150
        ),
        "depth": ft.TextField(
            label="Глубина:", on_change=validate_numeric_input, width=150
        ),
    }

    # Методы шифрования
    methods = {
        "Цезарь": ["param"],
        "Виженер": ["key"],
        "Квадратичный шифр": ["a", "b", "c", "m"],
        "AES": ["key"],
        "Модифицированный AES": ["num_keys", "depth"],
    }

    def update_params(e):
        method = method_combo.value
        result_output.value = ""

        # Скрыть все поля
        for field in input_fields.values():
            field.visible = False

        # Показать нужные поля
        if method in methods:
            for param in methods[method]:
                input_fields[param].visible = True

        update_key_inputs()
        page.update()

    # Генерация тестовых данных
    def generate_example(e):
        method = method_combo.value
        text_input.value = "Secure Data 2025"

        if method == "Модифицированный AES":
            input_fields["num_keys"].value = "2"
            input_fields["depth"].value = "3"
            update_key_inputs()
            for i in range(2):
                key_inputs[i].value = generate_random_key(16)

        elif method == "AES":
            input_fields["key"].value = generate_random_key(32)

        elif method == "Цезарь":
            input_fields["param"].value = "5"

        elif method == "Виженер":
            input_fields["key"].value = "SECRETKEY"

        elif method == "Квадратичный шифр":
            input_fields["a"].value = "1"
            input_fields["b"].value = "2"
            input_fields["c"].value = "3"
            input_fields["m"].value = "257"

        page.update()

    def process(e):
        action = action_combo.value
        method = method_combo.value
        text = text_input.value.strip()

        try:
            if not text:
                raise ValueError("Введите текст для обработки")

            if method == "Цезарь":
                if not input_fields["param"].value:
                    raise ValueError("Введите значение сдвига")
                shift = int(input_fields["param"].value)
                result = (
                    caesar_encrypt(text, shift)
                    if action == "Шифрование"
                    else caesar_decrypt(text, shift)
                )

            elif method == "Виженер":
                if not input_fields["key"].value:
                    raise ValueError("Введите ключ")
                key = input_fields["key"].value
                result = (
                    vigenere_encrypt(text, key)
                    if action == "Шифрование"
                    else vigenere_decrypt(text, key)
                )

            elif method == "Квадратичный шифр":
                params = {}
                for param in ["a", "b", "c", "m"]:
                    if not input_fields[param].value:
                        raise ValueError(f"Введите параметр {param}")
                    params[param] = int(input_fields[param].value)

                if action == "Шифрование":
                    result = quadratic_encrypt(text, **params)
                else:
                    if not all(c.isdigit() or c in [",", " "] for c in text):
                        raise ValueError(
                            "Для дешифрования введите числа через запятую, например: '123, 456'"
                        )
                    encrypted = list(map(int, text.replace(" ", "").split(",")))
                    result = quadratic_decrypt(encrypted, **params)

            elif method == "AES":
                if not input_fields["key"].value:
                    raise ValueError("Введите ключ")
                key = input_fields["key"].value
                result = (
                    aes_encrypt(text, key)
                    if action == "Шифрование"
                    else aes_decrypt(text, key)
                )

            elif method == "Модифицированный AES":
                if not input_fields["num_keys"].value:
                    raise ValueError("Укажите количество ключей")
                if not input_fields["depth"].value:
                    raise ValueError("Укажите глубину")

                num_keys = int(input_fields["num_keys"].value)
                depth = int(input_fields["depth"].value)

                if num_keys <= 0:
                    raise ValueError("Количество ключей должно быть > 0")
                if depth <= 0:
                    raise ValueError("Глубина должна быть > 0")

                if len(key_inputs) < num_keys:
                    raise ValueError(f"Введите все {num_keys} ключей")

                keys = []
                for i, key_input in enumerate(key_inputs[:num_keys]):
                    if not key_input.value:
                        raise ValueError(f"Введите ключ {i+1}")
                    try:
                        # Преобразование hex-строки в байты
                        key_bytes = bytes.fromhex(key_input.value.strip())
                        keys.append(key_bytes)
                    except ValueError:
                        raise ValueError(f"Ключ {i+1} должен быть в hex-формате!")

                if action == "Шифрование":
                    encrypted_data = encrypt(text.encode(), keys, depth)
                    result = encrypted_data.hex()
                else:
                    try:
                        encrypted_data = bytes.fromhex(text)
                        decrypted_data = decrypt(encrypted_data, keys, depth)
                        result = decrypted_data.decode(errors="ignore")
                    except ValueError:
                        raise ValueError("Для дешифрования введите hex-строку")

            else:
                result = "Выберите метод шифрования"

        except ValueError as ve:
            result = f"Ошибка ввода: {str(ve)}"
        except Exception as e:
            result = f"Ошибка обработки: {str(e)}"

        result_output.value = result
        page.update()

    # Элементы интерфейса
    action_combo = ft.Dropdown(
        options=[ft.dropdown.Option(o) for o in ["Шифрование", "Дешифрование"]],
        width=200,
        value="Шифрование",
    )

    method_combo = ft.Dropdown(
        options=[ft.dropdown.Option(m) for m in methods.keys()],
        width=200,
        on_change=update_params,
    )

    generate_btn = ft.ElevatedButton(
        "Сгенерировать пример",
        icon=ft.icons.AUTOFPS_SELECT,
        on_click=generate_example,
        width=200,
    )

    text_input = ft.TextField(
        multiline=True, min_lines=3, hint_text="Введите текст...", width=400
    )

    result_output = ft.TextField(
        read_only=True, multiline=True, min_lines=3, hint_text="Результат...", width=400
    )

    scroll_column = ft.Column(
        controls=[
            ft.Row([ft.Text("Действие:", width=100), action_combo]),
            ft.Row([ft.Text("Метод:", width=100), method_combo]),
            generate_btn,
            *[input_fields[k] for k in input_fields],
            ft.Text("Ввод данных:", weight=ft.FontWeight.BOLD),
            text_input,
            ft.Text("Результат:", weight=ft.FontWeight.BOLD),
            result_output,
            ft.ElevatedButton("Выполнить", on_click=process, width=200),
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        spacing=15,
    )

    page.add(scroll_column)
    update_params(None)


ft.app(target=main)

# Константа — текущий год (для простоты задаём вручную)
CURRENT_YEAR = 2026

# Ширина рамки в символах
WIDTH = 40
BORDER = "*" * WIDTH


def print_centered(text: str) -> None:
    """Вывести строку, выровненную по центру внутри рамки из звёздочек."""
    # Внутренняя ширина (без двух боковых '*')
    inner = WIDTH - 2
    print("*" + text.center(inner) + "*")


def print_left(label: str, value) -> None:
    """Вывести строку вида '* Метка: значение                *'."""
    inner = WIDTH - 2
    line = " " + f"{label}: {value}"
    # Дополняем пробелами справа до нужной ширины
    line = line.ljust(inner)
    print("*" + line + "*")


def age_word(age: int) -> str:
    """Подобрать правильное окончание слова 'год' для числа age."""
    n = abs(age) % 100
    n1 = n % 10
    if 10 < n < 20:
        return "лет"
    if n1 == 1:
        return "год"
    if 2 <= n1 <= 4:
        return "года"
    return "лет"


def main() -> None:
    # --- Заголовок ---
    print(BORDER)
    print_centered("Личная визитка")
    print(BORDER)
    print()

    # --- Ввод данных ---
    name = input("Введите ваше имя: ").strip()
    surname = input("Введите вашу фамилию: ").strip()

    # Преобразование строки в целое число
    year_of_birth = int(input("Введите год рождения: "))

    # Преобразование строки в число с плавающей точкой
    # Заменяем запятую на точку для удобства пользователя
    height = float(input("Введите ваш рост (см): ").replace(",", "."))

    # --- Вычисление возраста ---
    age = CURRENT_YEAR - year_of_birth

    # --- Вывод визитки ---
    print()
    print(BORDER)
    print_centered("ВАША ВИЗИТКА")
    print(BORDER)
    print_left("Имя", name)
    print_left("Фамилия", surname)
    print_left("Год рождения", year_of_birth)
    print_left("Возраст", f"{age} {age_word(age)}")
    print_left("Рост", f"{height} см")
    print(BORDER)


if __name__ == "__main__":
    main()
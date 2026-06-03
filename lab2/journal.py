from pathlib import Path
from datetime import datetime

# ---------- Кроссплатформенные пути ----------
# Path(__file__).resolve().parent — каталог, где лежит сам скрипт
# (работает одинаково на Windows, Linux, macOS)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "journal.txt"

# Разделитель полей в файле
SEP = " | "


def ensure_storage() -> None:
    """Создать папку data и пустой файл журнала, если их ещё нет."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.touch()


# ---------- Ввод с проверкой ----------
def input_date() -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД с проверкой корректности."""
    while True:
        s = input("Введите дату (ГГГГ-ММ-ДД): ").strip()
        try:
            # strptime выбросит ValueError при неверном формате/несуществующей дате
            datetime.strptime(s, "%Y-%m-%d")
            return s
        except ValueError:
            print("  Ошибка: неверный формат даты. Пример: 2024-09-15")


def input_text() -> str:
    """Запросить непустой текст наблюдения."""
    while True:
        s = input("Введите текст наблюдения: ").strip()
        if not s:
            print("  Ошибка: текст не может быть пустым.")
            continue
        # Уберём символ-разделитель, чтобы не сломать формат файла
        if SEP.strip() in s:
            s = s.replace("|", "/")
        return s


def input_score() -> int:
    """Запросить целую оценку в диапазоне 1..10."""
    while True:
        s = input("Введите оценку (1-10): ").strip()
        try:
            n = int(s)
        except ValueError:
            print("  Ошибка: нужно ввести целое число.")
            continue
        if 1 <= n <= 10:
            return n
        print("  Ошибка: оценка должна быть от 1 до 10.")


# ---------- Операции с журналом ----------
def add_record() -> None:
    """Добавить новую запись в файл."""
    print("\n--- Добавление новой записи ---")
    date = input_date()
    text = input_text()
    score = input_score()

    # Открываем в текстовом режиме — Python сам подставит \n / \r\n
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{date}{SEP}{score}{SEP}{text}\n")

    print("\nЗапись успешно добавлена!\n")


def read_records() -> list[tuple[str, int, str]]:
    """Прочитать все записи из файла и вернуть список кортежей."""
    records = []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if not line:
                continue
            parts = line.split(SEP, 2)
            if len(parts) != 3:
                continue
            date, score, text = parts
            try:
                records.append((date, int(score), text))
            except ValueError:
                continue
    return records


def show_records() -> None:
    """Вывести все записи в виде таблицы и статистику."""
    print("\n--- Все записи ---")
    records = read_records()

    if not records:
        print("Журнал пуст.\n")
        return

    # Ширины колонок
    w_date = 10
    w_score = 6
    w_text = max(20, max(len(r[2]) for r in records))

    sep_line = "+" + "-" * (w_date + 2) + "+" + "-" * (w_score + 2) + "+" + "-" * (w_text + 2) + "+"
    header = (
        f"| {'Дата'.center(w_date)} "
        f"| {'Оценка'.center(w_score)} "
        f"| {'Текст'.center(w_text)} |"
    )

    print(sep_line)
    print(header)
    print(sep_line)
    for date, score, text in records:
        print(
            f"| {date.center(w_date)} "
            f"| {str(score).center(w_score)} "
            f"| {text.ljust(w_text)} |"
        )
    print(sep_line)

    avg = sum(r[1] for r in records) / len(records)
    print("\nСтатистика:")
    print(f"Всего записей: {len(records)}")
    print(f"Средняя оценка: {avg:.2f}\n")


def clear_journal() -> None:
    """Очистить файл журнала."""
    confirm = input("Вы уверены, что хотите очистить журнал? (д/н): ").strip().lower()
    if confirm in ("д", "да", "y", "yes"):
        # Открытие в режиме 'w' усекает файл до нулевой длины
        DATA_FILE.open("w", encoding="utf-8").close()
        print("Журнал очищен.\n")
    else:
        print("Очистка отменена.\n")


# ---------- Главное меню ----------
def print_menu() -> None:
    print("=" * 40)
    print("        ЖУРНАЛ НАБЛЮДЕНИЙ")
    print("=" * 40)
    print("Выберите действие:")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Очистить журнал")
    print("4. Выход")


def main() -> None:
    ensure_storage()
    while True:
        print_menu()
        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            add_record()
        elif choice == "2":
            show_records()
        elif choice == "3":
            clear_journal()
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("  Неверный пункт меню. Введите число от 1 до 4.\n")


if __name__ == "__main__":
    main()
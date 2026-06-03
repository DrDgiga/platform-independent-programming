import json
from datetime import datetime
from pathlib import Path

# ---------- Константы ----------
# Каталог программы и файл данных определяются кроссплатформенно
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "notes.json"

# Форматы даты и времени
DT_FORMAT = "%d.%m.%Y %H:%M:%S"   # для отображения и хранения
DATE_FORMAT = "%d.%m.%Y"          # для поиска по дате


# ---------- Работа с файлом ----------
def load_notes() -> list[dict]:
    """Загрузить список заметок из JSON-файла.

    Если файл отсутствует или повреждён, возвращается пустой список.
    """
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            # На случай, если в файле оказался не список
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Предупреждение: файл данных повреждён, создаётся новый.")
        return []


def save_notes(notes: list[dict]) -> None:
    """Сохранить список заметок в JSON-файл (UTF-8, с отступами)."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


# ---------- Основные действия ----------
def create_note() -> None:
    """Создать новую заметку и сохранить её в файл."""
    print("\n--- Создание новой заметки ---")
    title = input("Введите заголовок заметки: ").strip()
    if not title:
        print("Заголовок не может быть пустым.\n")
        return

    text = input("Введите текст заметки: ").strip()
    if not text:
        print("Текст заметки не может быть пустым.\n")
        return

    # Автоматическая дата и время создания
    created = datetime.now().strftime(DT_FORMAT)

    note = {
        "title": title,
        "text": text,
        "created": created,
    }

    notes = load_notes()
    notes.append(note)
    save_notes(notes)

    print(f"Заметка успешно сохранена (дата: {created}).\n")


def show_all_notes() -> None:
    """Вывести все заметки в красивом виде."""
    notes = load_notes()
    print("\n--- Все заметки ---")

    if not notes:
        print("Заметок пока нет.\n")
        return

    for i, note in enumerate(notes, start=1):
        print("=" * 50)
        print(f"Заметка №{i}")
        print(f"Дата:      {note.get('created', '—')}")
        print(f"Заголовок: {note.get('title', '—')}")
        print(f"Текст:     {note.get('text', '—')}")
    print("=" * 50)
    print(f"Всего заметок: {len(notes)}\n")


def find_notes_by_date() -> None:
    """Найти все заметки за указанную дату."""
    print("\n--- Поиск заметок по дате ---")
    date_str = input("Введите дату (ДД.ММ.ГГГГ): ").strip()

    # Проверка корректности формата
    try:
        target_date = datetime.strptime(date_str, DATE_FORMAT).date()
    except ValueError:
        print("Неверный формат даты. Пример: 15.09.2024\n")
        return

    notes = load_notes()
    found = []
    for note in notes:
        try:
            note_date = datetime.strptime(note["created"], DT_FORMAT).date()
        except (ValueError, KeyError):
            continue
        if note_date == target_date:
            found.append(note)

    if not found:
        print(f"За {date_str} заметок не найдено.\n")
        return

    print(f"Найдено заметок: {len(found)}")
    for i, note in enumerate(found, start=1):
        print("-" * 50)
        print(f"Заметка №{i}")
        print(f"Время:     {note['created']}")
        print(f"Заголовок: {note['title']}")
        print(f"Текст:     {note['text']}")
    print("-" * 50 + "\n")


# ---------- Главное меню ----------
def print_menu() -> None:
    print("=" * 40)
    print("       ДНЕВНИК ЗАМЕТОК")
    print("=" * 40)
    print("1 – Создать новую заметку")
    print("2 – Показать все заметки")
    print("3 – Найти заметку по дате")
    print("4 – Выход")


def main() -> None:
    while True:
        print_menu()
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            create_note()
        elif choice == "2":
            show_all_notes()
        elif choice == "3":
            find_notes_by_date()
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню. Введите число от 1 до 4.\n")


if __name__ == "__main__":
    main()
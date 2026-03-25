# @title Виселица
import random
import os

# загрузка этапов виселицы

def load_hangman_stages_from_files(total=8):
    """
    Загружает все стадии виселицы из папки 'stages', которая находится рядом со скриптом.
    total — количество стадий (по умолчанию 8, файлы 0.txt до 7.txt)
    """
    stages = []

    # путь к текущему скрипту
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stages_folder = os.path.join(script_dir, "stages")

    for i in range(total):
        filename = os.path.join(stages_folder, f"{i}.txt")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                stages.append(f.read())
        except FileNotFoundError:
            print(f"⚠️ Файл стадии не найден: {filename}")
            stages.append("[Стадия отсутствует]")

    return stages


def if_not_word(text):
    return any(char.isdigit() for char in text)


def clean(text):
    result = ''
    for char in text:
      if char.isalpha():
        result += char
    return result.upper()


def load_words(filename):
    words = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or ":" not in line:
                    continue

                word_part, hint_part = line.split(":", 1)

                word = clean(word_part)
                hint = hint_part.strip()

                if word and not if_not_word(word):
                    words.append({
                        "word": word.upper(),
                        "hint": hint.lower()
                    })

        if words:
            return words

    except FileNotFoundError:
        print("Файл со словами не найден.")

    # На  случай отсуствия файла
    return [
        {"word": "ПИТОН", "hint": "язык программирования, а также змея"},
        {"word": "КРОКОДИЛ", "hint": "зелёное зубастое животное"}
    ]

def choose_word(words_list):
    entry = random.choice(words_list)
    return entry["word"], entry["hint"]


def display_hangman(tries):
    index = len(HANGMAN_STAGES) - 1 - tries
    index = max(0, min(index, len(HANGMAN_STAGES) - 1))
    return HANGMAN_STAGES[index]


def initialize_game(words_source):
    word, hint = choose_word(words_source)
    return {
        "word": word,
        "hint": hint,
        "display": ["_"] * len(word),
        "guessed_letters": set(),
        "wrong_letters": set(),
        "tries_left": len(HANGMAN_STAGES) - 1,
        "game_over": False
    }


def display_state(game):
    print("\n" + "=" * 40)
    print(f"Подсказка: {game['hint']}")
    print(display_hangman(game["tries_left"]))
    print("Слово: " + " ".join(game["display"]))
    print(f"Осталось попыток: {game['tries_left']}")
    if game["wrong_letters"]:
        print("Ошибочные буквы:", ", ".join(sorted(game["wrong_letters"])))
    print()


def get_guess():
    while True:
        guess = input("Введите букву или слово целиком: ").strip().upper()
        if not guess:
            print("Вы ничего не ввели. Попробуйте снова.")
            continue
        if not guess.isalpha():
            print("Можно использовать только буквы.")
            continue
        return guess


def process_guess(game, guess):
    if game["game_over"]:
        return

    if len(guess) == 1:
        if guess in game["guessed_letters"] or guess in game["wrong_letters"]:
            print("Вы уже называли эту букву.")
            return

        if guess in game["word"]:
            game["guessed_letters"].add(guess)
            for i, ch in enumerate(game["word"]):
                if ch == guess:
                    game["display"][i] = guess
            print(f"Буква {guess} есть!")
        else:
            game["wrong_letters"].add(guess)
            game["tries_left"] -= 1
            print(f"Буквы {guess} нет.")

    elif len(guess) == len(game["word"]):
        if guess == game["word"]:
            game["display"] = list(game["word"])
            game["game_over"] = True
            print("Вы угадали слово!")
        else:
            game["tries_left"] -= 1
            print("Неверное слово.")
    else:
        print("Неверная длина слова.")

    if "_" not in game["display"]:
        game["game_over"] = True
        print("Победа!")
    elif game["tries_left"] <= 0:
        game["game_over"] = True
        print("Вы проиграли.")


def is_finished(game):
    return game["game_over"]


def display_result(game):
    if "_" not in game["display"]:
        print(f"\nВы выиграли! Слово: {game['word']}")
        input("Нажмите Enter, чтобы выйти...")
    else:
        print(f"\nВы проиграли. Слово: {game['word']}")
        input("Нажмите Enter, чтобы выйти...")


def run_game():
    global HANGMAN_STAGES

    print("Добро пожаловать в Виселицу!")

    # ввод файлов
    words_file = get_filename("Введите файл со словами: ")

    # загрузка
    HANGMAN_STAGES = load_hangman_stages_from_files()
    words = load_words(words_file)

    # обработка ошибок со словами и стадиями
    if not HANGMAN_STAGES:
        print("Ошибка: не удалось загрузить стадии виселицы.")
        return

    if not words:
        print("Ошибка: не удалось загрузить слова.")
        return

    game = initialize_game(words)

    while not is_finished(game):
        display_state(game)
        guess = get_guess()
        process_guess(game, guess)

    display_result(game)

def get_filename(prompt):
    while True:
        filename = input(prompt).strip()

        if not filename:
            print("Вы не ввели имя файла. Беру файл по умолчанию")
            return "words.txt"
            continue

        if "." not in filename:
            print("Укажите файл с расширением (например: words.txt)")
            continue

        if not os.path.isfile(filename):
            print("Файл не найден. Попробуйте снова.")
            continue

        if os.path.getsize(filename) == 0:
            print("Файл пустой.")
            continue

        return filename

run_game()
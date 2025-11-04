import os
import sys
import time
import atexit

TARGET_DIR = "/data/"
SELF_PATH = os.path.abspath(__file__)
success = False

def cleanup():
    """Удаляет сам файл после успешного выполнения"""
    if success:
        try:
            time.sleep(0.1)
            os.remove(SELF_PATH)
            print(f"[✓] Скрипт {os.path.basename(SELF_PATH)} удалён после выполнения")
        except Exception as e:
            print(f"[!] Ошибка при удалении себя: {e}")

atexit.register(cleanup)

def safe_replace(text: str, old: str, new: str) -> str:
    """Безопасно заменяет все варианты регистра"""
    variants = [old.lower(), old.upper(), old.capitalize()]
    for v in variants:
        text = text.replace(v, new)
    return text

def main():
    global success

    if not os.path.isdir(TARGET_DIR):
        print(f"[!] Папка {TARGET_DIR} не найдена или не является директорией!")
        return

    renamed = errors = 0

    for filename in os.listdir(TARGET_DIR):
        src = os.path.join(TARGET_DIR, filename)

        if not os.path.isfile(src):
            continue

        if "legacy" not in filename.lower():
            continue

        dst_name = safe_replace(filename, "legacy", "hikka")
        dst = os.path.join(TARGET_DIR, dst_name)

        if os.path.exists(dst):
            print(f"[!] Пропуск: {dst_name} уже существует")
            continue

        try:
            os.rename(src, dst)
            renamed += 1
            print(f"[✓] {filename} → {dst_name}")
        except Exception as e:
            errors += 1
            print(f"[!] Ошибка при переименовании {filename}: {e}")

    print(f"\n[i] Переименовано: {renamed}, ошибок: {errors}")
    success = True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Критическая ошибка: {e}")
        sys.exit(1)
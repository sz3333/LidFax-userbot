import os
import sys

# Папка, где переименовываем файлы
target_dir = "/data/"

# Путь к самому этому файлу, чтобы удалить себя
self_path = os.path.abspath(__file__)

# Переименование файлов (только в target_dir, без подпапок)
for filename in os.listdir(target_dir):
    old_path = os.path.join(target_dir, filename)
    # Проверяем, что это файл, а не папка
    if os.path.isfile(old_path) and "heroku" in filename:
        new_filename = filename.replace("heroku", "hikka")
        new_path = os.path.join(target_dir, new_filename)
        try:
            os.rename(old_path, new_path)
            print(f"[✓] Переименован: {filename} → {new_filename}")
        except Exception as e:
            print(f"[!] Ошибка при переименовании {filename}: {e}")

# Самоуничтожение скрипта
try:
    os.remove(self_path)
    print(f"[✓] Скрипт {os.path.basename(self_path)} удалён после выполнения")
except Exception as e:
    print(f"[!] Ошибка при удалении себя: {e}")

sys.exit(0)
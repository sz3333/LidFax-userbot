import os
import sys
import time
import atexit

# Папка, где переименовываем файлы
target_dir = "/data/"

# Путь к самому этому файлу
self_path = os.path.abspath(__file__)

# Флаг успешного выполнения
success = False

def cleanup():
    """Удаляем скрипт при выходе, если всё прошло успешно"""
    global success
    if success:
        try:
            # Небольшая задержка для гарантии
            time.sleep(0.1)
            if os.path.exists(self_path):
                os.remove(self_path)
                print(f"[✓] Скрипт {os.path.basename(self_path)} удалён после выполнения")
        except Exception as e:
            print(f"[!] Ошибка при удалении себя: {e}")

# Регистрируем функцию очистки
atexit.register(cleanup)

def main():
    global success
    
    # Проверяем существование целевой папки
    if not os.path.exists(target_dir):
        print(f"[!] Папка {target_dir} не существует!")
        return
    
    if not os.path.isdir(target_dir):
        print(f"[!] {target_dir} не является папкой!")
        return
    
    renamed_count = 0
    error_count = 0
    
    # Переименование файлов
    try:
        files = os.listdir(target_dir)
    except PermissionError:
        print(f"[!] Нет доступа к папке {target_dir}")
        return
    except Exception as e:
        print(f"[!] Ошибка при чтении папки: {e}")
        return
    
    for filename in files:
        old_path = os.path.join(target_dir, filename)
        
        # Проверяем, что это файл, а не папка
        if not os.path.isfile(old_path):
            continue
            
        if "legacy" not in filename.lower():
            continue
        
        # Создаём новое имя (case-insensitive замена)
        new_filename = filename.replace("legacy", "hikka").replace("legacy", "Hikka").replace("legacy", "HIKKA")
        new_path = os.path.join(target_dir, new_filename)
        
        # Проверяем, не существует ли уже файл с таким именем
        if os.path.exists(new_path):
            print(f"[!] Файл {new_filename} уже существует, пропускаем")
            continue
        
        try:
            os.rename(old_path, new_path)
            print(f"[✓] Переименован: {filename} → {new_filename}")
            renamed_count += 1
        except PermissionError:
            print(f"[!] Нет прав для переименования {filename}")
            error_count += 1
        except Exception as e:
            print(f"[!] Ошибка при переименовании {filename}: {e}")
            error_count += 1
    
    # Итоги
    print(f"\n[i] Переименовано файлов: {renamed_count}")
    if error_count > 0:
        print(f"[i] Ошибок: {error_count}")
    
    # Помечаем как успешно выполненный
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
    
    sys.exit(0)
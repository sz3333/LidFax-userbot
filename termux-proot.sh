#!/bin/bash

echo -e "\033[2J\033[3;1f"
printf "\033[1;35mLidFax auto-installer with proot-distro 🐾\033[0m\n\n"

export PROOT_NO_SECCOMP=1

# Обновляем Termux и proot-distro
echo -e "\033[0;96mUpdating Termux packages...\033[0m"
pkg update -y
pkg upgrade -y
pkg install proot-distro wget -y

DISTRO_NAME="debian"

# Полностью удаляем старую установку
echo -e "\033[0;93mCleaning up...\033[0m"
proot-distro remove $DISTRO_NAME 2>/dev/null
rm -rf $PREFIX/var/lib/proot-distro/installed-rootfs/$DISTRO_NAME

# Устанавливаем с игнорированием ошибок конфигурации
echo -e "\033[0;96mInstalling $DISTRO_NAME (ignoring config errors)...\033[0m"

# Патчим скрипт установки, чтобы игнорировать dpkg-reconfigure
DISTRO_PLUGIN="$PREFIX/etc/proot-distro/debian.sh"

if [ -f "$DISTRO_PLUGIN" ]; then
    # Создаем бэкап
    cp "$DISTRO_PLUGIN" "${DISTRO_PLUGIN}.bak"
    
    # Комментируем проблемную строку с dpkg-reconfigure
    sed -i 's/run_proot_cmd dpkg-reconfigure locales/#run_proot_cmd dpkg-reconfigure locales/g' "$DISTRO_PLUGIN"
fi

# Устанавливаем дистро
proot-distro install $DISTRO_NAME

# Восстанавливаем оригинальный файл
if [ -f "${DISTRO_PLUGIN}.bak" ]; then
    mv "${DISTRO_PLUGIN}.bak" "$DISTRO_PLUGIN"
fi

# Проверяем установку
if ! proot-distro list 2>/dev/null | grep -q "$DISTRO_NAME (installed)"; then
    echo -e "\033[0;91mInstallation failed!\033[0m"
    exit 1
fi

echo -e "\033[0;92mDebian installed successfully!\033[0m\n"

# Настройка окружения
echo -e "\033[0;96mSetting up environment...\033[0m"
proot-distro login $DISTRO_NAME -- bash -c "
export DEBIAN_FRONTEND=noninteractive
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-dev git \
    libjpeg-dev libssl-dev zlib1g-dev build-essential
"

# Установка Python пакетов
echo -e "\033[0;96mInstalling Python packages...\033[0m"
proot-distro login $DISTRO_NAME -- bash -c "
pip3 install --no-cache-dir --upgrade pip setuptools wheel
pip3 install --no-cache-dir --upgrade Pillow
"

# Клонирование LidFax
echo -e "\033[0;96mCloning LidFax...\033[0m"
proot-distro login $DISTRO_NAME -- bash -c "
rm -rf ~/LidFax-userbot
git clone -b stable https://github.com/sz3333/LidFax-userbot ~/LidFax-userbot
cd ~/LidFax-userbot
pip3 install --no-cache-dir -r requirements.txt --upgrade
"

# Запуск
echo -e "\033[0;32m\nStarting LidFax...\033[0m\n"
proot-distro login $DISTRO_NAME -- bash -c "cd ~/LidFax-userbot && python3 -m hikka --root"Что делает скрипт:Обновляет Termux полностьюПатчит файл конфигурации Debian перед установкой (комментирует проблемную строку с dpkg-reconfigure)Устанавливает Debian без ошибокВосстанавливает оригинальный файл конфигурацииЕсли это не поможет, попробуй альтернативный метод - использовать Ubuntu вместо Debian:
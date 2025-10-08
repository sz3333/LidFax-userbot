#!/bin/bash

echo -e "\033[2J\033[3;1f"
printf "\033[1;35mLidFax auto-installer with proot-distro 🐾\033[0m\n\n"

# Отключаем seccomp для обхода багов Termux
export PROOT_NO_SECCOMP=1

# Установка proot-distro если нет
if ! command -v proot-distro &>/dev/null; then
    echo -e "\033[0;96mInstalling proot-distro...\033[0m"
    pkg install proot-distro -y
fi

DISTRO_NAME="debian"

# Удаляем старую установку если есть проблемы
if proot-distro list 2>/dev/null | grep -q "$DISTRO_NAME (installed)"; then
    echo -e "\033[0;93mRemoving old installation...\033[0m"
    proot-distro remove $DISTRO_NAME
fi

# Устанавливаем дистро с флагом --override-alias
echo -e "\033[0;96mInstalling $DISTRO_NAME...\033[0m"
proot-distro install $DISTRO_NAME --override-alias debian

# Проверяем успешность установки
if ! proot-distro list 2>/dev/null | grep -q "$DISTRO_NAME (installed)"; then
    echo -e "\033[0;91mInstallation failed! Trying alternative method...\033[0m"
    pkg reinstall proot-distro -y
    proot-distro install debian
fi

# Команда внутри дистро - разбита на этапы для стабильности
echo -e "\033[0;96mEntering $DISTRO_NAME...\033[0m"

proot-distro login $DISTRO_NAME -- bash -c "
export DEBIAN_FRONTEND=noninteractive
apt update
apt upgrade -y
apt install -y python3 python3-pip git libjpeg-dev libssl-dev zlib1g-dev
"

proot-distro login $DISTRO_NAME -- bash -c "
pip3 install --no-cache-dir --upgrade pip setuptools wheel
pip3 install --no-cache-dir --upgrade Pillow
"

proot-distro login $DISTRO_NAME -- bash -c "
rm -rf ~/LidFax-userbot
git clone -b stable https://github.com/sz3333/LidFax-userbot ~/LidFax-userbot
cd ~/LidFax-userbot
pip3 install --no-cache-dir -r requirements.txt --upgrade
"

echo -e "\033[0;32mStarting LidFax...\033[0m"
proot-distro login $DISTRO_NAME -- bash -c "cd ~/LidFax-userbot && python3 -m hikka --root"
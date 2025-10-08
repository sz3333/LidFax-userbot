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

DISTRO_NAME="debian"  # стабильный вариант для Termux

# Проверяем наличие дистро
if ! proot-distro list | grep -q "$DISTRO_NAME"; then
    echo -e "\033[0;96mInstalling $DISTRO_NAME...\033[0m"
    proot-distro install $DISTRO_NAME
fi

# Команда внутри дистро
RUN_CMD="bash -c '
apt update && apt upgrade -y &&
apt install -y python3.10 python3-pip git libjpeg-dev libssl-dev &&
echo -e \"\033[0;96mInstalling Pillow...\033[0m\" &&
pip3 install --no-cache-dir --upgrade Pillow &&
echo -e \"\033[0;96mDownloading LidFax...\033[0m\" &&
rm -rf ~/LidFax-userbot &&
git clone -b stable https://github.com/sz3333/LidFax-userbot ~/LidFax-userbot &&
cd ~/LidFax-userbot &&
pip3 install --no-cache-dir -r requirements.txt --upgrade &&
echo -e \"\033[0;32mStarting LidFax with --root...\033[0m\" &&
python3 -m hikka --root
'"

# Запуск дистро
echo -e "\033[0;96mEntering $DISTRO_NAME...\033[0m"
proot-distro login $DISTRO_NAME -- $RUN_CMD

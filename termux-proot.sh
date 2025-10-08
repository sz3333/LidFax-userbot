#!/bin/bash

echo -e "\033[2J\033[3;1f"
printf "\033[1;35mLidFax auto-installer with proot-distro 🐾\033[0m\n\n"

# Проверяем proot-distro
if ! command -v proot-distro &>/dev/null; then
    echo -e "\033[0;96mInstalling proot-distro...\033[0m"
    pkg install proot-distro -y
fi

DISTRO_NAME="ubuntu-22.04"

# Проверяем наличие дистро
if ! proot-distro list | grep -q "$DISTRO_NAME"; then
    echo -e "\033[0;96mInstalling $DISTRO_NAME...\033[0m"
    proot-distro install $DISTRO_NAME
fi

# Создаём команду запуска внутри дистро
RUN_CMD="bash -c '
apt update && apt install -y python3.10 python3-pip git libjpeg-dev libssl-dev &&
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

# Запуск в proot-дистро
echo -e "\033[0;96mEntering $DISTRO_NAME...\033[0m"
proot-distro login $DISTRO_NAME -- $RUN_CMD

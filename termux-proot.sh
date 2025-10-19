#!/bin/bash
# LidFax-userbot setup script 🐾 by Лид & Mochi

set -e  # Остановить выполнение при ошибке

echo "🐾 Обновляю пакеты..."
apt update -y && apt upgrade -y

echo "🧰 Устанавливаю необходимые пакеты..."
apt install -y nano curl wget git python3-pip python3.13-venv

echo "📦 Клонирую репозиторий LidFax-userbot..."
git clone https://github.com/sz3333/LidFax-userbot -y 2>/dev/null || true

cd LidFax-userbot || exit

echo "🌿 Создаю виртуальное окружение..."
python3 -m venv venv

echo "🐍 Активирую окружение..."
source venv/bin/activate

echo "📚 Устанавливаю зависимости..."
pip install -r requirements.txt -y

echo "🚀 Запускаю LidFax-userbot..."
python3 -m hikka --root --no-web
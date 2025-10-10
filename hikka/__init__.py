"""Package init and compatibility import hooks"""

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# Do not delete this file, it will cause errors.

# Compatibility layer: map legacy `lidfaxtl` imports to Telethon
# This enables running the project with Telethon without rewriting imports.
import builtins as _builtins

_native_import = _builtins.__import__


def _hikka_import(name, *args, **kwargs):
    # Redirect all 'lidfaxtl' imports to 'telethon'
    if name.startswith("lidfaxtl"):
        name = "telethon" + name[len("lidfaxtl"):]
    return _native_import(name, *args, **kwargs)


_builtins.__import__ = _hikka_import

__author__ = "Dan Gazizullin"
__contact__ = "me@hikariatama.ru"
__copyright__ = "Copyright 2022, Dan Gazizullin"
__credits__ = ["LonamiWebs", "penn5"]
__license__ = "AGPLv3"
__maintainer__ = "developer"
__status__ = "Production"

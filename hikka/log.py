"""Main logging part"""

# пасхалка номер 3
# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import contextlib
import inspect
import io
import linecache
import logging
import re
import sys
import traceback
import typing
import time  # <--- Добавлен импорт time для работы с таймаутом антиспама
from logging.handlers import RotatingFileHandler

import lidfaxtl
try:
    from aiogram.exceptions import NetworkError
except ImportError:
    try:
        from aiogram.utils.exceptions import NetworkError
    except ImportError:
        # Fallback for older versions
        NetworkError = Exception

from . import utils
from .tl_cache import CustomTelegramClient
from .types import BotInlineCall, Module
from .web.debugger import WebDebugger

# Monkeypatch linecache to make interactive line debugger available
# in werkzeug web debugger
# This is weird, but the only adequate approach
# https://github.com/pallets/werkzeug/blob/3115aa6a6276939f5fd6efa46282e0256ff21f1a/src/werkzeug/debug/tbtools.py#L382-L416

old = linecache.getlines


def getlines(filename: str, module_globals=None) -> str:
    """
    Get the lines for a Python source file from the cache.
    Update the cache if it doesn't contain an entry for this file already.

    Modified version of original `linecache.getlines`, which returns the
    source code of LidFax modules properly. This is needed for
    interactive line debugger in werkzeug web debugger.
    """

    try:
        if filename.startswith("<") and filename.endswith(">"):
            module = filename[1:-1].split(maxsplit=1)[-1]
            if (module.startswith("hikka.modules")) and module in sys.modules:
                return list(
                    map(
                        lambda x: f"{x}\n",
                        sys.modules[module].__loader__.get_source().splitlines(),
                    )
                )
    except Exception:
        logging.debug("Can't get lines for %s", filename, exc_info=True)

    return old(filename, module_globals)


linecache.getlines = getlines


def override_text(exception: Exception) -> typing.Optional[str]:
    """Returns error-specific description if available, else `None`"""
    if isinstance(exception, NetworkError):
        return "✈️ <b>You have problems with internet🍅connection on your server.</b>"

    return None


class HikkaException:
    def __init__(
        self,
        message: str,
        full_stack: str,
        sysinfo: typing.Optional[
            typing.Tuple[object, Exception, traceback.TracebackException]
        ] = None,
    ):
        self.message = message
        self.full_stack = full_stack
        self.sysinfo = sysinfo
        self.debug_url = None
        # <--- Добавлен атрибут для счетчика антиспама
        self.repeat_count = 0 

    @classmethod
    def from_exc_info(
        cls,
        exc_type: object,
        exc_value: Exception,
        tb: traceback.TracebackException,
        stack: typing.Optional[typing.List[inspect.FrameInfo]] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> "HikkaException":
        def to_hashable(dictionary: dict) -> dict:
            dictionary = dictionary.copy()
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    dictionary[key] = to_hashable(value)
                else:
                    try:
                        if (
                            getattr(getattr(value, "__class__", None), "__name__", None)
                            == "Database"
                        ):
                            dictionary[key] = "<Database>"
                        elif isinstance(
                            value,
                            (lidfaxtl.TelegramClient, CustomTelegramClient),
                        ):
                            dictionary[key] = f"<{value.__class__.__name__}>"
                        elif len(str(value)) > 512:
                            dictionary[key] = f"{str(value)[:512]}..."
                        else:
                            dictionary[key] = str(value)
                    except Exception:
                        dictionary[key] = f"<{value.__class__.__name__}>"

            return dictionary

        full_traceback = traceback.format_exc().replace(
            "Traceback (most recent call last):\n",
            "",
        )

        line_regex = re.compile(r'  File "(.*?)", line ([0-9]+), in (.+)')

        def format_line(line: str) -> str:
            filename_, lineno_, name_ = line_regex.search(line).groups()

            return (
                f"👉 <code>{utils.escape_html(filename_)}:{lineno_}</code> <b>in</b>"
                f" <code>{utils.escape_html(name_)}</code>"
            )

        filename, lineno, name = next(
            (
                line_regex.search(line).groups()
                for line in reversed(full_traceback.splitlines())
                if line_regex.search(line)
            ),
            (None, None, None),
        )

        full_traceback = "\n".join(
            [
                (
                    format_line(line)
                    if line_regex.search(line)
                    else f"<code>{utils.escape_html(line)}</code>"
                )
                for line in full_traceback.splitlines()
            ]
        )

        caller = utils.find_caller(stack or inspect.stack())

        return cls(
            message=override_text(exc_value)
            or (
                "{}<b>🎯 Source:</b> <code>{}:{}</code><b> in"
                " </b><code>{}</code>\n<b>❓ Error:</b> <code>{}</code>{}"
            ).format(
                (
                    (
                        "🔮 <b>Cause: method </b><code>{}</code><b> of"
                        " </b><code>{}</code>\n\n"
                    ).format(
                        utils.escape_html(caller.__name__),
                        utils.escape_html(caller.__self__.__class__.__name__),
                    )
                    if (
                        caller
                        and hasattr(caller, "__self__")
                        and hasattr(caller, "__name__")
                    )
                    else ""
                ),
                utils.escape_html(filename),
                lineno,
                utils.escape_html(name),
                utils.escape_html(
                    "".join(
                        traceback.format_exception_only(exc_type, exc_value)
                    ).strip()
                ),
                (
                    "\n💭 <b>Message:</b>"
                    f" <code>{utils.escape_html(str(comment))}</code>"
                    if comment
                    else ""
                ),
            ),
            full_stack=full_traceback,
            sysinfo=(exc_type, exc_value, tb),
        )


class TelegramLogsHandler(logging.Handler):
    """
    Keeps 2 buffers.
    One for dispatched messages.
    One for unused messages.
    When the length of the 2 together is 100
    truncate to make them 100 together,
    first trimming handled then unused.
    """

    def __init__(self, targets: list, capacity: int):
        super().__init__(0)
        self.buffer = []
        self.handledbuffer = []
        self._queue = []
        self._mods = {}
        self.tg_buff = []
        self.force_send_all = False
        self.tg_level = 20
        self.ignore_common = False
        self.web_debugger = None
        self.targets = targets
        self.capacity = capacity
        self.lvl = logging.NOTSET
        self._send_lock = asyncio.Lock()
        # <--- Добавлены атрибуты для антиспама
        self._recent_errors = {}  # {(client_id, error_type, error_text): (last_time_sent, count)}
        self._error_cooldown = 60  # секунда, через которую можно повторно отправлять ту же ошибку

    def install_tg_log(self, mod: Module):
        if getattr(self, "_task", False):
            self._task.cancel()

        self._mods[mod.tg_id] = mod

        if mod.db.get(__name__, "debugger", False):
            self.web_debugger = WebDebugger()

        self._task = asyncio.ensure_future(self.queue_poller())

    async def queue_poller(self):
        while True:
            with contextlib.suppress(Exception):
                await self.sender()
            await asyncio.sleep(3)

    def setLevel(self, level: int):
        self.lvl = level

    def dump(self):
        """Return a list of logging entries"""
        return self.handledbuffer + self.buffer

    def dumps(
        self,
        lvl: int = 0,
        client_id: typing.Optional[int] = None,
    ) -> typing.List[str]:
        """Return all entries of minimum level as list of strings"""
        return [
            self.targets[0].format(record)
            for record in (self.buffer + self.handledbuffer)
            if record.levelno >= lvl
            and (not record.hikka_caller or client_id == record.hikka_caller)
        ]

    async def _show_full_trace(
        self,
        call: BotInlineCall,
        bot: "aiogram.Bot",  # type: ignore  # noqa: F821
        item: HikkaException,
    ):
        # <--- Изменена логика для добавления счетчика повторов
        repeat_text = (
            f"\n\n💭 <i>This same error repeated {item.repeat_count} times</i>"
            if item.repeat_count > 0
            else ""
        )
        
        chunks = item.message + repeat_text + "\n\n<b>⛄ Full traceback:</b>\n" + item.full_stack

        chunks = list(utils.smart_split(*lidfaxtl.extensions.html.parse(chunks), 4096))

        await call.edit(
            chunks[0],
            reply_markup=self._gen_web_debug_button(item),
        )

        for chunk in chunks[1:]:
            await bot.send_message(chat_id=call.chat_id, text=chunk)

    def _gen_web_debug_button(self, item: HikkaException) -> list:
        if not item.sysinfo:
            return []

        if not (url := item.debug_url):
            try:
                url = self.web_debugger.feed(*item.sysinfo)
            except Exception:
                url = None

            item.debug_url = url

        return [
            (
                {
                    "text": "🐞 Web debugger",
                    "url": url,
                }
                if self.web_debugger
                else {
                    "text": "🪲 Start debugger",
                    "callback": self._start_debugger,
                    "args": (item,),
                }
            )
        ]

    async def _start_debugger(
        self,
        call: "InlineCall",  # type: ignore  # noqa: F821
        item: HikkaException,
    ):
        if not self.web_debugger:
            self.web_debugger = WebDebugger()
            await self.web_debugger.proxy_ready.wait()

        url = self.web_debugger.feed(*item.sysinfo)
        item.debug_url = url

        await call.edit(
            item.message,
            reply_markup=self._gen_web_debug_button(item),
        )

        await call.answer(
            (
                "Web debugger started. You can get PIN using .debugger command. \n⚠️"
                " !DO NOT GIVE IT TO ANYONE! ⚠️"
            ),
            show_alert=True,
        )

    def get_logid_by_client(self, client_id: int) -> int:
        return self._mods[client_id].logchat

    async def sender(self):
        # <--- Добавлена логика для отправки сообщений с накопленным счетчиком ошибок
        # (включая текстовые логи)
        current_tg_buff = []
        current_exc_queue_items = []

        for item, caller in self.tg_buff:
            if isinstance(item, HikkaException):
                # Добавление счетчика повторов к сообщению HikkaException
                if item.repeat_count > 0:
                    item.message += (
                        f"\n\n💭 <i>This same error repeated {item.repeat_count} times</i>"
                    )
                current_exc_queue_items.append((item, caller))
            else:
                current_tg_buff.append((item, caller))

        # Обновление _recent_errors: сбрасываем счетчики для тех ошибок, которые мы сейчас отправляем
        errors_to_remove = []
        for key, (last_time_sent, count) in self._recent_errors.items():
            if time.time() - last_time_sent >= self._error_cooldown:
                errors_to_remove.append(key)
        
        for key in errors_to_remove:
            del self._recent_errors[key]
        
        # Очистка tg_buff и дальнейшая обработка
        self.tg_buff = []


        async with self._send_lock:
            # Логика для обычных текстовых логов
            self._queue = {
                client_id: utils.chunks(
                    utils.escape_html(
                        "".join(
                            [
                                item[0]
                                for item in current_tg_buff
                                if isinstance(item[0], str)
                                and (
                                    not item[1]
                                    or item[1] == client_id
                                    or self.force_send_all
                                )
                            ]
                        )
                    ),
                    4096,
                )
                for client_id in self._mods
            }
            
            # Логика для исключений
            self._exc_queue = {
                client_id: [
                    self._mods[client_id].inline.bot.send_message(
                        self._mods[client_id].logchat,
                        item[0].message,
                        reply_markup=self._mods[client_id].inline.generate_markup(
                            [
                                {
                                    "text": "☃️ Full traceback",
                                    "callback": self._show_full_trace,
                                    "args": (
                                        self._mods[client_id].inline.bot,
                                        item[0],
                                    ),
                                    "disable_security": True,
                                },
                                *self._gen_web_debug_button(item[0]),
                            ],
                        ),
                    )
                    for item in current_exc_queue_items
                    if isinstance(item[0], HikkaException)
                    and (not item[1] or item[1] == client_id or self.force_send_all)
                ]
                for client_id in self._mods
            }

            for exceptions in self._exc_queue.values():
                for exc in exceptions:
                    await exc

            # self.tg_buff = []  <--- Уже очищен

            for client_id in self._mods:
                if client_id not in self._queue:
                    continue

                if len(self._queue[client_id]) > 5:
                    logfile = io.BytesIO(
                        "".join(self._queue[client_id]).encode("utf-8")
                    )
                    logfile.name = "heroku-logs.txt"
                    logfile.seek(0)
                    await self._mods[client_id].inline.bot.send_document(
                        self._mods[client_id].logchat,
                        logfile,
                        caption=(
                            "<b>🧳 Journals are too big to be sent as separate"
                            " messages</b>"
                        ),
                    )

                    self._queue[client_id] = []
                    continue

                while self._queue[client_id]:
                    if chunk := self._queue[client_id].pop(0):
                        asyncio.ensure_future(
                            self._mods[client_id].inline.bot.send_message(
                                self._mods[client_id].logchat,
                                f"<code>{chunk}</code>",
                                disable_notification=True,
                            )
                        )

    def emit(self, record: logging.LogRecord):
        try:
            caller = next(
                (
                    frame_info.frame.f_locals["_hikka_client_id_logging_tag"]
                    for frame_info in inspect.stack()
                    if isinstance(
                        getattr(getattr(frame_info, "frame", None), "f_locals", {}).get(
                            "_hikka_client_id_logging_tag"
                        ),
                        int,
                    )
                ),
                False,
            )

            if not isinstance(caller, int):
                caller = None
        except Exception:
            caller = None

        record.hikka_caller = caller

        if record.levelno >= self.tg_level:
            if record.exc_info:
                exc_type, exc_value, tb = record.exc_info
                
                exc = HikkaException.from_exc_info(
                    exc_type,
                    exc_value,
                    tb,
                    stack=record.__dict__.get("stack", None),
                    comment=record.msg % record.args,
                )
                
                # <--- Логика антиспама для повторяющихся ошибок
                key = (caller, type(exc_value), exc.message)
                current_time = time.time()
                
                if key in self._recent_errors:
                    last_time_sent, count = self._recent_errors[key]
                    
                    if current_time - last_time_sent < self._error_cooldown:
                        # Ошибка повторяется, но не отправляем ее сразу
                        self._recent_errors[key] = (last_time_sent, count + 1)
                        return # Не добавляем в tg_buff
                    else:
                        # Кулер прошел, отправляем, обновляем время и сбрасываем счетчик
                        exc.repeat_count = count
                        self._recent_errors[key] = (current_time, 0)
                else:
                    # Новая ошибка, добавляем ее в recent_errors
                    self._recent_errors[key] = (current_time, 0)
                # <--- Конец логики антиспама

                if not self.ignore_common or all(
                    field not in exc.message
                    for field in [
                        "InputPeerEmpty() does not have any entity type",
                        "https://docs.telethon.dev/en/stable/concepts/entities.html",
                    ]
                ):
                    self.tg_buff += [(exc, caller)]
            else:
                self.tg_buff += [
                    (
                        _tg_formatter.format(record),
                        caller,
                    )
                ]

        if len(self.buffer) + len(self.handledbuffer) >= self.capacity:
            if self.handledbuffer:
                del self.handledbuffer[0]
            else:
                del self.buffer[0]

        self.buffer.append(record)

        if record.levelno >= self.lvl >= 0:
            self.acquire()
            try:
                for precord in self.buffer:
                    for target in self.targets:
                        if record.levelno >= target.level:
                            target.handle(precord)

                self.handledbuffer = (
                    self.handledbuffer[-(self.capacity - len(self.buffer)) :]
                    + self.buffer
                )
                self.buffer = []
            finally:
                self.release()


_main_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    dat
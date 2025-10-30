# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import contextlib
import copy
import functools
import logging
import time
import traceback
import typing

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.exceptions import TelegramRetryAfter
from lidfaxtl.errors.rpcerrorlist import ChatSendInlineForbiddenError
from lidfaxtl.extensions.html import CUSTOM_EMOJIS
from lidfaxtl.tl.types import Message

from .. import main, utils
from ..types import HikkaReplyMarkup
from .types import InlineMessage, InlineUnit

logger = logging.getLogger(__name__)


class List(InlineUnit):
    def _split_text(self, text: str, max_length: int = 4096) -> typing.List[str]:
        """
        Splits text into multiple parts if it exceeds max_length
        
        :param text: text to split
        :param max_length: maximum length per part (default 4096)
        :return: list of text parts
        """
        if len(text) <= max_length:
            return [text]
        
        parts = []
        current_part = ""
        
        # Split by lines to avoid breaking in the middle of a line
        lines = text.split('\n')
        
        for line in lines:
            # If single line is longer than max_length, split it
            if len(line) > max_length:
                # If current_part has content, save it first
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                
                # Split long line into chunks
                while len(line) > max_length:
                    # Try to find space to break at
                    break_point = line.rfind(' ', 0, max_length)
                    if break_point == -1:
                        break_point = max_length
                    
                    parts.append(line[:break_point])
                    line = line[break_point:].lstrip()
                
                if line:
                    current_part = line
            else:
                # Check if adding this line would exceed limit
                if len(current_part) + len(line) + 1 > max_length:
                    parts.append(current_part)
                    current_part = line
                else:
                    if current_part:
                        current_part += '\n' + line
                    else:
                        current_part = line
        
        # Don't forget the last part
        if current_part:
            parts.append(current_part)
        
        return parts

    def _expand_strings(self, strings: typing.List[str]) -> typing.List[str]:
        """
        Expands strings list by splitting long strings into multiple parts
        
        :param strings: original list of strings
        :return: expanded list with long strings split
        """
        expanded = []
        for string in strings:
            parts = self._split_text(string)
            if len(parts) > 1:
                # Add part indicators
                for i, part in enumerate(parts, 1):
                    expanded.append(f"{part}\n\n<i>📄 Part {i}/{len(parts)}</i>")
            else:
                expanded.append(string)
        
        return expanded

    async def list(
        self,
        message: typing.Union[Message, int],
        strings: typing.List[str],
        *,
        force_me: bool = False,
        always_allow: typing.Optional[typing.List[int]] = None,
        manual_security: bool = False,
        disable_security: bool = False,
        ttl: typing.Union[int, bool] = False,
        on_unload: typing.Optional[typing.Callable[[], typing.Any]] = None,
        silent: bool = False,
        custom_buttons: typing.Optional[HikkaReplyMarkup] = None,
    ) -> typing.Union[bool, InlineMessage]:
        """
        Send inline list to chat
        :param message: Where to send list. Can be either `Message` or `int`
        :param strings: List of strings, which should become inline list
        :param force_me: Either this list buttons must be pressed only by owner scope or no
        :param always_allow: Users, that are allowed to press buttons in addition to previous rules
        :param ttl: Time, when the list is going to be unloaded. Unload means, that the list
                    will become unusable. Pay attention, that ttl can't
                    be bigger, than default one (1 day) and must be either `int` or `False`
        :param on_unload: Callback, called when list is unloaded and/or closed. You can clean up trash
                          or perform another needed action
        :param manual_security: By default, Hikka will try to inherit inline buttons security from the caller (command)
                                If you want to avoid this, pass `manual_security=True`
        :param disable_security: By default, Hikka will try to inherit inline buttons security from the caller (command)
                                 If you want to disable all security checks on this list in particular, pass `disable_security=True`
        :param silent: Whether the list must be sent silently (w/o "Opening list..." message)
        :param custom_buttons: Custom buttons to add above native ones
        :return: If list is sent, returns :obj:`InlineMessage`, otherwise returns `False`
        """
        with contextlib.suppress(AttributeError):
            _hikka_client_id_logging_tag = copy.copy(self._client.tg_id)  # noqa: F841

        custom_buttons = self._validate_markup(custom_buttons)

        if not isinstance(manual_security, bool):
            logger.error(
                "Invalid type for `manual_security`. Expected `bool`, got `%s`",
                type(manual_security),
            )
            return False

        if not isinstance(silent, bool):
            logger.error(
                "Invalid type for `silent`. Expected `bool`, got `%s`",
                type(silent),
            )
            return False

        if not isinstance(disable_security, bool):
            logger.error(
                "Invalid type for `disable_security`. Expected `bool`, got `%s`",
                type(disable_security),
            )
            return False

        if not isinstance(message, (Message, int)):
            logger.error(
                "Invalid type for `message`. Expected `Message` or `int`, got `%s`",
                type(message),
            )
            return False

        if not isinstance(force_me, bool):
            logger.error(
                "Invalid type for `force_me`. Expected `bool`, got `%s`",
                type(force_me),
            )
            return False

        if not isinstance(strings, list) or not strings:
            logger.error(
                (
                    "Invalid type for `strings`. Expected `list` with at least one"
                    " element, got `%s`"
                ),
                type(strings),
            )
            return False

        # Expand strings that are too long
        strings = self._expand_strings(strings)

        if len(strings) > 50:
            logger.warning(
                "Too many pages for `strings` (%s), truncating to 50",
                len(strings)
            )
            strings = strings[:50]

        if always_allow and not isinstance(always_allow, list):
            logger.error(
                "Invalid type for `always_allow`. Expected `list`, got `%s`",
                type(always_allow),
            )
            return False

        if not always_allow:
            always_allow = []

        if not isinstance(ttl, int) and ttl:
            logger.error(
                "Invalid type for `ttl`. Expected `int` or `False`, got `%s`",
                type(ttl),
            )
            return False

        unit_id = utils.rand(16)

        perms_map = None if manual_security else self._find_caller_sec_map()

        self._units[unit_id] = {
            "type": "list",
            "caller": message,
            "chat": None,
            "message_id": None,
            "top_msg_id": utils.get_topic(message),
            "uid": unit_id,
            "current_index": 0,
            "strings": strings,
            "future": asyncio.Event(),
            **({"ttl": round(time.time()) + ttl} if ttl else {}),
            **({"force_me": force_me} if force_me else {}),
            **({"disable_security": disable_security} if disable_security else {}),
            **({"on_unload": on_unload} if callable(on_unload) else {}),
            **({"always_allow": always_allow} if always_allow else {}),
            **({"perms_map": perms_map} if perms_map else {}),
            **({"message": message} if isinstance(message, Message) else {}),
            **({"custom_buttons": custom_buttons} if custom_buttons else {}),
        }

        btn_call_data = utils.rand(10)

        self._custom_map[btn_call_data] = {
            "handler": functools.partial(
                self._list_page,
                unit_id=unit_id,
            ),
            **(
                {"ttl": self._units[unit_id]["ttl"]}
                if "ttl" in self._units[unit_id]
                else {}
            ),
            **({"always_allow": always_allow} if always_allow else {}),
            **({"force_me": force_me} if force_me else {}),
            **({"disable_security": disable_security} if disable_security else {}),
            **({"perms_map": perms_map} if perms_map else {}),
            **({"message": message} if isinstance(message, Message) else {}),
        }

        if isinstance(message, Message) and not silent:
            try:
                status_message = await (
                    message.edit if message.out else message.respond
                )(
                    (
                        utils.get_platform_emoji()
                        if utils.can_use_custom_emojis(self._client)
                        else "☃️"
                    )
                    + self.translator.getkey("inline.opening_list"),
                    **({"reply_to": utils.get_topic(message)} if message.out else {}),
                )
            except Exception:
                status_message = None
        else:
            status_message = None

        async def answer(msg: str):
            nonlocal message
            msg = utils.apply_exteragram_emojis(msg)
            if isinstance(message, Message):
                await (message.edit if message.out else message.respond)(
                    msg,
                    **({} if message.out else {"reply_to": utils.get_topic(message)}),
                )
            else:
                await self._client.send_message(message, msg)

        try:
            m = await self._invoke_unit(unit_id, message)
        except ChatSendInlineForbiddenError:
            await answer(self.translator.getkey("inline.inline403"))
        except Exception:
            logger.exception("Can't send list")

            del self._units[unit_id]
            await answer(
                self.translator.getkey("inline.invoke_failed_logs").format(
                    utils.escape_html(
                        "\n".join(traceback.format_exc().splitlines()[1:])
                    )
                )
                if self._db.get(main.__name__, "inlinelogs", True)
                else self.translator.getkey("inline.invoke_failed")
            )

            return False

        await self._units[unit_id]["future"].wait()
        del self._units[unit_id]["future"]

        self._units[unit_id]["chat"] = utils.get_chat_id(m)
        self._units[unit_id]["message_id"] = m.id
        self._units[unit_id]["inline_message_id"] = getattr(m, "inline_message_id", None)

        if isinstance(message, Message) and message.out:
            await message.delete()

        if status_message and not message.out:
            await status_message.delete()

        # Return appropriate message instance based on message type
        # If inline_message_id exists, it's an inline message (edit via inline_message_id)
        # Otherwise it's a regular bot message (edit via chat_id/message_id)
        if self._units[unit_id]["inline_message_id"]:
            return InlineMessage(self, unit_id, self._units[unit_id]["inline_message_id"])
        else:
            from .types import BotInlineMessage
            return BotInlineMessage(self, unit_id, self._units[unit_id]["chat"], self._units[unit_id]["message_id"])

    async def _list_page(
        self,
        call: CallbackQuery,
        page: typing.Union[int, str],
        unit_id: str = None,
    ):
        if page == "close":
            await self._delete_unit_message(call, unit_id=unit_id)
            return

        if self._units[unit_id]["current_index"] < 0 or page >= len(
            self._units[unit_id]["strings"]
        ):
            await call.answer("Can't go to this page", show_alert=True)
            return

        self._units[unit_id]["current_index"] = page

        try:
            await self.bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text=self.sanitise_text(
                    self._units[unit_id]["strings"][
                        self._units[unit_id]["current_index"]
                    ]
                ),
                reply_markup=self._list_markup(unit_id),
            )
            await call.answer()
        except TelegramRetryAfter as e:
            wait_time = getattr(e, "retry_after", getattr(e, "timeout", 1))
            await call.answer(
                f"Got FloodWait. Wait for {wait_time} seconds",
                show_alert=True,
            )
        except Exception:
            logger.exception("Exception while trying to edit list")
            await call.answer("Error occurred", show_alert=True)
            return

    def _list_markup(self, unit_id: str) -> InlineKeyboardMarkup:
        """Generates aiogram markup for `list`"""
        callback = functools.partial(self._list_page, unit_id=unit_id)
        return self.generate_markup(
            self._units[unit_id].get("custom_buttons", [])
            + self.build_pagination(
                callback=callback,
                total_pages=len(self._units[unit_id]["strings"]),
                unit_id=unit_id,
            )
            + [[{"text": "🔻 Close", "callback": callback, "args": ("close",)}]],
        )

    async def _list_inline_handler(self, inline_query: InlineQuery):
        try:
            query = inline_query.query.split()[0]
        except IndexError:
            query = inline_query.query
        
        # Check if query is a switch_query for input buttons
        for unit_id, unit in self._units.copy().items():
            if unit.get("type") != "list":
                continue
            
            custom_buttons = unit.get("custom_buttons", [])
            if not isinstance(custom_buttons, list):
                continue
                
            for button in utils.array_sum(custom_buttons):
                if not isinstance(button, dict):
                    continue
                    
                if (
                    button.get("_switch_query") == query
                    and "input" in button
                    and inline_query.from_user.id
                    in [self._me]
                    + self._client.dispatcher.security._owner
                    + unit.get("always_allow", [])
                ):
                    await inline_query.answer(
                        [
                            InlineQueryResultArticle(
                                id=utils.rand(20),
                                title=button.get("input", "Enter value"),
                                description=inline_query.query.split(maxsplit=1)[1]
                                if len(inline_query.query.split()) > 1
                                else "Click to submit",
                                input_message_content=InputTextMessageContent(
                                    message_text="🌘 <i>Inline input processing...</i>",
                                    parse_mode="HTML",
                                ),
                            )
                        ],
                        cache_time=0,
                    )
                    return
        
        for unit in self._units.copy().values():
            if (
                inline_query.from_user.id == self._me
                and inline_query.query == unit["uid"]
                and unit["type"] == "list"
            ):
                try:
                    await inline_query.answer(
                        [
                            InlineQueryResultArticle(
                                id=utils.rand(20),
                                title="Hikka",
                                input_message_content=InputTextMessageContent(
                                    message_text=self.sanitise_text(unit["strings"][0]),
                                    parse_mode="HTML",
                                    disable_web_page_preview=True,
                                ),
                                reply_markup=self._list_markup(inline_query.query),
                            )
                        ],
                        cache_time=60,
                    )
                except Exception as e:
                    if unit["uid"] in self._error_events:
                        self._error_events[unit["uid"]].set()
                        self._error_events[unit["uid"]] = e
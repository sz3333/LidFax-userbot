# ©️ Dan Gazizullin, 2021-2023
# Modified by LidF1x
# 🌐 https://github.com/hikariatama/Hikka
# Licensed under the AGPLv3

import contextlib
import copy
import logging
import os
import random
import time
import traceback
import typing
from asyncio import Event
from urllib.parse import urlparse

import grapheme
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultDocument,
    InlineQueryResultGif,
    InlineQueryResultLocation,
    InlineQueryResultPhoto,
    InlineQueryResultVideo,
    InputTextMessageContent,
)
from lidfaxtl.errors.rpcerrorlist import ChatSendInlineForbiddenError
from lidfaxtl.extensions.html import CUSTOM_EMOJIS
from lidfaxtl.tl.types import Message

from .. import main, utils
from ..types import HikkaReplyMarkup
from .types import InlineMessage, InlineUnit

logger = logging.getLogger(__name__)

class Placeholder:
    """Placeholder"""

VERIFICATION_EMOJIES = list(
    grapheme.graphemes("🐱🐾🌸🐈🐕🦊🐇🐿🐦🐥🐉🌈⭐️✨💫🌙🌕☁️🌤☃️🔥🌊🍀🌷🌻🍓🍉🍒🍩🍪🍰🎂🧁🍫🍭🎈🎀🪩🎮🎧")
)

class Form(InlineUnit):
    async def form(
        self,
        text: str,
        message: typing.Union[Message, int],
        reply_markup: typing.Optional[HikkaReplyMarkup] = None,
        *,
        force_me: bool = False,
        always_allow: typing.Optional[typing.List[int]] = None,
        manual_security: bool = False,
        disable_security: bool = False,
        ttl: typing.Optional[int] = None,
        on_unload: typing.Optional[callable] = None,
        photo: typing.Optional[str] = None,
        gif: typing.Optional[str] = None,
        file: typing.Optional[str] = None,
        mime_type: typing.Optional[str] = None,
        video: typing.Optional[str] = None,
        location: typing.Optional[str] = None,
        audio: typing.Optional[typing.Union[dict, str]] = None,
        silent: bool = False,
    ) -> typing.Union[InlineMessage, bool]:
        with contextlib.suppress(AttributeError):
            _hikka_client_id_logging_tag = copy.copy(self._client.tg_id)

        if reply_markup is None:
            reply_markup = []
        if always_allow is None:
            always_allow = []

        if not isinstance(text, str):
            logger.error("Invalid type for `text`")
            return False

        text = self.sanitise_text(text)

        if photo:
            try:
                path = urlparse(photo).path
                ext = os.path.splitext(path)[1]
                if ext in {".gif", ".mp4"}:
                    gif = copy.copy(photo)
                    photo = None
            except Exception:
                pass

        if isinstance(audio, str):
            audio = {"url": audio}

        unit_id = utils.rand(16)
        perms_map = None if manual_security else self._find_caller_sec_map()

        self._units[unit_id] = {
            "type": "form",
            "text": text,
            "buttons": reply_markup,
            "caller": message,
            "chat": None,
            "message_id": None,
            "uid": unit_id,
            "on_unload": on_unload,
            "future": Event(),
            **({"photo": photo} if photo else {}),
            **({"video": video} if video else {}),
            **({"gif": gif} if gif else {}),
            **({"gif_thumb": gif} if gif else {}),
            **({"file": file} if file else {}),
            **({"mime_type": mime_type} if mime_type else {}),
            **({"audio": audio} if audio else {}),
            **({"location": location} if location else {}),
            **({"perms_map": perms_map} if perms_map else {}),
            **({"message": message} if isinstance(message, Message) else {}),
            **({"force_me": force_me} if force_me else {}),
            **({"disable_security": disable_security} if disable_security else {}),
            **({"ttl": round(time.time()) + ttl} if ttl else {}),
            **({"always_allow": always_allow} if always_allow else {}),
        }

        try:
            m = await self._invoke_unit(unit_id, message)
        except ChatSendInlineForbiddenError:
            return False
        except Exception:
            logger.exception("Can't send form")
            return False

        await self._units[unit_id]["future"].wait()
        del self._units[unit_id]["future"]

        self._units[unit_id]["chat"] = utils.get_chat_id(m)
        self._units[unit_id]["message_id"] = m.id
        self._units[unit_id]["inline_message_id"] = getattr(m, "inline_message_id", None)  # 💫 фикс для кнопок

        return InlineMessage(self, unit_id, self._units[unit_id]["inline_message_id"])

    async def _form_inline_handler(self, inline_query: InlineQuery):
        try:
            query = inline_query.query.split()[0]
        except IndexError:
            return

        if (
            inline_query.query not in self._units
            or self._units[inline_query.query]["type"] != "form"
        ):
            return

        form = self._units[inline_query.query]
        try:
            if "photo" in form:
                await inline_query.answer(
                    [
                        InlineQueryResultPhoto(
                            id=utils.rand(20),
                            title="Hikka",
                            caption=form.get("text"),
                            parse_mode="HTML",
                            photo_url=form["photo"],
                            thumbnail_url="https://img.icons8.com/cotton/452/moon-satellite.png",
                            reply_markup=self.generate_markup(form["uid"])
                            if hasattr(self, "generate_markup")
                            else None,
                        )
                    ],
                    cache_time=0,
                )
            elif "gif" in form:
                await inline_query.answer(
                    [
                        InlineQueryResultGif(
                            id=utils.rand(20),
                            title="Hikka",
                            caption=form.get("text"),
                            parse_mode="HTML",
                            gif_url=form["gif"],
                            thumbnail_url=(
                                form.get("gif_thumb")
                                or "https://img.icons8.com/cotton/452/moon-satellite.png"
                            ),
                            reply_markup=self.generate_markup(form["uid"])
                            if hasattr(self, "generate_markup")
                            else None,
                        )
                    ],
                    cache_time=0,
                )
            elif "video" in form:
                await inline_query.answer(
                    [
                        InlineQueryResultVideo(
                            id=utils.rand(20),
                            title="Hikka",
                            caption=form.get("text"),
                            parse_mode="HTML",
                            video_url=form["video"],
                            thumbnail_url="https://img.icons8.com/cotton/452/moon-satellite.png",
                            mime_type="video/mp4",
                            reply_markup=self.generate_markup(form["uid"])
                            if hasattr(self, "generate_markup")
                            else None,
                        )
                    ],
                    cache_time=0,
                )
            elif "file" in form:
                await inline_query.answer(
                    [
                        InlineQueryResultDocument(
                            id=utils.rand(20),
                            title="Hikka",
                            caption=form.get("text"),
                            parse_mode="HTML",
                            document_url=form["file"],
                            mime_type=form.get("mime_type", "application/zip"),
                            reply_markup=self.generate_markup(form["uid"])
                            if hasattr(self, "generate_markup")
                            else None,
                        )
                    ],
                    cache_time=0,
                )
            elif "audio" in form:
                await inline_query.answer(
                    [
                        InlineQueryResultAudio(
                            id=utils.rand(20),
                            audio_url=form["audio"]["url"],
                            caption=form.get("text"),
                            parse_mode="HTML",
                            title=form["audio"].get("title", "Hikka"),
                            performer=form["audio"].get("performer"),
                            audio_duration=form["audio"].get("duration"),
                            reply_markup=self.generate_markup(form["uid"])
                            if hasattr(self, "generate_markup")
                            else None,
                        )
                    ],
                    cache_time=0,
                )
            else:
                await inline_query.answer(
                    [
                        InlineQueryResultArticle(
                            id=utils.rand(20),
                            title="Hikka",
                            input_message_content=InputTextMessageContent(
                                message_text=form["text"],
                                parse_mode="HTML",
                                disable_web_page_preview=True,
                            ),
                            reply_markup=self.generate_markup(inline_query.query)
                            if hasattr(self, "generate_markup")
                            else None,
                        )
                    ],
                    cache_time=0,
                )
        except Exception as e:
            logger.warning(f"Inline form error: {e}")
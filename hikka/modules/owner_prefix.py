# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import logging
from hikkatl.tl.types import Message
from hikkatl.utils import get_display_name

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class OwnerPrefixMod(loader.Module):
    """Custom prefix management for owners"""

    strings = {"name": "OwnerPrefix"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "allow_owner_custom_prefix",
                True,
                "Allow owners to set custom prefixes",
                validator=loader.validators.Boolean(),
            ),
        )

    async def client_ready(self):
        # Initialize owner prefixes storage
        if not hasattr(self, "_owner_prefixes"):
            self._owner_prefixes = self._db.get(main.__name__, "owner_prefixes", {})

    def is_owner(self, user_id: int) -> bool:
        """Check if user is owner"""
        return user_id in self._client.dispatcher.security.owner

    def get_owner_prefix(self, user_id: int) -> str:
        """Get custom prefix for owner"""
        return self._owner_prefixes.get(str(user_id), "")

    def set_owner_prefix(self, user_id: int, prefix: str) -> bool:
        """Set custom prefix for owner"""
        if not self.is_owner(user_id):
            return False
        
        if prefix:
            self._owner_prefixes[str(user_id)] = prefix
        else:
            self._owner_prefixes.pop(str(user_id), None)
        
        self._db.set(main.__name__, "owner_prefixes", self._owner_prefixes)
        return True

    @loader.command()
    async def sprefix(self, message: Message):
        """Set custom prefix for owner"""
        if not self.config["allow_owner_custom_prefix"]:
            await utils.answer(message, self.strings("feature_disabled_notice"))
            return

        if not self.is_owner(message.sender_id):
            await utils.answer(message, self.strings("not_owner"))
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("what_prefix"))
            return

        if len(args) > 10:  # Limit prefix length
            await utils.answer(message, self.strings("prefix_too_long"))
            return

        # Check if prefix contains only valid characters
        if not all(ord(c) < 128 for c in args):  # Only ASCII characters
            await utils.answer(message, self.strings("invalid_prefix"))
            return

        old_prefix = self.get_owner_prefix(message.sender_id)
        
        if self.set_owner_prefix(message.sender_id, args):
            await utils.answer(
                message,
                self.strings("prefix_set").format(
                    new_prefix=utils.escape_html(args),
                    old_prefix=utils.escape_html(old_prefix) if old_prefix else self.strings("none"),
                ),
            )
        else:
            await utils.answer(message, self.strings("failed_to_set"))

    @loader.command()
    async def rprefix(self, message: Message):
        """Remove custom prefix for owner"""
        if not self.config["allow_owner_custom_prefix"]:
            await utils.answer(message, self.strings("feature_disabled_notice"))
            return

        if not self.is_owner(message.sender_id):
            await utils.answer(message, self.strings("not_owner"))
            return

        old_prefix = self.get_owner_prefix(message.sender_id)
        
        if not old_prefix:
            await utils.answer(message, self.strings("no_custom_prefix"))
            return

        if self.set_owner_prefix(message.sender_id, ""):
            await utils.answer(
                message,
                self.strings("prefix_removed").format(
                    old_prefix=utils.escape_html(old_prefix)
                ),
            )
        else:
            await utils.answer(message, self.strings("failed_to_remove"))

    @loader.command()
    async def mprefix(self, message: Message):
        """Show current custom prefix for owner"""
        if not self.is_owner(message.sender_id):
            await utils.answer(message, self.strings("not_owner"))
            return

        current_prefix = self.get_owner_prefix(message.sender_id)
        default_prefix = self.get_prefix()
        
        if current_prefix:
            await utils.answer(
                message,
                self.strings("current_prefix").format(
                    custom_prefix=utils.escape_html(current_prefix),
                    default_prefix=utils.escape_html(default_prefix),
                ),
            )
        else:
            await utils.answer(
                message,
                self.strings("no_custom_prefix_set").format(
                    default_prefix=utils.escape_html(default_prefix)
                ),
            )

    @loader.command()
    async def prefixes(self, message: Message):
        """List all owner custom prefixes (only for owners)"""
        if not self.is_owner(message.sender_id):
            await utils.answer(message, self.strings("not_owner"))
            return

        if not self._owner_prefixes:
            await utils.answer(message, self.strings("no_owner_prefixes"))
            return

        prefixes_list = []
        for user_id_str, prefix in self._owner_prefixes.items():
            try:
                user_id = int(user_id_str)
                user = await self._client.get_entity(user_id)
                user_name = get_display_name(user)
                prefixes_list.append(
                    f"▫️ <b><a href='tg://user?id={user_id}'>{utils.escape_html(user_name)}</a></b>: "
                    f"<code>{utils.escape_html(prefix)}</code>"
                )
            except Exception:
                # Remove invalid user IDs
                self._owner_prefixes.pop(user_id_str, None)
                continue

        if not prefixes_list:
            await utils.answer(message, self.strings("no_owner_prefixes"))
            return

        self._db.set(main.__name__, "owner_prefixes", self._owner_prefixes)
        
        await utils.answer(
            message,
            self.strings("owner_prefixes_list").format("\n".join(prefixes_list))
        )

    async def inline__toggle_feature(self, call: InlineCall):
        """Toggle owner custom prefix feature"""
        if not self.is_owner(call.from_user.id):
            await call.answer(self.strings("not_owner"), show_alert=True)
            return

        self.config["allow_owner_custom_prefix"] = not self.config["allow_owner_custom_prefix"]
        await call.answer("✅")
        
        await call.edit(
            self.strings("feature_settings"),
            reply_markup=self._get_feature_markup(),
        )

    def _get_feature_markup(self) -> list:
        return [
            [
                {
                    "text": (
                        "✅ " + self.strings("feature_enabled")
                        if self.config["allow_owner_custom_prefix"]
                        else "🚫 " + self.strings("feature_disabled")
                    ),
                    "callback": self.inline__toggle_feature,
                }
            ],
            [{"text": self.strings("close_menu"), "action": "close"}],
        ]

    @loader.command()
    async def ownerprefixsettings(self, message: Message):
        """Open owner prefix settings"""
        if not self.is_owner(message.sender_id):
            await utils.answer(message, self.strings("not_owner"))
            return

        await self.inline.form(
            self.strings("feature_settings"),
            message=message,
            reply_markup=self._get_feature_markup(),
        )

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import git
from hikkatl.tl.types import Message
from hikkatl.utils import get_display_name
import requests
import os
from .. import loader, utils, version
from ..inline.types import InlineQuery
import platform as lib_platform
import getpass

@loader.tds
class LidFaxInfoMod(loader.Module):
    """Show userbot info"""

    strings = {"name": "LidFaxInfo"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                doc=lambda: self.strings("_cfg_cst_msg"),
            ),

            loader.ConfigValue(
                "banner_url",
                "https://x0.at/wGb3.mp4",
                lambda: self.strings("_cfg_banner"),
            ),
            
            loader.ConfigValue(
                "pp_to_banner",
                False,
                validator=loader.validators.Boolean(),
            ),

            loader.ConfigValue(
                "show_lidfax",
                True,
                validator=loader.validators.Boolean(),
            ),
        )

    def _render_info(self, inline: bool) -> str:
        try:
            repo = git.Repo(search_parent_directories=True)
            diff = repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
            upd = (
                self.strings("update_required") if diff else self.strings("up-to-date")
            )
        except Exception:
            upd = ""

        me = '<b><a href="tg://user?id={}">{}</a></b>'.format(
            self._client.hikka_me.id,
            utils.escape_html(get_display_name(self._client.hikka_me)),
        )
        build = utils.get_commit_url()
        _version = f'<i>{".".join(list(map(str, list(version.__version__))))}</i>'
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"

        platform = utils.get_named_platform()

        for emoji, icon in [
            ("🍊", "<emoji document_id=5449599833973203438>🧡</emoji>"),
            ("🍇", "<emoji document_id=5449468596952507859>💜</emoji>"),
            ("😶‍🌫️", "<emoji document_id=5370547013815376328>😶‍🌫️</emoji>"),
            ("❓", "<emoji document_id=5407025283456835913>📱</emoji>"),
            ("🍀", "<emoji document_id=5395325195542078574>🍀</emoji>"),
            ("🦾", "<emoji document_id=5386766919154016047>🦾</emoji>"),
            ("🚂", "<emoji document_id=5359595190807962128>🚂</emoji>"),
            ("🐳", "<emoji document_id=5431815452437257407>🐳</emoji>"),
            ("🕶", "<emoji document_id=5407025283456835913>📱</emoji>"),
            ("🐈‍⬛", "<emoji document_id=6334750507294262724>🐈‍⬛</emoji>"),
            ("✌️", "<emoji document_id=5469986291380657759>✌️</emoji>"),
            ("💎", "<emoji document_id=5471952986970267163>💎</emoji>"),
            ("🛡", "<emoji document_id=5282731554135615450>🌩</emoji>"),
            ("💘", "<emoji document_id=5452140079495518256>💘</emoji>"),
            ("🌼", "<emoji document_id=5224219153077914783>❤️</emoji>"),
            ("🎡", "<emoji document_id=5226711870492126219>🎡</emoji>"),
            ("🐧", "<emoji document_id=5361541227604878624>🐧</emoji>")
        ]:
            platform = platform.replace(emoji, icon)
        return (
            (
                "<b>☃️ LidFax</b>\n"
                if self.config["show_lidfax"]
                else ""
            )
            + self.config["custom_message"].format(
                me=me,
                version=_version,
                build=build,
                prefix=prefix,
                platform=platform,
                upd=upd,
                uptime=utils.formatted_uptime(),
                cpu_usage=utils.get_cpu_usage(),
                ram_usage=f"{utils.get_ram_usage()} MB",
                branch=version.branch,
                hostname=lib_platform.node(),
                user=getpass.getuser(),
            )
            if self.config["custom_message"]
            else (
                f'<b>{{}}</b>\n\n<b>{{}} {self.strings("owner")}:</b> {me}\n\n<b>{{}}'
                f' {self.strings("version")}:</b> {_version} {build}\n<b>{{}}'
                f' {self.strings("branch")}:'
                f"</b> <code>{version.branch}</code>\n{upd}\n\n<b>{{}}"
                f' {self.strings("prefix")}:</b> {prefix}\n<b>{{}}'
                f' {self.strings("uptime")}:'
                f"</b> {utils.formatted_uptime()}\n\n<b>{{}}"
                f' {self.strings("cpu_usage")}:'
                f"</b> <i>~{utils.get_cpu_usage()} %</i>\n<b>{{}}"
                f' {self.strings("ram_usage")}:'
                f"</b> <i>~{utils.get_ram_usage()} MB</i>\n<b>{{}}</b>"
            ).format(
                *map(
                    lambda x: utils.remove_html(x) if inline else x,
                    (
                        (
                            utils.get_platform_emoji()
                            if self._client.hikka_me.premium and self.config["show_lidfax"]
                            else ""
                        ),
                        "<emoji document_id=5373141891321699086>😎</emoji>",
                        "<emoji document_id=5469741319330996757>💫</emoji>",
                        "<emoji document_id=5449918202718985124>🌳</emoji>",
                        "<emoji document_id=5472111548572900003>⌨️</emoji>",
                        "<emoji document_id=5451646226975955576>⌛️</emoji>",
                        "<emoji document_id=5431449001532594346>⚡️</emoji>",
                        "<emoji document_id=5359785904535774578>💼</emoji>",
                        platform,
                    ),
                )
            )
        )

    async def upload_pp_to_oxo(self, photo):
        save_path = "profile_photo.jpg"
        await self._client.download_media(photo, file=save_path)

        try:
            with open(save_path, 'rb') as file:
                oxo = await utils.run_sync(
                    requests.post,
                    "https://0x0.st",
                    files={"file": file},
                    data={"secret": True},
                )

            if oxo.status_code == 200:
                return oxo.text.strip()
            else:
                return "https://x0.at/wGb3.mp4"

        except Exception:
            return "https://x0.at/wGb3.mp4"

        finally:
            if os.path.exists(save_path):
                os.remove(save_path)

    async def get_pp_for_banner(self):
        photos = await self._client.get_profile_photos('me')
        if photos:
            return await self.upload_pp_to_oxo(photos[0])
        return "https://x0.at/wGb3.mp4"

    async def info(self, _: InlineQuery) -> dict:
        """Send userbot info"""

        return {
            "title": self.strings("send_info"),
            "description": self.strings("description"),
            **(
                {"photo": self.config["banner_url"], "caption": self._render_info(True)}
                if self.config["banner_url"]
                else {"message": self._render_info(True)}
            ),
            "thumb": (
                "https://github.com/hikariatama/Hikka/raw/master/assets/hikka_pfp.png"
            ),
            "reply_markup": self._get_mark(),
        }

    @loader.command()
    async def infocmd(self, message: Message):
        if self.config.get('pp_to_banner', True):
            print(self.config['banner_url'])
            try:
                new_banner_url = await self.get_pp_for_banner()
                if new_banner_url:
                    self.config['banner_url'] = new_banner_url
                    await self._db.set("Config", "banner_url", new_banner_url)
            except Exception:
                pass
        await utils.answer_file(
            message,
            self.config["banner_url"],
            self._render_info(False),
        )

    @loader.command()
    async def lidfaxinfo(self, message: Message):
        await utils.answer(message, self.strings("desc"))

    @loader.command()
    async def setinfo(self, message: Message):
        if not (args := utils.get_args_html(message)):
            return await utils.answer(message, self.strings("setinfo_no_args"))

        self.config["custom_message"] = args
        await utils.answer(message, self.strings("setinfo_success"))


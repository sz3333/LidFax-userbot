# ©️ LidF1x, 2025
# This file is a part of LidFax Userbot
# 🌐 https://github.com/sz3333/LidFax-userbot
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html


import logging
import platform
import re
import sys
import aiohttp
from datetime import datetime
from .. import utils
from .. import loader
from ..inline.types import BotInlineCall

logger = logging.getLogger(__name__)


@loader.tds
class LidFaxAnalytics(loader.Module):
    strings = {"name": "LidFaxAnalytics"}
    
    _analytics_url = "https://lidapi.onrender.com/api/analytics"

    async def client_ready(self):
        if self.get("analytics_sent"):
            return

        analytics_data = await self._collect_analytics()
        
        try:
            analytics_id = await self._send_analytics(analytics_data)
            self.set("analytics_id", analytics_id)
            await self._show_analytics_prompt(analytics_id)
            logger.info(f"Analytics sent, ID: {analytics_id}")
        except Exception as e:
            logger.warning(f"Analytics send failed: {e}")

        self.set("analytics_sent", True)

    async def _show_analytics_prompt(self, analytics_id):
        markup = [
            [
                {
                    "text": self.strings("btn_keep"),
                    "callback": self._keep_analytics,
                },
                {
                    "text": self.strings("btn_delete"),
                    "callback": self._delete_analytics,
                    "args": (analytics_id,),
                },
            ]
        ]

        await self.inline.bot.send_message(
            self._client.tg_id,
            self.strings("analytics_sent"),
            reply_markup=self.inline.generate_markup(markup),
        )

    async def _keep_analytics(self, call: BotInlineCall):
        await call.edit(self.strings("analytics_kept"))
        logger.info("Analytics kept")

    async def _delete_analytics(self, call: BotInlineCall, analytics_id: int):
        try:
            await self._remove_analytics(analytics_id)
            await call.edit(self.strings("analytics_deleted"))
            logger.info(f"Analytics deleted, ID: {analytics_id}")
        except Exception as e:
            await call.edit(f"❌ {e}")
            logger.warning(f"Analytics delete failed: {e}")

    async def _collect_analytics(self) -> dict:
        platform_name = utils.get_platform_name()
        hosting = re.sub(r'[^\w\s-]', '', platform_name).strip().lower()
        hosting = re.sub(r'\s+', '_', hosting)
        
        data = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "hosting": hosting,
            "timestamp": datetime.utcnow().isoformat(),
        }

        return data

    async def _send_analytics(self, data: dict) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._analytics_url,
                json=data,
                timeout=aiohttp.ClientTimeout(total=10),
                headers={"Content-Type": "application/json"},
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("id")
                else:
                    raise Exception(f"Server returned {response.status}")

    async def _remove_analytics(self, analytics_id: int):
        url = self._analytics_url.rstrip("/analytics") + f"/analytics/{analytics_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status != 200:
                    raise Exception(f"Server returned {response.status}")

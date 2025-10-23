import sys
import traceback
import html
import time
import lidfaxtl
import asyncio
import logging

from meval import meval
from io import StringIO

from .. import loader, utils
from ..log import HikkaException

logger = logging.getLogger(__name__)

@loader.tds
class Executor(loader.Module):
    """Выполнение python кода"""

    strings = {
        "name": "Executor",
        "no_code": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть </b><code>{}exec [python код]</code>",
        "executing": "<b><emoji document_id=5332600281970517875>🔄</emoji> Выполняю код...</b>",
        "no_phone": "Скрывает твой номер телефона при выводе",
        "result_no_error": '✅ <b>Результат:</b>\n<pre><code class="language-python">{result}</code></pre>\n',
        "result_error": '🚫 <b>Ошибка:</b>\n<pre><code class="language-python">{result}</code></pre>\n',
        "res_return": '💾 <b>Код вернул:</b>\n<pre><code class="language-python">{res}</code></pre>\n',
        "result": '<b>💻 <b>Код:</b>\n<pre><code class="language-python">{code}</code></pre>\n{result}⏳ <b>Выполнен за {time} сек</b></b>',
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "hide_phone",
                True,
                lambda: self.strings["no_phone"],
                validator=loader.validators.Boolean()
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    async def cexecute(self, code, message, reply):
        client = self.client
        me = await client.get_me()
        reply = await message.get_reply_message()
        
        input_data = []
        
        async def ainput(prompt=""):
            nonlocal input_data
            if prompt:
                await utils.answer(message, f"<b>📥 Input:</b> {html.escape(prompt)}")
            else:
                await utils.answer(message, "<b>📥 Ожидаю ввода...</b>")
            
            response = await client.wait_for(
                lidfaxtl.events.NewMessage(
                    chats=message.chat_id,
                    from_users=message.sender_id
                ),
                timeout=60
            )
            
            user_input = response.message.message
            input_data.append(user_input)
            return user_input
        
        functions = {
            "message": message,
            "client": self._client,
            "reply": reply,
            "r": reply,
            "event": message,
            "chat": message.to_id,
            "me": me,
            "lidfaxtl": lidfaxtl,
            "telethon": lidfaxtl,
            "utils": utils,
            "loader": loader,
            "f": lidfaxtl.tl.functions,
            "c": self._client,
            "m": message,
            "lookup": self.lookup,
            "self": self,
            "db": self.db,
            "input": ainput,
        }
        result = sys.stdout = StringIO()
        
        _globals = {k: v for k, v in globals().items() if k != 'input'}
        
        try:
            res = await meval(
                code,
                _globals,
                **functions,
            )
        except:
            return traceback.format_exc().strip(), None, True
        return result.getvalue().strip(), res, False

    @loader.command()
    async def execcmd(self, message):
        """Выполнить python код"""

        code = utils.get_args_raw(message)
        if not code:
            return await utils.answer(message, self.strings["no_code"].format(self.get_prefix()))

        await utils.answer(message, self.strings["executing"])

        reply = await message.get_reply_message()

        start_time = time.perf_counter()
        result, res, cerr = await self.cexecute(code, message, reply)
        stop_time = time.perf_counter()

        me = await self.client.get_me()

        result = str(result)
        res = str(res)

        if self.config['hide_phone']:
            t_h = "never gonna give you up"

            if result:
                result = result.replace("+"+me.phone, t_h).replace(me.phone, t_h)
            if res:
                res = res.replace("+"+me.phone, t_h).replace(me.phone, t_h)

        if result:
            if not cerr:
                result = self.strings["result_no_error"].format(result=result)
            else:
                result = self.strings["result_error"].format(result=result)

        if res or res == 0 or res == False and res is not None:
            result += self.strings["res_return"].format(res=res)

        return await utils.answer(message, self.strings["result"].format(code=code, result=result, time=round(stop_time - start_time, 5)))

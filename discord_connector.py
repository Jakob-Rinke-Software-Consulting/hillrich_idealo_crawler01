# discord_connector.py
import json
import discord
import asyncio
import threading
import requests
import io
import proxquest.agents as agents
try:
    with open("settings/discord_api_creds.json", "r") as f:
        cfg = json.load(f)
    TOKEN = cfg["token"]
    CHANNEL_ID = int(cfg["all_channel_id"])
    MAIN_CHANNEL_ID = int(cfg["main_channel_id"])
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
except Exception as e:
    print(f"⚠️ Discord config error: {e}")
    client = None

_loop = asyncio.new_event_loop()
_started = threading.Event()


async def _send_message_coro(message: str, image_url: str | None = None, channel="all"):
    if client is None:
        return
    await client.wait_until_ready()
    channelid = CHANNEL_ID if channel == "all" else MAIN_CHANNEL_ID
    channel = client.get_channel(channelid)
    if channel is None:
        try:
            channel = await client.fetch_channel(channelid)
        except Exception as e:
            print(f"Channel nicht gefunden/ladebar: {e}")
            return

    file = None
    if image_url:
        try:
            resp = requests.get(image_url, timeout=10, headers=agents.get_header())
            resp.raise_for_status()
            file = discord.File(io.BytesIO(resp.content), filename="image.jpg")
        except Exception as e:
            print(f"Fehler beim Herunterladen des Bildes: {e}")

    if file:
        await channel.send(content=message, file=file, suppress_embeds=True)
    else:
        await channel.send(content=message, suppress_embeds=True)


def send_message(message: str, image_url: str | None = None, channel="all"):
    if client is None:
        return
    if not _started.is_set():
        _start_thread()
        _started.wait(timeout=2)
    fut = asyncio.run_coroutine_threadsafe(
        _send_message_coro(message, image_url, channel), _loop
    )

    def _log_err(f):
        exc = f.exception()
        if exc:
            print(f"Discord send failed: {exc}")
    fut.add_done_callback(_log_err)

if client is not None:
    @client.event
    async def on_ready():
        if client is None:
            return
        print(f"Logged in as {client.user}")
        await _send_message_coro("Bot (re)-started")


def _runner():
    if client is None:
        return
    asyncio.set_event_loop(_loop)
    _loop.create_task(client.start(TOKEN))
    _started.set()
    _loop.run_forever()


def _start_thread():
    threading.Thread(target=_runner, daemon=True, name="discord-bot").start()


# Autostart
_start_thread()

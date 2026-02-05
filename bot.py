import discord
import os
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# --- [Re-Keep-Alive 區塊] ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- [機器人主體] ---
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ 已登入為：{bot.user.name}')
    # 每 5 分鐘在後台噴一次心跳訊息
    if not heartbeat.is_running():
        heartbeat.start()
    
    try:
        synced = await bot.tree.sync()
        print(f"🌐 已同步 {len(synced)} 個斜線指令")
    except Exception as e:
        print(f"❌ 同步失敗: {e}")

@tasks.loop(minutes=5)
async def heartbeat():
    print("💓 [Re-Check] 系統心跳正常，已維持在線狀態。")

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'🚚 模組載入成功: {filename}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    keep_alive()  # 啟動網頁伺服器
    asyncio.run(main())
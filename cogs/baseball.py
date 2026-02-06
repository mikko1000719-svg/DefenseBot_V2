import discord
from discord import app_commands
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Baseball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="棒球", description="查詢 MLB / CPBL / NPB 比分與排名")
    @app_commands.choices(類別=[
        app_commands.Choice(name="今日比分", value="score"),
        app_commands.Choice(name="聯盟排名", value="rank"),
    ])
    @app_commands.choices(聯盟=[
        app_commands.Choice(name="MLB 大聯盟", value="mlb"),
        app_commands.Choice(name="CPBL 中華職棒", value="cpbl"),
        app_commands.Choice(name="NPB 日本職棒", value="npb"),
    ])
    async def baseball(self, interaction: discord.Interaction, 類別: str, 聯盟: str):
        await interaction.response.defer()
        
        # 這裡以爬取邏輯範例為主，實際 URL 依各官網結構調整
        urls = {
            "mlb": "https://www.espn.com/mlb/scoreboard",
            "cpbl": "https://www.cpbl.com.tw/schedules",
            "npb": "https://baseball.yahoo.co.jp/npb/"
        }
        
        try:
            # 模擬爬蟲判斷 (實務上會用 requests.get)
            current_month = datetime.now().month
            
            # 智慧判斷休賽季 (11月到2月通常沒比賽)
            if current_month in [12, 1, 2]:
                embed = discord.Embed(
                    title=f"⚾ {聯盟.upper()} 賽事資訊",
                    description=f"目前處於 **休賽季** 或 **春訓整備期**。\n暫時沒有正式比賽比分喔！",
                    color=discord.Color.orange()
                )
                await interaction.followup.send(embed=embed)
                return

            # 抓取邏輯 (此處為架構展示)
            embed = discord.Embed(title=f"⚾ {聯盟.upper()} {類別} 報告", color=discord.Color.blue())
            
            if 類別 == "score":
                embed.add_field(name="今日賽況", value="目前暫無即時賽事 (或尚未開賽)", inline=False)
            else:
                embed.add_field(name="排名概況", value="數據獲取中，請點擊下方連結查看詳細排名", inline=False)
                
            embed.add_field(name="官方數據源", value=f"[點我跳轉至 {聯盟.upper()} 官網]({urls[聯盟]})")
            embed.set_footer(text=f"查詢時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"❌ 數據抓取失敗，可能是官網維護中：{e}")

async def setup(bot):
    await bot.add_commands(Baseball(bot)) # 修正為符合最新版本載入
    await bot.add_cog(Baseball(bot))
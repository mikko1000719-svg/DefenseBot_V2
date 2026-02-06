import discord
from discord import app_commands
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import os
import aiohttp
import datetime

# --- 爬蟲核心函數 ---

def get_cpbl_scores():
    """抓取中華職棒即時比分"""
    try:
        url = "https://www.cpbl.com.tw/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        
        # 尋找首頁的比賽區塊
        games = soup.find_all('div', class_='game_item')
        if not games:
            return "⚾ **中職 (CPBL)**: 今日目前無比賽資訊。"
        
        result = "⚾ **中職今日戰況**\n"
        for game in games:
            try:
                # 抓取隊伍名稱與分數
                teams = game.find_all('div', class_='team_name')
                scores = game.find_all('div', class_='score')
                status = game.find('div', class_='game_status') # 比賽狀態 (如：已結束、1局上)
                
                t1, t2 = teams[0].text.strip(), teams[1].text.strip()
                s1, s2 = scores[0].text.strip(), scores[1].text.strip()
                st = status.text.strip() if status else "進行中"
                
                result += f"🔹 {t1} **{s1}** vs **{s2}** {t2} ({st})\n"
            except:
                continue
        return result
    except Exception as e:
        return f"❌ 中職抓取失敗: {e}"

def get_mlb_summary():
    """美職 MLB 簡報 (範例結構)"""
    return "🇺🇸 **美職 MLB**: 請至官網查看最新即時比分 (MLB 結構動態加載，建議串接 API)。"

def get_npb_summary():
    """日職 NPB 簡報 (範例結構)"""
    return "🇯🇵 **日職 NPB**: 今日比賽詳情請見 Yahoo Japan Baseball。"

# --- Discord 指令部分

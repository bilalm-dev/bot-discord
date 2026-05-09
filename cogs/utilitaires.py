import discord
from discord import app_commands
from discord.ext import commands
import requests
import os

class Utilitaires(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meteo", description="Affiche la météo d'une ville")
    async def meteo(self, interaction: discord.Interaction, ville: str):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
        
        response = requests.get(url)
        
        if response.status_code != 200:
            await interaction.response.send_message(f"❌ Ville '{ville}' introuvable.")
            return
        
        data = response.json()
        
        nom = data["name"]
        pays = data["sys"]["country"]
        temp = data["main"]["temp"]
        ressenti = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidite = data["main"]["humidity"]
        vent = data["wind"]["speed"]

        embed = discord.Embed(
            title=f"🌤️ Météo à {nom}, {pays}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🌡️ Température", value=f"{temp}°C (ressenti {ressenti}°C)", inline=False)
        embed.add_field(name="☁️ Conditions", value=description.capitalize(), inline=False)
        embed.add_field(name="💧 Humidité", value=f"{humidite}%", inline=True)
        embed.add_field(name="💨 Vent", value=f"{vent} m/s", inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Affiche les informations du serveur")
    async def info(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = discord.Embed(
            title=f"📊 Informations — {guild.name}",
            color=discord.Color.green()
        )
        embed.add_field(name="👑 Propriétaire", value=guild.owner.mention, inline=False)
        embed.add_field(name="👥 Membres", value=guild.member_count, inline=True)
        embed.add_field(name="📅 Créé le", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="💬 Salons", value=len(guild.channels), inline=True)
        embed.add_field(name="🎭 Rôles", value=len(guild.roles), inline=True)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="aide", description="Affiche la liste des commandes disponibles")
    async def aide(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Commandes ServerMate",
            description="Voici toutes les commandes disponibles :",
            color=discord.Color.purple()
        )
        embed.add_field(name="🌤️ /meteo [ville]", value="Affiche la météo en temps réel", inline=False)
        embed.add_field(name="📊 /info", value="Informations sur le serveur", inline=False)
        embed.add_field(name="🎯 /quiz", value="Lance un quiz aléatoire", inline=False)
        embed.add_field(name="⏰ /rappel [secondes] [message]", value="Crée un rappel personnalisé", inline=False)
        embed.add_field(name="📖 /aide", value="Affiche ce message", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilitaires(bot))
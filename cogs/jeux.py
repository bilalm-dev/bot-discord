import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

QUESTIONS = [
    {
        "question": "Quel langage est utilisé pour le développement web côté client ?",
        "choix": ["Python", "JavaScript", "Java", "C++"],
        "reponse": "JavaScript"
    },
    {
        "question": "Que signifie 'API' ?",
        "choix": ["Application Programming Interface", "Automated Program Integration", "Advanced Python Interface", "Application Process Integration"],
        "reponse": "Application Programming Interface"
    },
    {
        "question": "Quel protocole est utilisé pour les requêtes web ?",
        "choix": ["FTP", "SSH", "HTTP", "SMTP"],
        "reponse": "HTTP"
    },
    {
        "question": "Qu'est-ce qu'un ORM ?",
        "choix": ["Object Relational Mapper", "Online Resource Manager", "Open Runtime Module", "Object Request Model"],
        "reponse": "Object Relational Mapper"
    },
    {
        "question": "Quel outil permet de containeriser une application ?",
        "choix": ["Git", "Docker", "Jenkins", "Nginx"],
        "reponse": "Docker"
    },
    {
        "question": "Que fait la commande 'git commit' ?",
        "choix": ["Envoie le code sur GitHub", "Crée une nouvelle branche", "Enregistre les modifications localement", "Fusionne deux branches"],
        "reponse": "Enregistre les modifications localement"
    },
    {
        "question": "Quel code HTTP signifie 'Not Found' ?",
        "choix": ["200", "401", "500", "404"],
        "reponse": "404"
    },
    {
        "question": "Qu'est-ce que JWT ?",
        "choix": ["Java Web Token", "JSON Web Token", "JavaScript Web Transfer", "JSON Web Transfer"],
        "reponse": "JSON Web Token"
    }
]

class QuizView(discord.ui.View):
    def __init__(self, question_data, user_id):
        super().__init__(timeout=30)
        self.question_data = question_data
        self.user_id = user_id
        self.answered = False

        for choix in question_data["choix"]:
            button = discord.ui.Button(label=choix, style=discord.ButtonStyle.primary)
            button.callback = self.make_callback(choix)
            self.add_item(button)

    def make_callback(self, choix):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(
                    "❌ Ce n'est pas ton quiz !", ephemeral=True
                )
                return
            if self.answered:
                await interaction.response.send_message(
                    "❌ Tu as déjà répondu !", ephemeral=True
                )
                return

            self.answered = True
            for child in self.children:
                child.disabled = True

            if choix == self.question_data["reponse"]:
                await interaction.response.edit_message(
                    content=f"✅ Bonne réponse ! **{choix}** est correct !",
                    view=self
                )
            else:
                await interaction.response.edit_message(
                    content=f"❌ Mauvaise réponse ! La bonne réponse était **{self.question_data['reponse']}**",
                    view=self
                )
        return callback

class Jeux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quiz", description="Lance un quiz aléatoire")
    async def quiz(self, interaction: discord.Interaction):
        question_data = random.choice(QUESTIONS)
        view = QuizView(question_data, interaction.user.id)

        embed = discord.Embed(
            title="🎯 Quiz Tech",
            description=question_data["question"],
            color=discord.Color.gold()
        )
        embed.set_footer(text="Tu as 30 secondes pour répondre !")

        await interaction.response.send_message(embed=embed, view=view)

        await asyncio.sleep(30)
        if not view.answered:
            await interaction.edit_original_response(
                content=f"⏰ Temps écoulé ! La bonne réponse était **{question_data['reponse']}**",
                view=None
            )

    @app_commands.command(name="rappel", description="Crée un rappel personnalisé")
    @app_commands.describe(
        secondes="Dans combien de secondes envoyer le rappel",
        message="Le message du rappel"
    )
    async def rappel(self, interaction: discord.Interaction, secondes: int, message: str):
        if secondes < 1 or secondes > 3600:
            await interaction.response.send_message(
                "❌ La durée doit être entre 1 et 3600 secondes.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"⏰ Rappel configuré ! Je te mentionnerai dans **{secondes} secondes**."
        )

        await asyncio.sleep(secondes)
        await interaction.channel.send(
            f"⏰ {interaction.user.mention} Rappel : **{message}**"
        )

async def setup(bot):
    await bot.add_cog(Jeux(bot))
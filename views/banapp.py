from discord import ButtonStyle
from discord.ui import Button

class BanAppealView(Button):
    def __init__(self):
        super().__init__(
            style=ButtonStyle.url,
            label="Ban Appeal",
            emoji="🔗",
            url="https://nagato.vercel.app/bp.html"
        )
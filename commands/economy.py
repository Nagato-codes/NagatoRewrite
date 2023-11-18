import discord
import json
import time
import random
import asyncio
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown
from utils.nagato import SERVERID

class Economy(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.userdata = self.load_userdata()  # Load userdata from JSON file
        self.items = {
            "apple": {"price": 300, "icon": "🍎"},
            "banana": {"price": 200, "icon": "🍌"},
            "pizza": {"price": 800, "icon": "🍕"},
            "hat": {"price": 600, "icon": "🎩"},
            "sword": {"price": 2500, "icon": "⚔️"},
            "book": {"price": 500, "icon": "📚"},
            "shoes": {"price": 700, "icon": "👟"},
            "guitar": {"price": 1500, "icon": "🎸"},
            "chocolate": {"price": 240, "icon": "🍫"},
            "sunglasses": {"price": 1000, "icon": "🕶️"},
            "ring": {"price": 1200, "icon": "💍"},
            "coffee": {"price": 240, "icon": "☕"},
            "backpack": {"price": 400, "icon": "🎒"},
            "flower": {"price": 80, "icon": "🌸"},
            "umbrella": {"price": 360, "icon": "☔"},
            "potion": {"price": 1200, "icon": "🧪"},
            "camera": {"price": 720, "icon": "📷"},
            "headphones": {"price": 600, "icon": "🎧"},
            "gift": {"price": 800, "icon": "🎁"},
            "teddy bear": {"price": 320, "icon": "🧸"},
            "gloves": {"price": 280, "icon": "🧤"},
            "watch": {"price": 1600, "icon": "⌚"},
            "computer": {"price": 3000, "icon": "💻"},
            "diamond": {"price": 10000, "icon": "💎"},
            "car": {"price": 25000, "icon": "🚗"},
            "house": {"price": 50000, "icon": "🏠"},
            "energy drink": {"price": 100000, "icon": "🥛"},
            "luxury watch": {"price": 200000, "icon": "⌚"},
            "girlfriend": {"price": 1000000, "icon": "👫"},
            "medal": {"price": 2000000, "icon": "🥇"},
            "jet": {"price": 4000000, "icon": "✈️"},
            "yacht": {"price": 6000000, "icon": "⛵"},
            "island": {"price": 10000000, "icon": "🏝️"},
            "Mansion": {"price": 100000000, "icon": "🏚"},
            "island": {"price": 1000000000, "icon": "🚢"},
        }
        self.ITEMS_PER_PAGE = 5

    def load_userdata(self):
        try:
            with open('utils/userdata.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_userdata(self):
        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)
            
    @app_commands.command(name="addacc", description="make your economy account")
    async def addacc(self, interaction:discord.Interaction):
        user_id = str(interaction.user.id)
        if user_id in self.userdata:
            embed = discord.Embed(
                title = "Error",
                description="You already have an account",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        self.userdata[user_id] = {"balance": 0, "last_daily": 0}
        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="New Account",
            description="New Account Created",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="addbal", description="add money to a users account")
    @commands.has_permissions(administrator=True)  # Ensure only admins can use this command
    async def addbal(self, intearaction:discord.Interaction, target_user: discord.User, amount: int):
        target_id = str(target_user.id)

        if target_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="The target user does not have an account.",
                color=discord.Color.random()
            )
            await intearaction.response.send_message(embed=embed)
            return

        self.userdata[target_id]["balance"] += amount

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Balance Added",
            description=f"You added {amount} to {target_user.mention}'s balance.",
            color=discord.Color.random()
        )
        await intearaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="daily money")
    async def daily(self, interaction:discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title = "Error",
                description="You dont have an account run ```?**addacc**`` to create an account",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        if user_id not in self.userdata:    
            self.userdata[user_id] = {"balance": 0, "last_daily": 0}

        last_daily = self.userdata[user_id]["last_daily"]
        current_time = int(time.time())

        if current_time - last_daily < 86400:
            time_left = 86400 - (current_time - last_daily)
            embed = discord.Embed(
                title="Sorry",
                description=f"**You can use this command after** {time_left} **seconds**.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        reward = random.randrange(500, 7000)
        self.userdata[user_id]["balance"] +=reward
        self.userdata[user_id]["last_daily"] = current_time
        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Daily Reward",
            description=f"**Your daily reward is:** {reward}",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="work", description="find a job and work")
    @commands.cooldown(1, 50, commands.BucketType.user)
    async def findjob(self, interaction:discord.Interaction):
        user_id = str(interaction.user.id)
        user_balance = self.userdata[user_id]["balance"]

        if user_id not in self.userdata:
            embed = discord.Embed(
                title = "Error",
                description="You dont have an account run ```?**addacc**`` to create an account",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        job_earnings = random.randrange(3000, 20000)

        if random.random() < 0.2:
            result_msg = "You worked hard but your boss forgot to pay you... again!"
        else:
            self.userdata[user_id]["balance"] += job_earnings ++ user_balance
            result_msg = f"You completed a job and earned **{job_earnings}**"

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Job Earnings",
            description=result_msg,
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gamble", description="gamble some money")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def gamble(self, interaction:discord.Interaction, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_balance = self.userdata[user_id]["balance"]

        if amount <= 0 or amount > user_balance:
            embed = discord.Embed(
                title="Error",
                description="Invalid amount to gamble or insufficient balance.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        chance = random.random()

        if chance < 0.5:  # 50% chance of winning
            winnings = amount * 2
            self.userdata[user_id]["balance"] += winnings
            result_msg = f"You won and earned **{winnings}**!"
        else:
            self.userdata[user_id]["balance"] -= amount

            if random.random() < 0.2:  # 20% chance of a funny message for losing
                result_msg = "You tried to outsmart the casino, but luck wasn't on your side."
            else:
                result_msg = f"You lost **{amount}**."

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Gambling Result",
            description=result_msg,
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="beg", description="beg for some money")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self,interaction:discord.Interaction):
        user_id = str(interaction.user.id)
        user_balance = self.userdata[user_id]["balance"]

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        if random.random() < 0.2:  # 20% chance of not receiving money while begging
            result_msg = "You begged and got... a pat on the back. No money this time!"
        else:
            earnings = random.randrange(1, 100)
            self.userdata[user_id]["balance"] += earnings
            result_msg = f"You begged and received **{earnings}**"

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Begging",
            description=result_msg,
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @findjob.error
    @gamble.error
    @beg.error
    async def command_on_cooldown(interaction, error):
        if isinstance(error, CommandOnCooldown):
            cooldown_messages = [
                "```Whoa there, speedy! Give it a rest for a moment.```",
                "```Slow down, pal! You're making the bot dizzy.```",
                "```Taking a break, huh? Good things come to those who wait!```",
                "```Hold your horses! You've got a cooldown to deal with.```",
                "```Cooldown engaged! Time to grab a snack while you wait.```",
            ]
            await interaction.response.send_message(random.choice(cooldown_messages))

    @app_commands.command(name="balance", description="Check yours or a user's balance")
    async def bankbal(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None:
            user = interaction.user

        user_id = str(user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry, the specified user does not have an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_balance = self.userdata[user_id]["balance"]
        user_bank_balance = self.userdata[user_id].get("bank_balance", 0)

        embed = discord.Embed(
            title="Wallet and Bank",
            description=f"**Wallet Balance:** {user_balance}\n**Bank Balance:** {user_bank_balance}",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="deposit", description="deposit to bank")
    async def deposit(self,interaction:discord.Interaction, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_balance = self.userdata[user_id]["balance"]

        if isinstance(amount, str) and amount.lower() == "all":
            amount = user_balance
        else:
            amount = int(amount)

        if amount <= 0 or amount > user_balance:
            embed = discord.Embed(
                title="Error",
                description="Invalid amount to deposit or insufficient balance.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        self.userdata[user_id]["balance"] -= amount
        self.userdata[user_id].setdefault("bank_balance", 0)
        self.userdata[user_id]["bank_balance"] += amount

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Deposit Complete",
            description=f"You deposited {'all your balance' if amount == user_balance else amount} into your bank.",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="withdraw", description="withdraw money from bank")
    async def withdraw(self,interaction:discord.Interaction, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_bank_balance = self.userdata[user_id].get("bank_balance", 0)

        if isinstance(amount, str) and amount.lower() == "all":
            amount = user_bank_balance
        else:
            amount = int(amount)

        if amount <= 0 or amount > user_bank_balance:
            embed = discord.Embed(
                title="Error",
                description="Invalid amount to withdraw or insufficient bank balance.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        self.userdata[user_id]["bank_balance"] -= amount
        self.userdata[user_id]["balance"] += amount

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Withdrawal Complete",
            description=f"You withdrew {'all your bank balance' if amount == user_bank_balance else amount} from your bank.",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="economylb", description="money leaderboard")
    async def lb(self,interaction:discord.Interaction):
        sorted_users = sorted(self.userdata.items(), key=lambda x: x[1]["balance"], reverse=True)
        leaderboard_text = "```css\n"
        position = 1

        for user_id, data in sorted_users[:10]:
            user = interaction.guild.get_member(int(user_id))
            username = user.display_name if user else "Unknown User"
            balance = data["balance"]
            leaderboard_text += f"{position}. {username}: {balance}\n"
            position += 1

        leaderboard_text += "```"

        embed = discord.Embed(
            title="Leaderboard - Top 10 Richest",
            description=leaderboard_text,
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="transfer", description="transfer money to a user")
    async def transfer(self,interaction:discord.Interaction, amount: int, target_user: discord.User):
        user_id = str(interaction.user.id)
        target_id = str(target_user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        if target_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="The target user does not have an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_balance = self.userdata[user_id]["balance"]

        if amount <= 0 or amount > user_balance:
            embed = discord.Embed(
                title="Error",
                description="Invalid amount to transfer or insufficient balance.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        self.userdata[user_id]["balance"] -= amount
        self.userdata[target_id]["balance"] += amount

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Transfer Complete",
            description=f"You transferred **{amount}** to {target_user.mention}.",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shop", description="view the shop")
    async def shop(self,interaction:discord.Interaction, page: int = 1):
        total_pages = (len(self.items) + self.ITEMS_PER_PAGE - 1) // self.ITEMS_PER_PAGE

        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        if page < 1 or page > total_pages:
            embed = discord.Embed(
                title="Error",
                description=f"Invalid page number. Please enter a number between 1 and {total_pages}.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        start_idx = (page - 1) * self.ITEMS_PER_PAGE
        end_idx = start_idx + self.ITEMS_PER_PAGE
        items_page = list(self.items.keys())[start_idx:end_idx]

        shop_text = "```css\n"
        for item in items_page:
            shop_text += f"{self.items[item]['icon']} {item.capitalize()}: {self.items[item]['price']}\n"
        shop_text += f"\nPage {page}/{total_pages}```"

        embed = discord.Embed(
            title="Shop",
            description=shop_text,
            color=discord.Color.random()
        )
        message = await interaction.response.send_message(embed=embed)

        if total_pages > 1:
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")

            def check(reaction, user):
                return user == interaction.user and str(reaction.emoji) in ["⬅️", "➡️"]

            while True:
                try:
                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                    if str(reaction.emoji) == "⬅️" and page > 1:
                        page -= 1
                    elif str(reaction.emoji) == "➡️" and page < total_pages:
                        page += 1

                    start_idx = (page - 1) * self.ITEMS_PER_PAGE
                    end_idx = start_idx + self.ITEMS_PER_PAGE
                    items_page = list(self.items.keys())[start_idx:end_idx]

                    shop_text = "```css\n"
                    for item in items_page:
                        shop_text += f"{self.items[item]['icon']} {item.capitalize()}: {self.items[item]['price']}\n"
                    shop_text += f"\nPage {page}/{total_pages}```"

                    await message.edit(content=None, embed=discord.Embed(title="Shop", description=shop_text, color=discord.Color.random()))
                    await message.remove_reaction(reaction, interaction.user)

                except asyncio.TimeoutError:
                    break

            await message.clear_reactions()

    @app_commands.command(name="buy", description="buy something from the shop")
    async def buy(self,interaction:discord.Interaction, *, item: str):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        if item not in self.items:
            embed = discord.Embed(
                title="Error",
                description="Item not found in the shop.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_balance = self.userdata[user_id]["balance"]
        item_data = self.items[item]

        if user_balance < item_data["price"]:
            embed = discord.Embed(
                title="Insufficient Funds",
                description="You don't have enough money to buy this item.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        self.userdata[user_id]["balance"] -= item_data["price"]
        self.userdata[user_id].setdefault("inventory", {})
        self.userdata[user_id]["inventory"].setdefault(item, 0)
        self.userdata[user_id]["inventory"][item] += 1

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Purchase Complete",
            description=f"You bought {item_data['icon']} {item.capitalize()} for {item_data['price']}.",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="check your inventory")
    async def inventory(self,interaction:discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_inventory = self.userdata[user_id].get("inventory", {})

        if not user_inventory:
            embed = discord.Embed(
                title="Inventory",
                description="Your inventory is empty.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        inventory_text = "```css\n"
        for item, quantity in user_inventory.items():
            inventory_text += f"{self.items[item]['icon']} {item.capitalize()}: {quantity}\n"
        inventory_text += "```"

        embed = discord.Embed(
            title="Inventory",
            description=inventory_text,
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sell", description="sell the items you have")
    async def sell(self,interaction:discord.Interaction, *, item: str):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run ``?addacc`` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_inventory = self.userdata[user_id].get("inventory", {})

        if item not in user_inventory or user_inventory[item] <= 0:
            embed = discord.Embed(
                title="Error",
                description="You don't have this item in your inventory.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        item_data = self.items[item]
        sell_price = item_data["price"] // 2

        self.userdata[user_id]["balance"] += sell_price
        self.userdata[user_id]["inventory"][item] -= 1

        if self.userdata[user_id]["inventory"][item] == 0:
            del self.userdata[user_id]["inventory"][item]

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Item Sold",
            description=f"You sold {item_data['icon']} {item.capitalize()} for {sell_price}.",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="duel", description="duel a member for money")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def duel(self, interaction:discord.Interaction, target_user: discord.User, amount: int):
        user_id = str(interaction.user.id)
        target_id = str(target_user.id)

        if user_id not in self.userdata or target_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Both players must have accounts. Make sure you and the target user have run ``**?addacc**``.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_balance = self.userdata[user_id]["balance"]
        target_balance = self.userdata[target_id]["balance"]

        if amount <= 0 or amount > user_balance:
            embed = discord.Embed(
                title="Error",
                description="Invalid amount to duel or insufficient balance.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        duel_messages = [
            f"{interaction.user.display_name} challenges {target_user.display_name} to a duel! 🤺",
            f"{target_user.display_name} receives the duel challenge from {interaction.user.display_name}! 🤺",
            f"{interaction.user.display_name} and {target_user.display_name} lock eyes, ready for a duel! 🤺",
        ]
        random_duel_message = random.choice(duel_messages)

        embed = discord.Embed(
            title="Duel Start",
            description=random_duel_message,
            color=discord.Color.random()
        )
        duel_msg = await interaction.response.send_message(embed=embed)

        await asyncio.sleep(2)

        winner_id = user_id if random.random() < 0.5 else target_id
        loser_id = target_id if winner_id == user_id else user_id

        self.userdata[winner_id]["balance"] += amount
        self.userdata[loser_id]["balance"] -= amount

        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        winner = interaction.guild.get_member(int(winner_id))
        loser = interaction.guild.get_member(int(loser_id))

        duel_results = [
            f"{winner.display_name} strikes a mighty blow and wins {amount} from {loser.display_name}! 💥",
            f"{loser.display_name} tried their best, but {winner.display_name} emerges victorious with {amount} richer! 💰",
            f"{winner.display_name} shows off their superior skills and takes {amount} from {loser.display_name}'s pockets! 🏆",
        ]
        random_duel_result = random.choice(duel_results)

        embed = discord.Embed(
            title="Duel Result",
            description=random_duel_result,
            color=discord.Color.random()
        )
        await duel_msg.edit(embed=embed)

    @app_commands.command(name="invest", description="Invest in....")
    async def invest(self,interaction:discord.Interaction, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="Sorry you do not have an account. Run `?addacc` to create an account.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_balance = self.userdata[user_id]["balance"]

        if amount <= 0 or amount > user_balance:
            embed = discord.Embed(
                title="Error",
                description="Invalid amount to invest or insufficient balance.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        potential_return = int(amount * random.uniform(1.05, 1.2))
        self.userdata[user_id]["balance"] -= amount
        self.userdata[user_id].setdefault("investments", 0)
        self.userdata[user_id]["investments"] += potential_return

        # Save userdata back to the JSON file
        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Investment",
            description=f"You invested {amount} and your potential return is {potential_return}.",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="redeem", description="Redeem your investments")
    async def redeem(self, interaction:discord.Interaction):
        user_id = str(interaction.user.id)

        if user_id not in self.userdata:
            embed = discord.Embed(
                title="Error",
                description="You don't have an account. Use `?addacc` to create one.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        user_investments = self.userdata[user_id].get("investments", 0)

        if user_investments <= 0:
            embed = discord.Embed(
                title="Error",
                description="You don't have any investments to redeem.",
                color=discord.Color.random()
            )
            await interaction.response.send_message(embed=embed)
            return

        # Calculate actual return based on a percentage
        actual_return = int(user_investments * random.uniform(0.8, 1.0))
        self.userdata[user_id]["balance"] += actual_return
        self.userdata[user_id]["investments"] = 0

        # Save self.userdata back to the JSON file
        with open('utils/userdata.json', 'w') as file:
            json.dump(self.userdata, file)

        embed = discord.Embed(
            title="Investment Redeemed",
            description=f"You redeemed your investments for {actual_return} and received cash.",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(Economy(bot), guilds=[discord.Object(id=SERVERID)])
import discord
from discord import app_commands, ui
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")
DISCORD_SERVER_ID = os.getenv("SERVER_ID")


class client(discord.Client):
    def __init__(self):
        intentes = discord.Intents.default()
        intentes.message_content = True
        super().__init__(intents=intentes)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=int(DISCORD_SERVER_ID)))
            self.synced = True


class my_modal(ui.Modal, title="Notification submissions"):
    answer = ui.TextInput(
        label="What to notify about",
        style=discord.TextStyle.short,
        placeholder="(Tentamen/Registration/Omtentamen/Terminsregistration)",
        default="(Tentamen/Registration/Omtentamen/Terminsregistration)",
        required=True,
        max_length=500,
    )
    date_input = ui.TextInput(
        label="When? (YYYY-MM-DD)",
        style=discord.TextStyle.short,
        placeholder=f"{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day}",
        default=f"{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day}",
        required=True,
        max_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            match str(self.answer):
                case "Tentamen":
                    pass
                case "Registration":
                    pass
                case "Omtentamen":
                    pass
                case "Terminsregistration":
                    pass
                case _:
                    await interaction.response.send_message(
                        "❌ Invalid occasion! Please only use the following (Tentamen/Registration/Omtentamen/Terminsregistration).",
                        ephemeral=True,
                    )
                    return
        except Exception:
            await interaction.response.send_message(
                "❌ Invalid occasion! Please only use the following (Tentamen/Registration/Omtentamen/Terminsregistration).",
                ephemeral=True,
            )
            return

        try:
            parsed_date = datetime.datetime.strptime(str(self.date_input), "%Y-%m-%d")
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid date! Please use the format YYYY-MM-DD.", ephemeral=True
            )
            return
        try:
            write_to_json(self.answer.value, str(parsed_date.date()))
        except Exception:
            await interaction.response.send_message(
                "Something went wrong Do note that i have no clue what went wrong but its prob in the parsing"
            )
            return
        embed = discord.Embed(
            title=self.title, description=f"{self.answer.label} {self.answer}"
        )
        embed = discord.Embed(
            title=self.title,
            description=(
                f"**Notification:** {self.answer}\n"
                f"**Time:** {parsed_date.date()}\n"
                f"**Submission should be done**"
            ),
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)


def write_to_json(event_type="Tentamen", date=str(datetime.datetime.now())):
    with open("datum.json", "r") as f:
        data = json.load(f)

    main_dict = data[0]

    if event_type not in main_dict:
        raise ValueError(f"Unknown event type: {event_type}")

    if main_dict[event_type] == [None]:
        main_dict[event_type] = []

    main_dict[event_type].append(date)

    with open("datum.json", "w") as f:
        json.dump(data, f, indent=4)


aclient = client()
tree = app_commands.CommandTree(aclient)


def eventEmbed():
    embed = discord.Embed(title="Upcoming events")
    text = ""
    with open("datum.json", "r") as file:
        data = json.load(file)
        if len(data[0]["Tentamen"]) != 0:
            text += "**Tentamen**\n"
            for i in data[0]["Tentamen"]:
                text += f"{i}\n"
        if len(data[0]["Registration"]) != 0:
            text += "**Registration**\n"
            for i in data[0]["Registration"]:
                text += f"{i}\n"
        if len(data[0]["Omtentamen"]) != 0:
            text += "**Omtentamen**\n"
            for i in data[0]["Omtentamen"]:
                text += f"{i}\n"
        if len(data[0]["Terminsregistration"]) != 0:
            text += "**Terminsregistration**\n"
            for i in data[0]["Terminsregistration"]:
                text += f"{i}\n"
    embed.description = text
    return embed


@tree.command(
    guild=discord.Object(id=int(DISCORD_SERVER_ID)),
    name="submit",
    description="Submits exam or other important events and their date",
)
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_modal(my_modal())


@tree.command(
    guild=discord.Object(id=int(DISCORD_SERVER_ID)),
    name="info",
    description="somsdfog",
)
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(embed=eventEmbed())


aclient.run(TOKEN)

import discord
from discord import app_commands, ui
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import datetime
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")


class client(discord.Client):
    def __init__(self):
        intentes = discord.Intents.default()
        intentes.message_content = True
        super().__init__(intents=intentes)
        self.synced = False

    async def setup_hook(self):
        self.loop.create_task(daily_notification())

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
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
    name="submit",
    description="Submits exam or other important events and their date",
)
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_modal(my_modal())


@tree.command(
    name="info",
    description="somsdfog",
)
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(embed=eventEmbed())


@tree.command(
    name="register",
    description="Register this server and channel to receive notifications",
)
async def register_command(interaction: discord.Interaction):
    if os.path.exists("server_info.json"):
        with open("server_info.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    # Check if this channel is already registered
    channel_already_registered = any(
        entry[1] == interaction.channel_id for entry in data
    )

    if channel_already_registered:
        await interaction.response.send_message(
            "This channel is already registered! ✅", ephemeral=True
        )
        return

    data.append([interaction.guild_id, interaction.channel_id])

    with open("server_info.json", "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(
        f"Server registered successfully! 🎉\n"
        f"**Server ID:** {interaction.guild_id}\n"
        f"**Channel ID:** {interaction.channel_id}",
        ephemeral=True,
    )


async def daily_notification():  #
    await aclient.wait_until_ready()
    while not aclient.is_closed():
        now = datetime.datetime.now()
        target = now.replace(hour=14, minute=59, second=0, microsecond=0)
        if now >= target:
            target += datetime.timedelta(days=1)
        seconds_until_target = (target - now).total_seconds()
        # Sleep until then
        await asyncio.sleep(seconds_until_target)

        # Send notifications
        if os.path.exists("datum.json"):
            with open("datum.json", "r") as d:
                info = json.load(d)
                print(info[0]["Registration"])
                for object in info[0]["Registration"]:
                    if datetime(object) == datetime.datetime.now:
                        if os.path.exists("server_info.json"):
                            with open("server_info.json", "r") as f:
                                data = json.load(f)
                            for _, channel_id in data:
                                channel = aclient.get_channel(channel_id)
                                if channel:
                                    await channel.send("<@>")


aclient.run(TOKEN)

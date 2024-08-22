import discord
from discord import app_commands
from discord import embeds
from discord.ext import commands
import discord.ui
import random
from datetime import datetime
import datetime
import requests
import calendar
import time
import urllib.request
import urllib
from urllib.error import HTTPError
import json
from pymongo import MongoClient
from discord import ButtonStyle
import os
import aiohttp  # Added aiohttp import

ts = calendar.timegm(time.gmtime())
loading_message = None
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="m", intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

uri = "mongodb+srv://k0uvuw:68h6ni@cluster0.ombggir.mongodb.net/?retryWrites=true&w=majority"
funFact = ["mtbr"]

mongobd = os.getenv('mongobd')
bot_owner_ids = [1026891696929255525]


@bot.event
async def on_message(message):
  if message.content == "za":
    await message.channel.send("hi,how are you!?")
  elif message.content == "z.help":
    await message.channel.send("hi,how are you!?2")
  elif message.content == "z.help2":
    await message.channel.send("hi,how are you!?3")

@bot.event
async def on_ready():

  description = "join https://dsc.gg/m29"
  await bot.change_presence(activity=discord.Game(
      name="join:https://dsc.gg/m29", description=description))
  print(f'Bot connecté en tant que {bot.user.name}')
  print(f'ID: {bot.user.id}')
  print("Bot running with:")
  print("Username: ", bot.user.name)
  print("User ID: ", bot.user.id)

  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands(s)")
  except Exception as e:
    print(e)




@bot.tree.command(name="fn-bot", description="Create a lobby bot.")
async def fortnite_bot(interaction: discord.Interaction, authcode: str):
  try:
    async with aiohttp.ClientSession() as session:
        # Make a POST request to get access token
        async with session.get(
            f'https://api-xji1.onrender.com/oauth?authorization_code={authcode}'
        ) as response:
            response_data = await response.json()
            account_id = response_data['account_id']
            display_name = response_data['display_name']
            icon_url = response_data['icon']
            embed = discord.Embed(title="fn-bot",
                                  description="Create a lobby bot.",
                                  color=0x00ff00)
            embed.add_field(name="Successful Login", value=f'Logged into {display_name}!', inline=False)
            embed.set_thumbnail(url=icon_url)
            embed.add_field(name='Account ID', value=account_id)
            embed.set_footer(
                            text="/fn-bot",
                            icon_url="https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
                        )
            await interaction.response.send_message(embed=embed)
  except Exception as e:
    print(e)
    embed = discord.Embed(title="fn-bot",
                            description="Create a lobby bot.",
                            color=0xff0000)
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1198655012012826634.webp")
    embed.add_field(name="Cannot login ", value=f'Probably bc `{authcode}` is outdated. Get a new [ here](https://www.epicgames.com/id/api/redirect?clientId=3446cd72694c4a4485d81b77adbb2141&responseType=code)', inline=False)
    embed.set_footer(
                            text="/fn-bot",
                            icon_url="https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
                        )
    await interaction.response.send_message(embed=embed)

# https://api-xji1.onrender.com/api/v2/party/crowns?accountId={accountId}&secret={secret}&deviceId={deviceId)}&number={amount}
@bot.tree.command(name="fn-fakelevel", description="Set a fake level")
async def fortnitebot_status(interaction: discord.Interaction, level: str):
    try:
        # Send loading message
        loading_message = await interaction.channel.send("Fetching data from API...")

        # Get accountId, secret, and deviceId from MongoDB
        client = MongoClient(uri, connect=False)
        collection = client.ZapotronBot.deviceAuths
        user_data = collection.find_one({"discord_id": interaction.user.id})

        if not user_data:
            await loading_message.edit(content="You need to login first.")
            return

        accountId = user_data['account_id']
        secret = user_data['secret']
        deviceId = user_data['device_id']

        # Construct the URL with query parameters
        url = f"https://api-xji1.onrender.com/api/v2/party/level?accountId={accountId}&secret={secret}&deviceId={deviceId}&level={level}"
        async with aiohttp.ClientSession() as session:
            retries = 3  # Number of retries
            for attempt in range(retries):
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Process the data as needed

                        # Create an embed
                        embed = discord.Embed(title=f"Successfully swapped {level}", color=discord.Color.green())
                        embed.set_thumbnail(url="https://media.discordapp.net/attachments/894313949573554226/949095749180862544/checkmark.png?ex=6621b5cb&is=660f40cb&hm=49319598fbc9f1d66a2b8b051fac9c9a3fbbe5fd765ade63b0308eba082e1275&=&format=webp&quality=lossless&width=750&height=671")  # Placeholder image URL
                        embed.add_field(name="Data", value=str(data))

                        # Edit loading message to embed
                        await loading_message.edit(content=None, embed=embed)
                        break  # Break the retry loop if successful
                    elif response.status == 429:    
                        # Retry after a delay
                        await asyncio.sleep(2 ** attempt)
                    elif response.status == 500:    
                        embed = discord.Embed(title="fn-fake-level",
                                  description="",
                                  color=0x00ff00)
                        embed.add_field(name="Please launch fortnite", value='', inline=False)
                        embed.set_image(url="https://tenor.com/view/launch-sideways-astra-slide-failure-gif-23032202")
                        embed.set_footer(
                            text="/fn-bot",
                            icon_url="https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
                        )
                        await interaction.response.send_message(embed=embed)
                    else:
                        await loading_message.edit(content=f"Failed to fetch data from API. Status code: {response.status}")
                        break  # Break the retry loop on non-retryable error codes
    except Exception as e:
        print('Error:', e)
        try:
            await loading_message.edit(content='An error occurred while fetching data from the API.')
        except discord.errors.NotFound:
            print("Interaction not found.")
        except Exception as e:
            print("An error occurred while sending the error message:", e)





@bot.tree.command(name='custom-status', description='Get a custom status')
async def status(interaction: discord.Interaction, status: str):
    try:
        # Send loading message
        loading_message = await interaction.channel.send("Fetching data from API...")

        # Get accountId, secret, and deviceId from MongoDB
        client = MongoClient(uri, connect=False)
        collection = client.ZapotronBot.deviceAuths
        user_data = collection.find_one({"discord_id": interaction.user.id})

        if not user_data:
            await loading_message.edit(content="You need to login first.")
            return
        refresh_token = user_data['refresh_token']
        accountId = user_data['account_id']
        access_token = user_data['access_token']
        # Construct the URL with query parameters
        url = f"https://api-xji1.onrender.com/api/v2/party/customstatus?token={refresh_token}&accountId={accountId}&status={status}"

        async with aiohttp.ClientSession() as session:
            retries = 3  # Number of retries
            for attempt in range(retries):
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Process the data as needed

                        # Create an embed
                        embed = discord.Embed(title=f"succesful set {status}", color=discord.Color.green())
                        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/tc0VcFM9g35bjVCfnZcSRNpRrdu1VbW8PDqr2hQAHiU/https/ironweb10.github.io/Pulsar-9000-GG/imagg/crown.jpg?format=webp&width=375&height=375")  # Placeholder image URL

    except Exception as e:
        print('Error:', e)
        await loading_message.edit(content="An error occurred while fetching data from the API.")


import discord
from discord.ext import commands
import aiohttp
import json
from pymongo import MongoClient

#uri = "mongodb+srv://mtbr29:s9bUacozh8yTfsB0@mtbr29.y4wregh.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://k0uvuw:68h6ni@cluster0.ombggir.mongodb.net/?retryWrites=true&w=majority"

@bot.tree.command(name='logout', description='Logs out from your epic games account!')
async def logout(interaction: discord.Interaction):
    try:

        # Connect to MongoDB
        client = MongoClient(uri, connect=False)

        # Get the collection
        collection = client.ZapotronBot.deviceAuths

        # Delete the user's data from the collection
        result = collection.delete_one({"discord_id": interaction.user.id})

        if result.deleted_count > 0:
            await interaction.response.send_message("You have been logged out successfully.")
        else:
            await interaction.response.send_message("You are not currently logged in.")

    except Exception as e:
        print('Error:', e)
        await interaction.response.send_message('An error occurred. Please try again.')





@bot.tree.command(name='login', description='Logins into your epic games account!')
async def login(interaction: discord.Interaction, authcode: str = None):
  if authcode is None:
    embed = discord.Embed(title="auth code", description="", color=0x00ff00)
    embed.add_field(
      name="step 1: ",
      value=
      "Login [here](https://www.epicgames.com/id/login).<a:loading:1206274680864903259> ",
      inline=False)
    embed.add_field(
      name="step 2:",
      value=
      "Visit the [link here](https://www.epicgames.com/id/api/redirect?clientId=3446cd72694c4a4485d81b77adbb2141&responseType=code) above to get your login code.:link: ",
      inline=False)
    embed.add_field(
      name="step 3:",
      value=
      "You should see a code after `?code=` like the picture.<a:llama:1181943210713550930> ",
      inline=False)
    embed.set_image(
      url=
      "https://media.discordapp.net/attachments/971328290067456000/1005656280758767767/unknown.png"
  )
    embed.set_footer(
      text="/auth-code",
      icon_url=
      "https://cdn.discordapp.com/app-icons/118044643767.png?size=64"
  )
    await interaction.response.send_message(embed=embed)
  else:
    try:
        async with aiohttp.ClientSession() as session:
            # Make a POST request to get access token
            async with session.get(
                f'https://api-xji1.onrender.com/oauth?authorization_code={authcode}'
            ) as response:
                response_data = await response.json()

        # Extract data from the response
        access_token = response_data['access_token']
        account_id = response_data['account_id']
        display_name = response_data['display_name']
        refresh_token = response_data['refresh_token']
        device_id = response_data['device_id']
        secret = response_data['secret']
        icon_url = response_data['icon']

        # Connect to MongoDB
        client = MongoClient(uri, connect=False)

        # Get the collection
        collection = client.ZapotronBot.deviceAuths

        # Construct the data to write to MongoDB
        dataToWrite = {
            'access_token': access_token,
            'account_id': account_id,
            'display_name': display_name,
            'refresh_token': refresh_token,
            'device_id': device_id,
            'secret': secret,
            'icon': icon_url,
            'discord_id': interaction.user.id
        }

        # Insert the data into the collection
        collection.insert_one(dataToWrite)

        # Create an embedded message
        embed = discord.Embed(title='Successful Login!', description=f'Logged into {display_name}!', color=0x00FF00)
        embed.set_thumbnail(url=icon_url)
        embed.add_field (name='Account ID', value=account_id)

        # Send the embedded message
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print('Error:', e)
        icon_url ="https://cdn.discordapp.com/emojis/1198655012012826634.webp?size=128"
        embed = discord.Embed(title='Unable Login!', description='Sorry please try in 5min!', color=0xff0000)
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name='get a new authcode', value="[ :arrow_right: authcode:arrow_left:](https://rebrand.ly/authcode)")

        await interaction.response.send_message(embed=embed)



import asyncio
import aiohttp

@bot.tree.command(name='ghost-equip', description='Fetches data from a specific API')
async def fechar_api(interaction: discord.Interaction, type: str,name: str):
    try:
        # Send loading message
        loading_message = await interaction.channel.send("Fetching data from API...")

        # Get accountId, secret, and deviceId from MongoDB
        client = MongoClient(uri, connect=False)
        collection = client.ZapotronBot.deviceAuths
        user_data = collection.find_one({"discord_id": interaction.user.id})

        if not user_data:
            await loading_message.edit(content="You need to login first.")
            return

        accountId = user_data['account_id']
        secret = user_data['secret']
        deviceId = user_data['device_id']

        # Construct the URL with query parameters
        url = f"https://api-xji1.onrender.com/api/v2/party/ghostequip?accountId={accountId}&secret={secret}&deviceId={deviceId}&{type}={name}"

        async with aiohttp.ClientSession() as session:
            retries = 3  # Number of retries
            for attempt in range(retries):
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Process the data as needed

                        # Create an embed
                        embed = discord.Embed(title=f"Successfully equipped the {type} :{name}", color=discord.Color.green())
                        embed.set_thumbnail(url="https://www.pngall.com/wp-content/uploads/9/Green-Tick-Vector-PNG-Pic.png")  # Placeholder image URL
                        embed.add_field(name="{type}", value={name})
                        embed.add_field(name="Data", value=str(data))

                        # Edit loading message to embed
                        await loading_message.edit(content=None, embed=embed)
                        break  # Break the retry loop if successful
                    elif response.status == 429:
                        # Retry after a delay
                        await asyncio.sleep(2 ** attempt)
                    elif response.status == 400:
                      embed = discord.Embed(title="An error has ocured!", color=discord.Color.red())  # Placeholder image URL
                      embed.add_field(name="please put a valid type:`emote,outfit` or a valid name: `floss`", value="serch command:")
                    elif response.status == 500:
                      embed = discord.Embed(title="An error has ocured!", color=discord.Color.red())  # Placeholder image URL
                      embed.add_field(name="please launch Fortnite", value="launch fortnite:")
                    else:
                        await loading_message.edit(content=f"Failed to fetch data from API. Status code: {response.status}")
                        break  # Break the retry loop on non-retryable error codes
    except Exception as e:
        print('Error:', e)
        try:
          # Send loading message
          loading_message = await interaction.channel.send("Fetching data from API...")
        except discord.errors.NotFound:
            print("Interaction not found.")
        except Exception as e:
            print("An error occurred while sending the error message:", e)




bot.run("")

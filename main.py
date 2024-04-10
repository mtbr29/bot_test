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

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="m", intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

funFact = ["mtbr"]

TOKEN = os.getenv('TOKEN')
bot_owner_ids = [1026891696929255525]

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 758346892357664818:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == '✅':
            print('yoooo')
            role = discord.utils.get(guild.roles, name='membre')
        else:
            role = discord.utils.get(guild.role, name=payload.emoji.name)

        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)
                print("done")
            else:
                print("member not found")
        else:
            print("role not found")

# Other event functions are left unchanged




@bot.event
async def on_message_pong(message):
  if message.content == "ping":
    await message.channel.send("Pong🏓!")


@bot.event
async def on_message(message):
  if message.content == "<@1180446437671178391>":
    await message.channel.send("hi,how are you!?")


@bot.event
async def on__message(message):
  if message.content == "<@1180446437671178391> help":
    await message.channel.send("hi do /help!?")


@bot.event
async def on_message_aes(message):
  if message.content == "<@1180446437671178391> z.fn-aes":
    try:
      # Make a GET request to the API
      response = requests.get('https://fortnite-api.com/v2/aes')
      response.raise_for_status(
      )  # Raise an error if the request was not successful

      data = response.json()  # Parse the JSON response
      aes_data = data['data']

      # Create an embed message
      embed = discord.Embed(
          title="AES Data",
          color=0x00ff00  # You can customize the color here
      )

      # Add fields to the embed with the fetched data
      embed.add_field(name="Build", value=aes_data['build'], inline=False)
      embed.add_field(name="Main Key", value=aes_data['mainKey'], inline=False)

      # Li    mit the number of dynamic keys displayed
      dynamic_keys = aes_data['dynamicKeys'][:5]  # Display the first 5 keys
      dynamic_keys_text = "\n".join(
          f"Filename: {item['pakFilename']}, GUID: {item['pakGuid']}, Key: {item['key']}"
          for item in dynamic_keys)
      embed.add_field(name="Dynamic Keys",
                      value=dynamic_keys_text,
                      inline=False)

      embed.add_field(name="Updated", value=aes_data['updated'], inline=False)
      embed.set_footer(
          text="/fn-aes",
          icon_url=
          "https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
      )
      # Send the embedded message as a response
      await message.channel.send(embed=embed)

    except Exception as e:
      # Handle any errors that occur during the request or response
      await message.channel.send(f'An error occurred: {e}')


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


@bot.tree.command(name='ping',
                  description='Test if the bot is online and play ping-pong!')
async def ping_slash(interaction: discord.Interaction):
  await interaction.response.send_message("Pong🏓!")



#pymongo>=2.7.2,<4.0

@bot.tree.command(name='test2', description='Test 2!')
async def add_role_button(interaction: discord.Interaction):
      if interaction.guild:
        role = discord.utils.get(interaction.guild.roles, name="testrole")
        member = interaction.user

        if role is not None:
            await member.add_roles(role)
            await interaction.response.send_message("Role added successfully!")

            # Create an embed message with the button
            embed = discord.Embed(title="Button Test", description="Click to get a role!", color=0x00ff00)
            view = discord.ui.View()
            button = discord.ui.Button(label="Click me!", style=discord.ButtonStyle.primary)
            button.callback = add_role_button
            view.add_item(button)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("Role not found!")
      else:
        await interaction.response.send_message("Unable to access guild information.")

    
@bot.tree.command(name='help', description='help you!')
async def help_slash(interaction: discord.Interaction):
  embed = discord.Embed(title="Help", description="", color=0x00ff00)
  embed.add_field(name="**General**", value="", inline=False)
  embed.add_field(name="```/ping```",
                  value=" :ping_pong: | Test if the bot is online.",
                  inline=False)
  embed.add_field(name="```/info```",
                  value="<:info:1102602224288415765> |info about mtbr29",
                  inline=False)
  embed.add_field(name="```/help```", value=":sos: | Help you!", inline=False)
  embed.add_field(name="```/ticket```",
                  value=":ticket: | Create a ticket.",
                  inline=False)
  embed.add_field(name="", value="", inline=False)
  embed.add_field(name="**Fortnite**", value="", inline=False)
  embed.add_field(name="", value="", inline=False)
  embed.add_field(name="```/fn-map```",
                  value=":map: | Show the curent  Fortnite map.",
                  inline=False)
  embed.add_field(name="```/fn-aes```",
                  value=":key: | Show the curent  Fortnite aes keys.",
                  inline=False)
  embed.add_field(
      name="```/fn-challenges```",
      value=
      ":chart_with_upwards_trend: | Show the curent  Fortnite challenges.",
      inline=False)
  embed.add_field(
      name="```/fn-playlist```",
      value=
      "<:PID_CP_Devices_Clapboard:1037683024571146250>| Show the curent  Fortnite challenges.",
      inline=False)
  embed.add_field(
      name="```/fn-search```",
      value=
      "<:PID_CP_Devices_MannequinStore:1037683015171715122>| Grabe info about any cosmetic.",
      inline=False)
  embed.add_field(name="```/random-spawn```",
                  value=":game_die:|Choose a random spawn for you",
                  inline=False)
  embed.add_field(
      name="```/auth-code```",
      value="<:peeposendcode:761411851765809223> |give an auth code",
      inline=False)
  embed.add_field(name="```/login```",
                  value="<:EpicGamesLogo:1041097675157803038> |Login.",
                  inline=False)
  embed.add_field(name="", value="", inline=False)
  embed.add_field(name="**Fortnite paks**", value="", inline=False)
  embed.add_field(name="", value="", inline=False)
  embed.add_field(
      name="```/fn-orange-copy```",
      value="<:4_:1197069192432734238> |Give the latest orange copy pack!",
      inline=False)
  embed.add_field(
      name="```/fn-dev-inv```",
      value="<:3_:1197069301790806178> |Give the latest Dev inventory pack!",
      inline=False)
  embed.add_field(
      name="```/fn-dev-lego```",
      value="<:1_:1197069324586856498> |Give the latest Dev lego pack!",
      inline=False)
  embed.add_field(
      name="```/fn-stw-builds```",
      value=
      "<:fortnitestw:1089518007891525692> |Give the latest STW builds pack!",
      inline=False)
  embed.add_field(
      name="```/fn-cr-ro```",
      value="<:5_:1197069182353817640> |Give the latest Creative royal pack!",
      inline=False)
  embed.set_footer(
      text="/help",
      icon_url=
      "https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
  )
  await interaction.response.send_message(embed=embed)


@bot.tree.command(name="fn-challenges", description="challegs gathered")
async def fortnite_challenges(interaction: discord.Interaction):
  try:
    # Fetch Fortnite challenges from the API
    response = requests.get('https://fortnite-api.com/v2/news')
    data = response.json()

    # Display the response in a code block in Discord
    formatted_data = json.dumps(data, indent=2)
    await interaction.response.send_message(f'```json\n{formatted_data}```')
  except Exception as e:
    print(e)
    await interaction.response.send_message(
        'An error occurred while fetching Fortnite challenges.')

@bot.tree.command(name="fn-item-shop",
                  description="give item shop")
async def item_shop(interaction: discord.Interaction, ):
    embed = discord.Embed(title="fn-shop",
                          description="give item shop.",
                          color=0x00ff00)
    embed.add_field(name="**Fortnite Item Shop**", value="", inline=False)
    embed.set_footer(
        text="/fn-item-shop",
        icon_url=
        "https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="fn-bot", description="Get a lobby bot.")
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

@bot.tree.command(name="epic-launch",
                  description="Log in to your Epic Games account")
async def launche(interaction: discord.Interaction, authcode:str):
  if not authcode:
    embed = discord.Embed(title="epic-launch",
                          description="Please provide the authorization code.",
                          color=0x00ff00)
    embed.set_footer(
        text="/epic-launch",
        icon_url=
        "https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
    )
    await interaction.response.send_message(embed=embed)
    return

  else:
    embed = discord.Embed(title="epic-launch",
                          description="show the current Fortnite map!",
                          color=0x00ff00)
    embed.add_field(
        name="For login on *epicgames.com* click on the link",
        value=f"https://www.epicgames.com/id/exchange?exchangeCode={authcode}")
    embed.set_footer(
        text="/epic-launch",
        icon_url=
        "https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


#,icon_url="https://cdn.discordapp.com/app-icons/1180446437671178391/04de"




@bot.tree.command(name='fn-aes',
                  description='Fetch AES data from Fortnite API')
async def fn_aes_slash(interaction: discord.Interaction):
  try:
    # Make a GET request to the API
    response = requests.get('https://fortnite-api.com/v2/aes')
    response.raise_for_status(
    )  # Raise an error if the request was not successful

    data = response.json()  # Parse the JSON response
    aes_data = data['data']

    # Create an embed message
    embed = discord.Embed(
        title="AES Data",
        color=0x00ff00  # You can customize the color here
    )

    # Add fields to the embed with the fetched data
    embed.add_field(name="Build", value=aes_data['build'], inline=False)
    embed.add_field(name="Main Key", value=aes_data['mainKey'], inline=False)

    # Limit the number of dynamic keys displayed
    dynamic_keys = aes_data['dynamicKeys'][:5]  # Display the first 5 keys
    dynamic_keys_text = "\n".join(
        f"Filename: {item['pakFilename']}, GUID: {item['pakGuid']}, Key: {item['key']}"
        for item in dynamic_keys)
    embed.add_field(name="Dynamic Keys", value=dynamic_keys_text, inline=False)

    embed.add_field(name="Updated", value=aes_data['updated'], inline=False)
    embed.set_footer(
        text="/fn-aes",
        icon_url=
        "https://cdn.discordapp.com/app-icons/1180446437671178391/04de63270eb61b237a4f53709dc4a2fd.png?size=64"
    )
    # Send the embedded message as a response
    await interaction.response.send_message(embed=embed)

  except Exception as e:
    # Handle any errors that occur during the request or response
    await interaction.response.send_message(f'An error occurred: {e}')


# /fn-playlist


@bot.tree.command(name="fn-playlist", description="List of Fortnite playlist.")
async def fortnite_playlist(interaction: discord.Interaction):
  try:
    # Fetch Fortnite weapons from the API (you should replace the URL with the correct one)
    response = requests.get('https://fortnite-api.com/v1/playlists/get')
    data = response.json()

    # Display the response in a code block in Discord
    formatted_data = json.dumps(data, indent=2)
    await interaction.response.send_message(f'```json\n{formatted_data}```')
  except Exception as e:
    print(e)
    await interaction.response.send_message(
        'An error occurred while fetching Fortnite playlist.')


@bot.tree.command(name="fn-search",
                  description="Grab any cosmetics from Fortnite.")
async def search(interaction: discord.Interaction, name: str):
  try:
    grabingAPI = urllib.request.urlopen(
        f"https://fortnite-api.com/v2/cosmetics/br/search?name={name}")
    grabingJson = json.load(grabingAPI)
    cosmeticid = grabingJson['data']['id']
    cosmeticname = grabingJson['data']['name']
    cosmeticdescription = grabingJson['data']['description']
    cosmeticimage = grabingJson['data']['images']['icon']

    introduced_data = grabingJson['data']['introduction']
    introduced_message = f"Introduced in Chapter {introduced_data['chapter']}, Season {introduced_data['season']}."

    paths = grabingJson['data']['path']

    # Remove commas and spaces from the path string
    cleaned_paths = "".join(paths.split(', '))

    # Create an embed message
    embed = discord.Embed(
        title="Cosmetic Information",
        description=
        f"ID: {cosmeticid}\nName: {cosmeticname}\nDescription: {cosmeticdescription}",
        color=0x00ff00  # You can customize the color here
    )

    # Set the image in the embed
    embed.set_image(url=cosmeticimage)

    # Include introduced date and cleaned paths in the embed
    embed.add_field(name="Introduced", value=introduced_message, inline=False)
    embed.add_field(name="Paths", value=cleaned_paths, inline=False)

    # Send the embedded message as a response
    await interaction.response.send_message(embed=embed)

  except HTTPError as e:
    await interaction.response.send_message(f"Error: {e}")


# fn-map




import discord
from discord.ext import commands
import aiohttp
import json
from pymongo import MongoClient

uri = "mongodb+srv://wny51:jr5wsa@cluster0.n7ppuyq.mongodb.net/?retryWrites=true&w=majority"

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
async def fechar_api(interaction: discord.Interaction, emote: str):
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
        url = f"https://api-xji1.onrender.com/api/v2/party/ghostequip?accountId={accountId}&secret={secret}&deviceId={deviceId}&emote={emote}"

        async with aiohttp.ClientSession() as session:
            retries = 3  # Number of retries
            for attempt in range(retries):
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Process the data as needed
                        
                        # Create an embed
                        embed = discord.Embed(title=f"Successfully equipped {emote}", color=discord.Color.green())
                        embed.set_thumbnail(url="https://www.pngall.com/wp-content/uploads/9/Green-Tick-Vector-PNG-Pic.png")  # Placeholder image URL
                        embed.add_field(name="Emote", value=emote)
                        embed.add_field(name="Data", value=str(data))
                        
                        # Edit loading message to embed
                        await loading_message.edit(content=None, embed=embed)
                        break  # Break the retry loop if successful
                    elif response.status == 429:
                        # Retry after a delay
                        await asyncio.sleep(2 ** attempt)
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




bot.run("MTIwNzIzNTk5NTQyMzA4ODY2MA.G1EhSo.gfWCYUEZm9a1k456H--NkY4xbGTdvN5GCsEHW8")

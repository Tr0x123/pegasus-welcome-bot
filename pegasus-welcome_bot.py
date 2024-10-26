import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1267065112456335392
BACKGROUND_URL = "https://i.ibb.co/9hMBXJV/Frame-333.png"
FONT_PATH = "Font-Bold.ttf"  # Putanja do bold fonta koji si uploadovao

@bot.event
async def on_member_join(member):
    try:
        # Preuzimanje pozadinske slike sa URL-a
        response = requests.get(BACKGROUND_URL)
        background = Image.open(BytesIO(response.content))
        
        # Provera da li član ima avatar
        if member.avatar:
            avatar_url = member.avatar.url
        else:
            # Generisanje URL-a za podrazumevani Discord avatar
            avatar_url = f"https://cdn.discordapp.com/embed/avatars/{int(member.discriminator) % 5}.png"
        
        # Preuzimanje avatara
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")
        
        # Rezanje avatara u oblik kruga
        avatar = avatar.resize((150, 150), Image.LANCZOS)
        mask = Image.new('L', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
        
        # Primena maske
        avatar.putalpha(mask)
        
        # Postavljanje avatara na sredinu pozadinske slike
        avatar_position = ((background.width - avatar.width) // 2, 50)
        background(avatar, avatar_position, avatar)
        
        # Učitavanje fontova
        font_welcome = ImageFont.truetype(FONT_PATH, 50)  # Font za "DOBRODOŠLI"
        font_username = ImageFont.truetype(FONT_PATH, 32)  # Manji font za korisničko ime
        font_pegasus = ImageFont.truetype(FONT_PATH, 40)  # Font za "PEGASUS"
        
        # Dodavanje teksta "DOBRODOŠLI" ispod avatara
        draw = ImageDraw.Draw(background)
        text_welcome = "DOBRODOŠLI"
        text_welcome_size = draw.textbbox((0, 0), text_welcome, font=font_welcome)
        welcome_position = ((background.width - (text_welcome_size[2] - text_welcome_size[0])) // 2, avatar_position[1] + 160)
        draw.text(welcome_position, text_welcome, font=font_welcome, fill=(255, 255, 255))
        
        # Dodavanje korisničkog imena ispod "DOBRODOŠLI"
        username = f"{member.name}"  # Uklonjen tag (#)
        username_size = draw.textbbox((0, 0), username, font=font_username)
        username_position = ((background.width - (username_size[2] - username_size[0])) // 2, welcome_position[1] + 60)
        draw.text(username_position, username, font=font_username, fill=(0, 255, 255))
        
        # Dodavanje teksta "PEGASUS" ispod korisničkog imena
        text_pegasus = "PEGASUS"
        pegasus_size = draw.textbbox((0, 0), text_pegasus, font=font_pegasus)
        pegasus_position = ((background.width - (pegasus_size[2] - pegasus_size[0])) // 2, username_position[1] + 50)
        draw.text(pegasus_position, text_pegasus, font=font_pegasus, fill=(255, 255, 255))
        
        # Čuvanje rezultata
        image_path = "welcome_final.png"
        background.save(image_path)
        
        # Slanje slike u kanal
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"Welcome to the server, {member.name}!", file=discord.File(image_path))
    except Exception as e:
        print(f"An error occurred: {e}")

bot.run("YOUR_BOT_TOKEN")
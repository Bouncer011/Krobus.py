              # -----* made by mindset *----- #
       # -----* discord.gg/godkuprojectreborn *----- #

            # -----* join the serv ^^ *----- #
import discord
from discord.ext              import commands
from PIL                      import Image, ImageDraw, ImageFont, ImageSequence
from math                     import floor
from discord                  import File, Button, View
import os
import aiohttp
import random
import math

# -----* variables *----- #
ASSETS_PATH = ".assets"
TMP_PATH = ".tmp"
FONTS_PATH = "fonts"
XP_PER_LVL = 100

# -----* Point Class *----- #

# -----* Summary *----- #
# This code defines a `Point` class with attributes `x` and `y` representing coordinates.
# The class provides methods to return the point's coordinates as a tuple and 
# a method to return a "shadow" tuple, which offsets the coordinates by 1.
# -----* Summary *----- #

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def shadow_tuple(self):
        return (self.x + 1, self.y + 1)

    def as_tuple(self):
        return (self.x, self.y)

# -----* more variables *----- #
IMG_BG = os.path.join(ASSETS_PATH, "bg_rank.png")
IMG_FRAME = os.path.join(ASSETS_PATH, "bg_rank_border_square.png")
IMG_BG2 = os.path.join(ASSETS_PATH, "bg_rank.png")
IMG_FRAME2 = os.path.join(ASSETS_PATH, "bg_rank_border_square.png")
IMG_SM_BAR = os.path.join(ASSETS_PATH, "bg_rank_bar_small.png")
IMG_LG_BAR = os.path.join(ASSETS_PATH, "bg_rank_bar_large.png")
FONT = os.path.join(FONTS_PATH, "Roboto-Medium.ttf")
FONT_COLOR = (208, 80, 84)
BACK_COLOR = (82, 31, 33)
USERNAME_POS = Point(90, 8)
LEVEL_POS = Point(90, 63)
RANK_POS = Point(385, 68)
BAR_X = [133, 153, 173, 193, 213, 247, 267, 287, 307, 327]
BAR_Y = 37

# -----* xp_data dict *----- #
xp_data = {}

# -----* bot intents *----- #
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.members = True

# -----* bot initialization *----- #
bot = commands.Bot(command_prefix='!', intents=intents)

# -----* `help` command removed *----- #
bot.remove_command("help")

# -----* on ready event to tell the person the bot is ready *----- #
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# -----* profile picture support *----- #
async def download_avatar(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                with open(filename, 'wb') as f:
                    f.write(data)
                return True
    return False

# -----* image rendering *----- #
async def render_level_up_image(user: discord.Member, old_level: int, new_level: int) -> Optional[str]:
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)

    out_filename = os.path.join(TMP_PATH, f"level_up_{user.id}_{user.guild.id}.png")

    bg = Image.open(IMG_BG2)
    frame = Image.open(IMG_FRAME2)

    bg.paste(frame, (14, 12), frame)

    draw = ImageDraw.Draw(bg)
    font_22 = ImageFont.load_default()

    level_text = f"{old_level} -> {new_level}"
    level_width = font_22.getlength(level_text)
    draw.text((bg.width // 2 - level_width // 2, bg.height // 2 - 10), level_text, FONT_COLOR, font=font_22)

    bg.save(out_filename)
    bg.close()
    frame.close()

    return out_filename

async def render_lvl_image(user: discord.Member, username: str, xp: int, rank: int) -> Optional[str]:
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)

    lvl = floor(xp / XP_PER_LVL)
    bar_num = math.ceil(10 * (xp - (lvl * XP_PER_LVL)) / XP_PER_LVL)

    out_filename = os.path.join(TMP_PATH, f"{user.id}_{user.guild.id}.png")
    avatar_filename = out_filename

    avatar_url = user.display_avatar.url

    success = await download_avatar(avatar_url, avatar_filename)
    if not success:
        return None

    bg = Image.open(IMG_BG)
    frame = Image.open(IMG_FRAME)
    small_bar = Image.open(IMG_SM_BAR)
    large_bar = Image.open(IMG_LG_BAR)

    if user.display_avatar.is_animated():
        avatar = Image.open(avatar_filename)
        frames = [frame.copy() for frame in ImageSequence.Iterator(avatar)]
        for i in range(len(frames)):
            frames[i] = frames[i].resize((68, 68))
            bg.paste(frames[i], (16, 14), frames[i])
            bg.paste(frame, (14, 12), frame)
            for j in range(0, bar_num):
                if j % 5 == 4:
                    bg.paste(large_bar, (BAR_X[j], BAR_Y), large_bar)
                else:
                    bg.paste(small_bar, (BAR_X[j], BAR_Y), small_bar)
            draw = ImageDraw.Draw(bg)
            font_14 = ImageFont.load_default()
            font_22 = ImageFont.load_default()
            draw.text(USERNAME_POS.shadow_tuple(), username, BACK_COLOR, font=font_22)
            draw.text(USERNAME_POS.as_tuple(), username, FONT_COLOR, font=font_22)
            draw.text(LEVEL_POS.shadow_tuple(), f"Level {lvl}", BACK_COLOR, font=font_22)
            draw.text(LEVEL_POS.as_tuple(), f"Level {lvl}", FONT_COLOR, font=font_22)
            rank_text = f"Server Rank : {rank}"
            rank_width = font_14.getlength(rank_text)
            draw.text((RANK_POS.x - rank_width, RANK_POS.y), rank_text, BACK_COLOR, font=font_14)
        frames[0].save(out_filename, save_all=True, append_images=frames[1:], loop=0, duration=100)
    else:
        avatar = Image.open(avatar_filename).convert("RGBA")
        avatar = avatar.resize((68, 68))
        bg.paste(avatar, (16, 14), avatar)
        bg.paste(frame, (14, 12), frame)
        for i in range(0, bar_num):
            if i % 5 == 4:
                bg.paste(large_bar, (BAR_X[i], BAR_Y), large_bar)
            else:
                bg.paste(small_bar, (BAR_X[i], BAR_Y), small_bar)
        draw = ImageDraw.Draw(bg)
        font_14 = ImageFont.load_default()
        font_22 = ImageFont.load_default()
        draw.text(USERNAME_POS.shadow_tuple(), username, BACK_COLOR, font=font_22)
        draw.text(USERNAME_POS.as_tuple(), username, FONT_COLOR, font=font_22)
        draw.text(LEVEL_POS.shadow_tuple(), f"Level {lvl}", BACK_COLOR, font=font_22)
        draw.text(LEVEL_POS.as_tuple(), f"Level {lvl}", FONT_COLOR, font=font_22)
        rank_text = f"Server Rank : {rank}"
        rank_width = font_14.getlength(rank_text)
        draw.text((RANK_POS.x - rank_width, RANK_POS.y), rank_text, BACK_COLOR, font=font_14)
        bg.save(out_filename)

    bg.close()
    frame.close()
    small_bar.close()
    large_bar.close()
    avatar.close()

    return out_filename

async def render_leaderboard_image(guild):
    sorted_users = sorted(xp_data.items(), key=lambda x: x[1], reverse=True)
    top_ten = sorted_users[:10]

    leaderboard_image = Image.new('RGBA', (400, 50 * len(top_ten)), (255, 255, 255, 0))  # Transparent background
    for i, ((user_id, guild_id), xp) in enumerate(top_ten):
        user = guild.get_member(user_id)
        if user:
            rank_image_path = await render_lvl_image(user, user.display_name, xp, i + 1)
            rank_image = Image.open(rank_image_path).convert("RGBA")
            leaderboard_image.paste(rank_image, (0, 50 * i), rank_image)
            rank_image.close()

    leaderboard_filename = os.path.join(TMP_PATH, "leaderboard.png")
    leaderboard_image.save(leaderboard_filename)
    return leaderboard_filename

# -----* xp and rank retrieval *----- #
def get_xp(user_id, guild_id):
    return f"{xp_data.get((user_id, guild_id), 0)} XP"

def get_rank(user_id, guild_id):
    sorted_users = sorted(xp_data.items(), key=lambda x: x[1], reverse=True)
    user_rank = next((i + 1 for i, ((uid, gid), _) in enumerate(sorted_users) if uid == user_id and gid == guild_id), None)
    return user_rank

# -----* xp related events *----- #
@bot.event
async def on_member_join(member):
    xp_data[(member.id, member.guild.id)] = 0  # Initialize new members with 0 XP

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)
    
    user_id = message.author.id
    guild_id = message.guild.id
    
    user_xp = xp_data.get((user_id, guild_id), 0)
    
    # Add XP
    user_xp += random.randint(4, 15)  
    xp_data[(user_id, guild_id)] = user_xp

    await check_level_up(message)

async def check_level_up(message):
    user_id = message.author.id
    guild_id = message.guild.id
    
    user_xp = xp_data.get((user_id, guild_id), 0)

    old_level = floor(user_xp / XP_PER_LVL)
    new_level = floor(user_xp / XP_PER_LVL)
    
    if new_level > old_level:
        # Level up logic
        image_path = await render_level_up_image(message.author, old_level, new_level)
        if image_path:
            await message.channel.send(f"**Congrats {message.author.mention}! You have reached Level {new_level}**", file=File(image_path))

            os.remove(image_path)

# -----* command: setlevel *----- #
@bot.command(name='setlevel')
@commands.has_permissions(administrator=True) 
async def set_level(ctx, member: discord.Member, level: int):
    user_id = member.id
    guild_id = ctx.guild.id
    
    if level < 0:
        msg = await ctx.send("Please enter a positive level.")
        await msg.delete(delay=5)  # Delete the message after 5 seconds
        return
        
    xp_required = level * XP_PER_LVL
    xp_data[(user_id, guild_id)] = xp_required
    
    confirmation_msg = await ctx.send(f"{member.display_name}'s level has been set to {level}")
    await confirmation_msg.delete(delay=5)  # Delete the confirmation message after 5 seconds

# -----* command: xp *----- #
@bot.command(name='xp')
async def xp(ctx):
    user = ctx.author
    await ctx.send(f"{user.mention}, Your current XP: {get_xp(user.id, ctx.guild.id)}")

# -----* command: lvl *----- #
@bot.command(name='lvl', aliases=['level'])
async def lvl(ctx):
    user = ctx.author
    username = user.display_name
    rank = get_rank(user.id, ctx.guild.id)
    xp = xp_data.get((user.id, ctx.guild.id), 0)
    image_path = await render_lvl_image(user, username, xp, rank)

    if image_path:
        await ctx.send(f"Hello, {user.mention}! Here's your rank!", file=discord.File(image_path))
        
        leaderboard_image_path = await render_leaderboard_image(ctx.guild)
        if leaderboard_image_path:
            await ctx.send(file=discord.File(leaderboard_image_path), reference=ctx.message)

        os.remove(image_path)

# -----* command: leaderboard/lb *----- #
@bot.command(name='leaderboard', aliases=['lb'])
async def leaderboard(ctx):
    leaderboard_image_path = await render_leaderboard_image(ctx.guild)
    if leaderboard_image_path:
        await ctx.send(file=discord.File(leaderboard_image_path))
        os.remove(leaderboard_image_path)

# -----* command: addxp *----- #
@bot.command(name='addxp')
@commands.has_permissions(administrator=True)
async def add_xp(ctx, member: discord.Member, amount: int):
    user_id = member.id
    guild_id = ctx.guild.id
    
    if amount < 0:
        msg = await ctx.send("Please enter a positive XP amount.")
        await msg.delete(delay=5)  # Delete the message after 5 seconds
        return
    
    current_xp = xp_data.get((user_id, guild_id), 0)
    new_xp = current_xp + amount
    xp_data[(user_id, guild_id)] = new_xp
    
    confirmation_msg = await ctx.send(f"{amount} XP added to {member.display_name}. New XP: {new_xp}")
    await confirmation_msg.delete(delay=5)  # Delete the confirmation message after 5 seconds

# -----* command: help *----- #
@bot.command(name='help')
async def custom_help(ctx):
    embed = discord.Embed(title="krobus Commands", color=discord.Color.blue())
    
    embed.add_field(name="`!xp`", value="Check your current XP.", inline=False)
    embed.add_field(name="`!lvl`", value="Check your rank and level.", inline=False)
    embed.add_field(name="`!leaderboard` or `!lb`", value="View the server's leaderboard.", inline=False)
    embed.add_field(name="`!setlevel`", value="Set a user's level (Admin only).", inline=False)
    embed.add_field(name="`!addxp`", value="Add XP to a user (Admin only).", inline=False)

    await ctx.send(embed=embed)

bot.run("tokenhere")
# -----* token ^ *----- #

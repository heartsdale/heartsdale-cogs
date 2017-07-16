import discord
from discord.ext import commands
import os
import asyncio
import aiohttp

try: # check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False


class Limimin:
    """Limimin emoticon commands"""
    base_dir = os.path.join("data", "limimin")

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True)
    async def limimin(self, ctx):
        """Limimin emoticon commands"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

def check_folders():
    # create data/limimin if not there
    if not os.path.exists(Limimin.base_dir):
        print("Creating {} folder...".format(Limimin.base_dir))
        os.makedirs(Limimin.base_dir)

async def check_files():
    async with aiohttp.ClientSession() as session:
        stamp_url = "http://unisonleague.wikia.com/wiki/Stamps"
        async with session.get(stamp_url) as response:
            soup = BeautifulSoup(await response.text(), "html.parser") 

        for x in range(19, 39):
            image_name = "Stamp_0{}_Icon.png".format(x)
            image_path = "{}/{}".format(Limimin.base_dir,image_name)
            if not os.path.exists(image_path):
                print("Couldn't find {} ...".format(image_path))
                try:
                    image_url = soup.find("img", attrs={"data-image-key": image_name})["src"]
                    print("Downloading from {} ...", image_url)
                    async with session.get(image_url) as r:
                        image = await r.content.read()
                    with open(image_path, "wb") as f:
                        f.write(image)
                except Exception as e:
                    print(e)
        return

def setup(bot):
    # Check for beautifulsoup4
    if not soupAvailable:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
    
    # Main
    check_folders()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_files())
    n = Limimin(bot)
    bot.add_cog(n)
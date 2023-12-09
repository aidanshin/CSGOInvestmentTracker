import discord
import test
import asyncio
import time


async def send_message(message, user_message):
  try:
    if user_message.lower() == "status":
      minutes_left = round(30 - (abs(time.time() - time_start) / 60))
      await message.channel.send(f"{minutes_left} min before next run.")
      # while True:
      #   response = await test.scrape()
      #   await message.channel.send(response)
      #   await message.channel.send(file=discord.File("itemanalysis.txt"))
      #   await asyncio.sleep(1800)
    elif user_message.lower() == "stop":
      await message.channel.send("Shutting down.")
      quit()
    elif user_message.lower() == "profits":
      await message.channel.send("This function is in development.")
    else:
      await message.channel.send(
        "Invalid input --> Valid Inputs:\tstatus\tstop\tprofits")
  except Exception as e:
    print(e)


def run_discord_bot():
  #Input discord bot token below
  TOKEN = ''
  intents = discord.Intents.default()
  intents.message_content = True  # explicitly enable the message content intents
  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    #Input discord channel ID Below
    channel_id = 0
    gen_text_channel = client.get_channel(channel_id)
    await gen_text_channel.send("Successfully Connected.")
    print(f'{client.user} is now running!')
    while True:
      response = await test.scrape()
      await gen_text_channel.send(response)
      await gen_text_channel.send(file=discord.File("itemanalysis.txt"))
      global time_start
      time_start = time.time()
      await asyncio.sleep(1800)

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' ({channel})")

    await send_message(message, user_message)

    # if user_message[0] == '?':
    #     user_message = user_message[1:]
    #     await send_message(message, user_message, is_private=True)
    # else:
    #     await send_message(message, user_message, is_private=False)

  client.run(TOKEN)

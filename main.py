

from config import TOKEN, MIDJOURNERY_ID, ADMIN_ID, CHANNEL_ID, GUILD_ID

from discord import Client, Intents, Message

from services import  next_prompt, next_upscale, start, choose, save
from storage import Storage


intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)


@client.event
async def on_message(message:Message):
    print(f"{message.id=}\n{message.type=}\n{message.author=}\n{message.channel=}\n{message.guild=}\n{message.interaction=}\n{message.activity=}\n{message.attachments=}\n{message.content=}\n{message.components=}")
    print("\n")

    if Storage.work == False and Storage.state != 0:
        print("Does not work")
        return
    if message.content == "stop":
                Storage.state = 0
                Storage.work = False
                print("Stopped")
                await message.channel.send("Stopped")
                
    if Storage.state == 0:
        if message.author.id == ADMIN_ID:
            if message.content == "start":
                await message.channel.send("starting")
                start()
            elif message.content == "choose":
                await message.channel.send("Choose images")
                choose()
            elif message.content == "save":
                await message.channel.send("Start Save")
                save()
                await message.channel.send("Save Done")
    elif Storage.state == 1:
        if message.author.id == MIDJOURNERY_ID:
            if message.content.strip().endswith("(fast)"):
                if Storage.prompts != []:
                    Storage.random_choice = [message.id, [x.custom_id for x in message.components[0].children]]
                    next_prompt()
                else:
                    Storage.state = 0
                    print("Prompts Done")
                    await message.channel.send("Prompts Done")
    elif Storage.state == 2:
        if message.author.id == MIDJOURNERY_ID:
            if message.content.strip().endswith(f" <@{ADMIN_ID}>"):
                Storage.to_upscale.append([message.id, message.components[0].children[1].custom_id])
        elif message.author.id == ADMIN_ID:
            if message.content.strip() == "upscale":
                await message.channel.send("Starting upscale")
                Storage.state = 3
                if Storage.to_upscale != []:
                    next_upscale()
                else:
                    Storage.state = 0
                    print("No upscale found")
    elif Storage.state == 3:
        if message.author.id == MIDJOURNERY_ID:
            if message.content.strip().endswith("(fast)"):
                Storage.to_save_image.append([message.attachments[0].url,message.content.split("--")[0].strip()[2:]])
                if Storage.to_upscale != []:
                    next_upscale()
                else:
                    Storage.state = 0
                    print("Upscale done")
                    await message.channel.send("Upscale Done")   


if __name__ == "__main__":
    client.run(TOKEN)


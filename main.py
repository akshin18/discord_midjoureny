import sys
from time import sleep
from discord import Client, Intents, Message

from config import TOKEN, MIDJOURNERY_ID
from services import  auto_choose, next_choose, next_prompt, next_upscale, start, choose, save
from storage import Storage


intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)



@client.event
async def on_message(message:Message):
    print(f"{message.id=}\n{message.type=}\n{message.author=}\n{message.channel=}\n{message.guild=}\n{message.interaction=}\n{message.activity=}\n{message.attachments=}\n{message.content=}\n{message.components=}")
    print("\n")
    if message.content == "connect" and Storage.ADMIN_ID == None:
         Storage.ADMIN_ID = message.author.id
         Storage.CHANNEL_ID = message.channel.id
         Storage.GUILD_ID = message.guild.id
         await message.channel.send("Connected")
    if Storage.work == False and Storage.state != 0:
        print("Does not work")
        return
    if message.content == "stop":
                Storage.state = 0
                Storage.work = False
                print("Stopped")
                await message.channel.send("Stopped")
                
    if Storage.state == 0:
        # if message.author.id == Storage.ADMIN_ID:
            if message.content == "start":
                await message.channel.send("starting")
                start()
            elif message.content == "choose":
                await message.channel.send("Choose images")
                choose()
                if Storage.auto == True:
                    auto_choose()
                    next_choose()
                    sleep(5)
            elif message.content == "save":
                await message.channel.send("Start Save")
                save()
                await message.channel.send("Save Done")
    elif Storage.state == 1:
        # if message.author.id == MIDJOURNERY_ID:
            if message.content.strip().endswith("(fast)"):
                Storage.random_choice.append([message.id, [x.custom_id for x in message.components[0].children[:4]]])
                if Storage.prompts != []:
                    next_prompt()
                else:
                    Storage.state = 0
                    print("Prompts Done")
                    await message.channel.send("Prompts Done")
                    if Storage.auto == True:
                        await message.channel.send("choose")
                         
    elif Storage.state == 2:
        # if message.author.id == MIDJOURNERY_ID:
            if message.content.strip().endswith(f" <@{Storage.ADMIN_ID}>"):
                Storage.to_upscale.append([message.id, message.components[0].children[1].custom_id])
                if Storage.auto == True:
                    if Storage.choose == []:
                          await message.channel.send("upscale")
                    else:
                         next_choose()
                         sleep(10)
        # elif message.author.id == Storage.ADMIN_ID:
            if message.content.strip() == "upscale":
                await message.channel.send("Starting upscale")
                Storage.state = 3
                if Storage.to_upscale != []:
                    next_upscale()
                    sleep(10)

                else:
                    Storage.state = 0
                    print("No upscale found")
                    await message.channel.send("No upscale found")   
    elif Storage.state == 3:
        # if message.author.id == MIDJOURNERY_ID:
            if message.content.strip().endswith("(fast)"):
                if "," in message.content:
                    Storage.to_save_image.append([message.attachments[0].url,message.content.split(",")[0].strip()[2:]])
                else:
                    Storage.to_save_image.append([message.attachments[0].url,message.content.split("--")[0].strip()[2:]])
                if Storage.to_upscale != []:
                    next_upscale()
                else:
                    Storage.state = 0
                    print("Upscale done")
                    await message.channel.send("Upscale Done")   
                    await message.channel.send("Start Save")
                    save()
                    await message.channel.send("Save Done")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        Storage.auto = True
    client.run(TOKEN)


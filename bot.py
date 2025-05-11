import discord,random,asyncio
from discord.ext import commands
from config import token  # Botun tokenini config dosyasından içe aktarma

intents = discord.Intents.default()
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları banlamasına izin verir
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanızı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

@bot.event
async def on_message(message):
    if message.author==bot.user:
        return
    
    if any(word.startswith("http") for word in message.content.split()):
        await message.author.ban(reason="bağlantı göndermek yasaktır")
        await message.channel.send(f"{message.author.mention} bağlantı gönderdiği için yasaklandı")
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    await message.channel.send(message.content)

@bot.event
async def on_member_join(member):
    # Karşılama mesajı gönderme
    for channel in member.guild.text_channels:
        await channel.send(f'Hoş geldiniz: , {member.mention}!')
                           
@bot.event
async def guess(message,self):
    if message.author==bot.user:
        return
    if message.content.startswith('$guess'):
        await message.channel.send('1 ve 10 arasında sayı tuttum bil bakalım!')
        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await self.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f'Üzgünüm,cevap vermen çok uzun sürdü {answer}.')
        if int(guess.content) == answer:
            await message.channel.send('Doğru!')
        else:
            await message.channel.send(f'Hayır,Sayı = {answer}.')
bot.run(token)
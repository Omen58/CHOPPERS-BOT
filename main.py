import discord
from discord.ext import commands
from datetime import datetime
import os

# --------------------
# Ayarlar
# --------------------
TOKEN = os.getenv("TOKEN")
SES_KANAL_ID = 1429963189751119984
DUYURU_KANAL = "genel-duyuru"
SELAM_KANAL_ID = 1423633138839715935  # Selam mesajlarının dinleneceği kanal
ROL_ADI = "Kayıtsız Üye"
# --------------------

# --------------------
# Unicode Emojiler
# --------------------
KATESHI_DUYURU = "📢"
KATESHI_MEMBER = "👤"
KATESHI_TAKVIM = "📅"
KATESHI_SAATHAREKETLI = "⏱️"
KATESHI_KITAP = "📖"
KATESHI_UYARI = "⚠️"
# --------------------

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.messages = True  # mesajları dinleyebilmesi için
intents.message_content = True  # içerikleri okuyabilmesi için

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# Hayalet mod: ses kanalı
# ------------------------
@bot.event
async def on_ready():
    print(f"{bot.user} hazır, hayalet modda ses kanalında!")
    channel = bot.get_channel(SES_KANAL_ID)
    if channel and not bot.voice_clients:
        await channel.connect(self_deaf=True)
        print(f"{bot.user} artık sesleri duymuyor ve konuşamıyor.")

# ------------------------
# Yeni üye karşılama (DM + Embed)
# ------------------------
@bot.event
async def on_member_join(member):
    try:
        dm_embed = discord.Embed(
            title=f"{KATESHI_DUYURU} Sunucuya Yeni Katılan",
            color=0x00ff7f
        )
        dm_embed.add_field(name=f"{KATESHI_MEMBER} Kullanıcı", value=f"{member} - {member}", inline=False)
        dm_embed.add_field(name=f"{KATESHI_TAKVIM} Hesap oluşturma tarihi", value=member.created_at.strftime("%d %B %Y %H:%M"), inline=False)
        dm_embed.add_field(name=f"{KATESHI_SAATHAREKETLI} Sunucuya giriş sırası", value=f"{len(member.guild.members)}/{member.guild.member_count}", inline=False)
        dm_embed.add_field(name=f"{KATESHI_KITAP} Hesap güvenliği", value="Güvenli ✔", inline=False)
        dm_embed.add_field(name=f"{KATESHI_UYARI}", value=f"Merhabalar, sunucumuza hoşgeldiniz! Sunucumuza katıldığın için üzerine {ROL_ADI} rolünü verdim!", inline=False)
        dm_embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        dm_embed.set_footer(text="Choppers ile sunucuda güvenli ve keyifli vakit geçir!")
        await member.send(embed=dm_embed)
    except discord.Forbidden:
        print(f"{member.name} DM almayı kapalı, mesaj gönderilemedi.")

    kanal = discord.utils.get(member.guild.text_channels, name=DUYURU_KANAL)
    if kanal:
        embed = discord.Embed(
            title=f"{KATESHI_DUYURU} Sunucuya Yeni Katılan",
            color=0x00ff7f
        )
        embed.add_field(name=f"{KATESHI_MEMBER} Kullanıcı", value=f"{member} - {member}", inline=False)
        embed.add_field(name=f"{KATESHI_TAKVIM} Hesap oluşturma tarihi", value=member.created_at.strftime("%d %B %Y %H:%M"), inline=False)
        embed.add_field(name=f"{KATESHI_SAATHAREKETLI} Sunucuya giriş sırası", value=f"{len(member.guild.members)}/{member.guild.member_count}", inline=False)
        embed.add_field(name=f"{KATESHI_KITAP} Hesap güvenliği", value="Güvenli ✔", inline=False)
        embed.add_field(name=f"{KATESHI_UYARI}", value=f"Merhabalar, sunucumuza hoşgeldiniz! Sunucumuza katıldığın için üzerine {ROL_ADI} rolünü verdim!", inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.set_footer(text="Choppers ile sunucuda güvenli ve keyifli vakit geçir!")
        await kanal.send(embed=embed)

    rol = discord.utils.get(member.guild.roles, name=ROL_ADI)
    if rol:
        await member.add_roles(rol)

# ------------------------
# Selam mesajına cevap verme
# ------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # kendi mesajlarına tepki verme

    if message.channel.id == SELAM_KANAL_ID:
        content = message.content.lower()
        if any(word in content for word in ["sa", "selamün aleyküm", "selamun aleykum", "merhaba","sa", "selamün aleyküm", "selamun aleykum", "merhaba", "hey", "yo", "hi", "hii", "naber", "selam kanka", "selam millet", "günaydın", "tünaydın", "wassup", "heeeyy", "selaaam", "hopa", "selamlar"]):
            await message.reply("Aleyküm selam kardeşim 😎🌙")

    await bot.process_commands(message)  # komutların da çalışması için

@bot.command()
@commands.has_permissions(manage_messages=True)  # Sadece mesajları yönetme yetkisi olanlar kullanabilir
async def temizle(ctx, miktar: int = 50):
    """Varsayılan olarak son 50 mesajı siler."""
    deleted = await ctx.channel.purge(limit=miktar)
    await ctx.send(f"{len(deleted)} mesaj silindi ✅", delete_after=5) 

bot.run(TOKEN)


import disnake
from disnake.ext import commands

class RecruitementModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label="Your steam nickname", placeholder="enter your steam nickname", custom_id="name"),
            disnake.ui.TextInput(label="Your steam id", placeholder="enter your steam id", custom_id="id"),
        ]

        title = "Регистрация в базу данных"


        super().__init__(title=title, components=components, custom_id="recruitmentModal")

    async def callback(self, interaction: disnake.MessageInteraction):
        name = interaction.text_values["name"]
        id = interaction.text_values["id"]
        discord_nickname = interaction.author.display_name
        if discord_nickname.lower() != name.lower():
            embed = disnake.Embed(color=0x2F3136, title="Заявка не отправлена! The application has not been sent!")
            embed.description = f"{interaction.author.mention},удостоверьтесь, что ваш steam nickname и ваш ник в дискорде одинаковы " \
                                f"make sure your steam nickname and your discord nickname are the same.!"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = disnake.Embed(color=0x2F3136, title="Заявка отправлена! The application has been sent!")
            embed.description = f"{interaction.author.mention}, Благодарим вас за **регистрацию**! " \
                               f"Thank you for **registering**!"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            channel_id = 1201477307194413056
            channel = interaction.guild.get_channel(channel_id)
            if channel:
                await channel.send(f"{interaction.author.mention} {name} {id}")
            else:
                 print(f"Канал с ID {channel_id} не найден.")

class RecruitementSelect(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RecruitementButton())

class RecruitementButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            style=disnake.ButtonStyle.primary,
            label="Начать регистрацию",
            custom_id="start_registration_button",
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        modal = RecruitementModal()
        await interaction.response.send_modal(modal=modal)

class Recruitement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def registration(self, ctx):
        view = RecruitementSelect()
        await ctx.send('Нажмите кнопку для прохождение регистрации в базу данных', view=view)

def setup(bot):
    bot.add_cog(Recruitement(bot))

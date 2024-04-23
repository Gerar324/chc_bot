import disnake
from disnake import utils, NotFound
from disnake.ext import commands
from gspread import worksheet
import config
import gspread
from google.auth import exceptions
from google.oauth2 import service_account
from gspread_asyncio import AsyncioGspreadClientManager


# Загрузка учетных данных
credentials = service_account.Credentials.from_service_account_file(
    'C:/Users/traxe/chc_bot/chc_bot/database/chclash-1076469e3c51.json',  # Укажите путь к своему JSON-файлу
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Подключение к Google Sheets API

gc = AsyncioGspreadClientManager(credentials).authorize()


sh = gc.open('CHClash')
# Открытие таблицы по идентификатору
#spreadsheet_id =   # Идентификатор вашей таблицы
spreadsheet = gc.open_by_key('1SwcN9NIT5GJIbKhOpTCXtx498nkbSxqi0NkcedBNu3c')
worksheet = spreadsheet.sheet1



intents = disnake.Intents.all()

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == config.POST_ID:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        try:
            guild = bot.get_guild(payload.guild_id)
            user = await guild.fetch_member(payload.user_id)
            emoji = str(payload.emoji)
            role_id = config.ROLES.get(emoji)

            if role_id is not None:
                role = guild.get_role(role_id)

                if user is not None and role is not None:
                    if (
                        len(
                            [
                                r
                                for r in user.roles
                                if r.id not in config.EXCROLES
                            ]
                        )
                        <= config.MAX_ROLES_PER_USER
                    ):
                        await user.add_roles(role)
                        print(
                            "[SUCCESS] User {0.display_name} has been granted with role {1.name}".format(
                                user, role
                            )
                        )
                    else:
                        await message.remove_reaction(payload.emoji, user)
                        print(
                            "[ERROR] Too many roles for user {0.display_name}".format(
                                user
                            )
                        )
                else:
                    print("[ERROR] User or role not found for emoji " + emoji)

        except Exception as e:
            print(repr(e))
    else:
        if payload.user_id != bot.user.id:
            if payload.channel_id in [config.CHANNEL_ID3]:
                guild = bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)

                # Проверяем, что участник не имеет роли
                if config.ROLES2 not in member.roles:
                    # Получаем данные из гугл таблицы
                    user_nickname = "nickname"  # Замените на корректный заголовок столбца с никнеймами
                    user_id_column = "steam id"  # Замените на корректный заголовок столбца с идентификаторами
                    worksheet_values = worksheet.get_all_records()
                    user_data = {row[user_nickname].lower(): row[user_id_column] for row in worksheet_values}

                    # Проверяем, есть ли человек в таблице
                    nickname = member.display_name.lower()  # Используем display_name для ника участника
                    if nickname in user_data:
                        # Добавляем роль участника турнира
                        role = guild.get_role(config.ROLES2.get("✅"))
                        await member.add_roles(role)
                        user_nickname = member.display_name.lower()  # Используем display_name для ника участника
                        new_value = "+"
                        row_index = None
                        for index, row in enumerate(worksheet.get_all_values(), start=1):
                            if row[0].lower() == user_nickname.lower():
                                row_index = index
                                break

                        # Если нашли строку с никнеймом, обновляем значение в колонке C
                        if row_index is not None:
                            cell_range = f'C{row_index}'  # Формируем диапазон ячеек, например, C1, C2 и так далее
                            worksheet.update([[new_value]], range_name=cell_range)
                        else:
                            print(f"Никнейм {user_nickname} не найден в таблице.")
            else:
                if payload.channel_id in [config.CHANNEL_ID4]:
                    guild = bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)

                    # Проверяем, что участник не имеет роли
                    if config.ROLES2 not in member.roles:
                        # Получаем данные из гугл таблицы
                        user_nickname = "nickname"  # Замените на корректный заголовок столбца с никнеймами
                        user_id_column = "steam id"  # Замените на корректный заголовок столбца с идентификаторами
                        worksheet_values = worksheet.get_all_records()
                        user_data = {row[user_nickname].lower(): row[user_id_column] for row in worksheet_values}

                        # Проверяем, есть ли человек в таблице
                        nickname = member.display_name.lower()  # Используем display_name для ника участника
                        if nickname in user_data:
                            # Добавляем роль участника турнира
                            role = guild.get_role(config.ROLES2.get("✅"))
                            await member.add_roles(role)
                            user_nickname = member.display_name.lower()  # Используем display_name для ника участника
                            new_value = "+"
                            row_index = None
                            for index, row in enumerate(worksheet.get_all_values(), start=1):
                                if row[0].lower() == user_nickname.lower():
                                    row_index = index
                                    break

                            # Если нашли строку с никнеймом, обновляем значение в колонке C
                            if row_index is not None:
                                cell_range = f'D{row_index}'  # Формируем диапазон ячеек, например, C1, C2 и так далее
                                worksheet.update([[new_value]],range_name=cell_range )
                            else:
                                print(f"Никнейм {user_nickname} не найден в таблице.")


@bot.event
async def on_message(message):
    if message.channel.id == config.CHANNEL_ID2:
        message_content = message.content
        nick = [message_content]
        words = nick[0].split()
        # Записать два последних элемента в разные переменные
        var1 = words[-2]
        var2 = words[-1]
        worksheet.append_row([var1,var2])
        await bot.process_commands(message)
    else:
        if message.channel.id in [config.CHANNEL_ID3, config.CHANNEL_ID4]:
            # Ваш код обработки сообщения здесь
            # Например, добавление реакции или обработка команды
            await message.add_reaction('✅')  # Пример добавления реакции

            return await bot.process_commands(message)
        else:
            return await bot.process_commands(message)


@bot.event
async def on_raw_reaction_remove(payload):
    # Проверяем, что реакция произошла в нужном канале и сообщении
    if payload.user_id != bot.user.id:
        if payload.channel_id in [config.CHANNEL_ID3]:
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            user_nickname = member.display_name.lower()  # Используем display_name для ника участника
            new_value = ""
            row_index = None
            for index, row in enumerate(worksheet.get_all_values(), start=1):
                if row[0].lower() == user_nickname.lower():
                    row_index = index
                    break

            # Если нашли строку с никнеймом, обновляем значение в колонке C
            if row_index is not None:
                cell_range = f'C{row_index}'  # Формируем диапазон ячеек, например, C1, C2 и так далее
                worksheet.update([[new_value]], range_name=cell_range)

                row_index = None
                for index, row in enumerate(worksheet.get_all_values(), start=1):
                    if row[0].lower() == user_nickname.lower():
                        row_index = index
                        break
                # Если нашли строку с никнеймом
                if row_index is not None:
                    # Проверяем столбец D
                    cell_range_d = f'D{row_index}'


                    value_c = worksheet.acell(cell_range_d).value  # Получаем значение из ячейки D
                    if not value_c:
                        # Если значение пусто, убираем роль
                        tournament_role = guild.get_role(config.ROLES2.get("✅"))
                        if tournament_role in member.roles:
                            await member.remove_roles(tournament_role)
                            print(
                                "[SUCCESS] Role has been removed for user {0.display_name} in channel {1.name}".format(
                                    member, payload.channel_id))
                        else:
                            print("[INFO] User does not have the tournament role in the current channel.")
                    else:
                        print("[INFO] User still has the tournament role based on Google Sheets data.")


        else:
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            user_nickname = member.display_name.lower()  # Используем display_name для ника участника
            new_value = ""
            row_index = None
            for index, row in enumerate(worksheet.get_all_values(), start=1):
                if row[0].lower() == user_nickname.lower():
                    row_index = index
                    break

            # Если нашли строку с никнеймом, обновляем значение в колонке C
            if row_index is not None:
                cell_range = f'D{row_index}'  # Формируем диапазон ячеек, например, C1, C2 и так далее
                worksheet.update([[new_value]], range_name=cell_range)


                row_index = None
                for index, row in enumerate(worksheet.get_all_values(), start=1):
                    if row[0].lower() == user_nickname.lower():
                        row_index = index
                        break

                # Если нашли строку с никнеймом
                if row_index is not None:
                    # Проверяем столбец C
                    cell_range_c = f'C{row_index}'
                    value_c = worksheet.acell(cell_range_c).value  # Получаем значение из ячейки C
                    print(value_c)
                    if not value_c:
                        # Если значение пусто, убираем роль
                        tournament_role = guild.get_role(config.ROLES2.get("✅"))
                        if tournament_role in member.roles:
                            await member.remove_roles(tournament_role)
                            print(
                                "[SUCCESS] Role has been removed for user {0.display_name} in channel {1.name}".format(
                                    member, payload.channel_id))
                        else:
                            print("[INFO] User does not have the tournament role in the current channel.")
                    else:
                        print("[INFO] User still has the tournament role based on Google Sheets data.")
                        print(value_c)


bot.load_extension("mycog")
bot.run(config.TOKEN)

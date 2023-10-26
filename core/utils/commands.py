from aiogram import types, Bot


async def set_commands(bot: Bot):
    command = [
        types.BotCommand(command='start', description='Главное меню'),
        types.BotCommand(command='help', description='Справка'),
        types.BotCommand(command='support', description='Поддержка'),
    ]
    await bot.set_my_commands(command, types.BotCommandScopeDefault())

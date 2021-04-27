from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

ADMINS = env.list("ADMINS")

DB_IP = env.str("IP")
DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')
DB_NAME = env.str('DB_NAME')

WEB_TEMPLATE = '\n'.join(
    [
        '🔹 <b>{title}</b>',
        '📘 {subjects}',
        '📙 {levels}',
        '🗓 {date} 🕓 {time}МСК',
        '🔹 <i>{subtitle}</i>',
        '',
        '🔗 {url}',
        '➖➖➖➖➖➖➖➖➖➖\n\n'
    ]
)

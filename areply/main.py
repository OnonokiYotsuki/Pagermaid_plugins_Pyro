import aiohttp
import io
from pagermaid.listener import listener
from pagermaid.enums import Message, AsyncClient

@listener(filters.text & filters.regex(r"\($"))
async def reply_bracket_close(_, message: Message):
    await message.reply(message.chat.id, ")")
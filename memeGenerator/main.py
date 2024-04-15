import aiohttp
import io
from pagermaid.listener import listener
from pagermaid.enums import Message, AsyncClient

@listener(command="ask", description="发送请求并回复图片")
async def ask(message: Message, client: AsyncClient):
    await message.edit("正在ask...")
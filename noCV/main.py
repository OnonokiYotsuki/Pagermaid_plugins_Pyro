from pyrogram.enums import ChatMembersFilter

from pagermaid.listener import listener
from pagermaid.enums import Client, Message


@listener(
    command="nof",
    description="24bit禁止转发哦",
    groups_only=True,
    parameters="[要说的话]",
)
async def nof(client: Client, message: Message):
    消息所在群id = message.chat.id
    消息id = message.id
    await client.forward_messages(消息所在群id, 消息所在群id, 消息id,protect_content=True)
    await client.delete_messages(消息所在群id, 消息id)
    
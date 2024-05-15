import traceback
from asyncio import sleep
from datetime import datetime, timedelta, timezone
from pagermaid.utils import pip_install

pip_install("emoji")

from emoji import emojize
from pagermaid import logs, scheduler, bot


auto_change_name_init = False
dizzy = emojize(":dizzy:", language="alias")
cake = emojize(":cake:", language="alias")
all_time_emoji_name = [f"clock{h}" if m == 0 else f"clock{h}30" for h in range(1, 13) for m in range(0, 60, 30)]
time_emoji_symb = [emojize(f":{s}:", language="alias") for s in all_time_emoji_name]
number_emoji_symb = {
    "0": emojize(":zero:", language="alias"),
    "1": emojize(":one:", language="alias"),
    "2": emojize(":two:", language="alias"),
    "3": emojize(":three:", language="alias"),
    "4": emojize(":four:", language="alias"),
    "5": emojize(":five:", language="alias"),
    "6": emojize(":six:", language="alias"),
    "7": emojize(":seven:", language="alias"),
    "8": emojize(":eight:", language="alias"),
    "9": emojize(":nine:", language="alias"),
}

@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        time_cur = (
            datetime.utcnow()
            .replace(tzinfo=timezone.utc)
            .astimezone(timezone(timedelta(hours=8)))
            .strftime("%H:%M:%S:%p:%a")
        )
        hour, minu, seco, p, abbwn = time_cur.split(":")
        shift = 1 if int(minu) > 30 else 0
        hsym = time_emoji_symb[(int(hour) % 12) * 2 + shift]
        hour = "".join([number_emoji_symb[i] for i in hour])
        minu = "".join([number_emoji_symb[i] for i in minu])
        _last_name = f"{hour}:{minu} {hsym}"
        await bot.update_profile(last_name=_last_name)
        me = await bot.get_me()
        if me.last_name != _last_name:
            raise Exception("修改 last_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")
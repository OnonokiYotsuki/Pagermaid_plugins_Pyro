import traceback
from asyncio import sleep
from datetime import datetime, timedelta, timezone
from pagermaid.utils import pip_install

pip_install("emoji")

from emoji import emojize
from pagermaid import logs, scheduler, bot


emoji_num = {str(i): emojize(f":{['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][i]}:", language="alias") for i in range(10)}
all_time_emoji_name = [
    "clock12",
    "clock1230",
    "clock1",
    "clock130",
    "clock2",
    "clock230",
    "clock3",
    "clock330",
    "clock4",
    "clock430",
    "clock5",
    "clock530",
    "clock6",
    "clock630",
    "clock7",
    "clock730",
    "clock8",
    "clock830",
    "clock9",
    "clock930",
    "clock10",
    "clock1030",
    "clock11",
    "clock1130",
]
time_emoji_symb = [emojize(f":{s}:", language="alias") for s in all_time_emoji_name]

@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
        hour, minute = now.hour, now.minute
        shift = 1 if int(minute) > 30 else 0
        clock_emoji = time_emoji_symb[(int(hour) % 12) * 2 + shift]
        hour_emoji = "".join(emoji_num[digit] for digit in f"{hour:02}")
        minute_emoji = "".join(emoji_num[digit] for digit in f"{minute:02}")
        new_name = f"{hour_emoji}:{minute_emoji} {clock_emoji}"
        
        await bot.update_profile(last_name=new_name)
        if (await bot.get_me()).last_name != new_name:
            raise Exception("修改 last_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")
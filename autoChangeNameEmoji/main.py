import traceback
from datetime import datetime, timedelta, timezone
from emoji import emojize
from pagermaid import logs, scheduler, bot

EMOJI_NUM = {str(i): emojize(f":{['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][i]}:", language="alias") for i in range(10)}
EMOJI_CLOCK = [emojize(f":clock{i % 12}{'30' if i % 2 else ''}:", language="alias") for i in range(24)]

@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
        hour, minute = now.hour, now.minute
        shift = 1 if minute > 30 else 0
        clock_emoji = EMOJI_CLOCK[(hour % 12) * 2 + shift]
        hour_emoji = "".join(EMOJI_NUM[digit] for digit in f"{hour:02}")
        minute_emoji = "".join(EMOJI_NUM[digit] for digit in f"{minute:02}")
        new_name = f"{hour_emoji}:{minute_emoji} {clock_emoji}"
        
        await bot.update_profile(last_name=new_name)
        if (await bot.get_me()).last_name != new_name:
            raise Exception("修改 last_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")

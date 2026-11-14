import asyncio, random
from . import config, db, providers

def _system(with_profile: bool) -> str:
    s = f"نام تو {config.BOT_NAME} است.\n{config.BOT_DESCRIPTION}"
    if with_profile:
        s += f"\n\nمشخصات کاربر:\n{config.USER_PROFILE}"
    return s

JUDGE_RULES = (
    "\n\nنقش ویژه‌ی تو: داور و ترکیب‌کننده. چند پاسخ شماره‌گذاری‌شده از مدل‌های مختلف می‌بینی. "
    "درستی هر کدام را بسنج، تناقض‌ها را پیدا کن (حدس نزن؛ اگر مطمئن نیستی بگو)، "
    "و بهترین نسخه‌ی نهایی را به زبان کاربر بنویس. به وجود مدل‌های دیگر یا شماره‌ی پاسخ‌ها اشاره نکن."
)

async def answer_stream(question: str):
    history = db.recent()
    user_msg = {"role": "user", "content": question}

    # ۱) پیشنهادها به‌صورت موازی
    p_msgs = [{"role": "system", "content": _system(config.SHARE_PROFILE)}, *history, user_msg]
    results = await asyncio.gather(*(providers.ask(n, p_msgs) for n in config.PROPOSERS))
    answers = [r for r in results if r]
    random.shuffle(answers)   # کم کردن سوگیری داور

    # ۲) داور (فقط این بخش استریم می‌شود)
    if answers:
        block = "\n\n".join(f"--- پاسخ {i+1} ---\n{a}" for i, a in enumerate(answers))
        j_user = {"role": "user", "content": f"سؤال کاربر:\n{question}\n\n{block}"}
    else:
        j_user = user_msg   # هیچ مدلی جواب نداد؛ داور خودش جواب می‌دهد
    j_msgs = [{"role": "system", "content": _system(True) + JUDGE_RULES}, *history, j_user]

    full = ""
    async for piece in providers.stream(config.JUDGE, j_msgs):
        full += piece
        yield piece

    db.add("user", question)
    db.add("assistant", full)

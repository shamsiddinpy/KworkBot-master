from sqlalchemy import select, insert

from bot.button.inline import confirm_inline_btn
from db.config import session
from db.model import Task

admins = [5970755682]


async def confirm_task_admin(bot, task: dict):
    save = insert(Task).values(**task)
    session.execute(save)
    session.commit()
    query = select(Task).where(Task.title == task.get("title"))
    task = session.execute(query).fetchone()[0]
    design_str = f"""
        Specialty: {task.category.name}
        title : {task.title}
        description : {task.description}
        price : {task.price}
    """
    for admin in admins:
        await bot.send_message(chat_id=admin, text=design_str, reply_markup=confirm_inline_btn(task.id))


task_design = """
🟢   Buyurtma raqami #{0}

🟡  Kategoriya: {1}
    
🔵  Proyektning nomi: {2}
    
🟤  Project Ma'lumot: {3}
    
⚫   Proyektning narxi: {4} sum
"""

import aiosqlite as sq


async def sql_start():
    global db, cur
    db = await sq.connect("main_db.db")
    cur = await db.cursor()

    await cur.execute(
        "CREATE TABLE IF NOT EXISTS userinfo("
        "user_id INT PRIMARY KEY, "
        "user_name TEXT, "
        "usertype INT, "
        "active INT)"
    )
    await cur.execute(
        "CREATE TABLE IF NOT EXISTS shores("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "user_id INT, "
        "photo TEXT, "
        "geo_tag TEXT, "
        "about TEXT, "
        "destruction INT, "
        "activated INT)"
    )


"""
Раздел базой данных USERINFO
"""


async def sql_add_user(user_id):
    """Добавляем пользователя в таблицу userinfo.

    Аргументы:
        user_id: принимает id пользователя из telegram (не повторяется)
    """
    cursor = await cur.execute("SELECT 1 FROM userinfo WHERE user_id = ?", (user_id,))
    user = await cursor.fetchone()
    if not user:
        await cur.execute(
            "INSERT INTO userinfo VALUES (?, ?, ?, ?)",
            (user_id, "", 0, 1),
        )
        await db.commit()


async def sql_update_user_name(user_name, user_id):
    await cur.execute(
        "UPDATE userinfo SET user_name = ? WHERE user_id = ?",
        (
            user_name,
            user_id,
        ),
    )
    await db.commit()


async def sql_check_exist_user(user_id):
    cursor = await cur.execute("SELECT 1 FROM userinfo WHERE user_id = ?", (user_id,))
    user = await cursor.fetchone()
    if not user:
        return False
    else:
        return True


async def sql_read_usertype(user_id):
    cursor = await cur.execute(
        "SELECT usertype FROM userinfo WHERE user_id = ?", (user_id,)
    )
    usertype = await cursor.fetchone()
    if usertype is None:
        return None
    elif usertype[0] == 0:
        return "Пользователь"
    else:
        return "Администратор"


"""
Раздел базой данных SHORES
"""


async def sql_add_shores(user_id, photo, geo_tag, about, destruction, activated):
    await cur.execute(
        "INSERT INTO shores (user_id, photo, geo_tag, about, destruction, activated) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, photo, geo_tag, about, destruction, activated),
    )
    await db.commit()


async def sql_get_user_shores(user_id):
    await cur.execute("SELECT * FROM shores WHERE user_id = ?", (user_id,))
    return await cur.fetchall()


async def sql_get_coordinates_shores():
    await cur.execute(
        "SELECT geo_tag, about, photo, destruction, activated FROM shores",
    )
    return await cur.fetchall()


async def sql_read_count_photos(user_id):
    await cur.execute("SELECT * FROM shores WHERE user_id = ?", (user_id,))
    return len(await cur.fetchall())


async def get_info_if_activated_zero():
    await cur.execute("SELECT * FROM shores WHERE activated = 0")
    return await cur.fetchall()


async def set_activated_to_one(id):
    await cur.execute("UPDATE shores SET activated = 1 WHERE id = ?", (id,))
    await db.commit()


async def update_destruction(id, new_destruction_value):
    await cur.execute(
        "UPDATE shores SET destruction = ? WHERE id = ?",
        (
            new_destruction_value,
            id,
        ),
    )
    await db.commit()


# Функция для изменения значения about
async def update_about(id, new_about_value):
    await cur.execute(
        "UPDATE shores SET about = ? WHERE id = ?",
        (
            new_about_value,
            id,
        ),
    )
    await db.commit()


async def delete_by_id(id):
    await cur.execute("DELETE FROM shores WHERE id = ?", (id,))
    await db.commit()

from asyncio import sleep

from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.exc import DataError, OperationalError, ProgrammingError

engine = create_engine("mysql://root:Kranvagn13@localhost/", echo = True)

try:
    engine.execute('CREATE DATABASE reg_data')
except ProgrammingError:
    engine.execute('USE reg_data')

try:
    sql = ("CREATE TABLE reg_data("
            "id int not null primary key AUTO_INCREMENT,"
            "name varchar(20) not null,"
            "age int not null,"
            "city varchar(12) not null)")
    engine.execute(sql)
except OperationalError:
    pass

async def index_handler(request):
    with open('form.html', 'r') as html:
        return web.Response(body = html.read(), content_type = "text/html")

async def handle_reg_data(request):
    data = await request.post()
    name = data['name']
    age = data['age']
    city = data['city']
    try:
        engine.execute("INSERT INTO reg_data (name, age, city) "
                        f"VALUES ('{name}', {age}, '{city}');")
    except DataError:
        return web.Response(text = "There was an error processing your data.")
    await sleep(10)
    return web.Response(text = f"Created user {data['name']}")

app = web.Application()
app.router.add_get('/', index_handler)
app.router.add_post('/', handle_reg_data)

if __name__ == "__main__":
    web.run_app(app, port=8000)

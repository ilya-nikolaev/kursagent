from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.orm import sessionmaker, Session


class DBMiddleware(LifetimeControllerMiddleware):
    def __init__(self, pool):
        super(DBMiddleware, self).__init__()
        self.pool: sessionmaker = pool
        
    async def pre_process(self, obj, data: dict, *args):
        db = self.pool()
        data['db']: Session = db
    
    async def post_process(self, obj, data: dict, *args):
        if db := data['db']:
            db.close()

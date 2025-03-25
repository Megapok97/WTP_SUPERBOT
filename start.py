from app.core import superbot
from app.database import init_database

if __name__ == '__main__':
    init_database()
    superbot.start()

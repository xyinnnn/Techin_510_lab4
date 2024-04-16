import psycopg2

class Database:
    def __init__(self) -> None:
        self.com = psycopg2.connect(os.getenv('DATABASE_URL'))
        self.cur = self.com.coursor()

    def create_table(self);
        q = 

        self.cu



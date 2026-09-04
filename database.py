import psycopg, dotenv
import os

dotenv.load_dotenv()

DB=os.getenv("DB_NAME")
USER=os.getenv("DB_USER")
PASSWORD=os.getenv("DB_PASSWORD")
HOST=os.getenv("DB_HOST")
PORT=os.getenv("DB_PORT")

def db_connect():
    return psycopg.connect(
        f"""dbname={DB} 
            user={USER} 
            password={PASSWORD} 
            host={HOST} 
            port={PORT}
        """,
        row_factory=psycopg.rows.dict_row
    )

def init_db():
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        ) 
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id SERIAL PRIMARY KEY,
            type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
            amount NUMERIC(10,2) NOT NULL,
            description TEXT,
            category_id INTEGER NOT NULL,
            logged_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Successfully Initialized Database!")



if __name__ == "__main__":
    init_db()
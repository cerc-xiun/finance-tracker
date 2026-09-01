from database import db_connect

tables = {
    'expense' : 'expenses',
    'income' : 'income'
}

def insert_record( type: str, amount: float, category: str, logged_at: str=None, description: str=None):
    conn = db_connect()
    cursor = conn.cursor()

    table = tables.get(type, None)
    if table is None:
        conn.close()
        return {"error" : "The type of record to be inserted is neither EXPENSE nor INCOME."}


    category_id = _get_category_id(cursor, category)

    if category_id is None:
        category_id = _create_category(cursor, category)
        if category_id is None:
            conn.close()
            return {"error" : "Could not create or retrieve category."}
    
    cursor.execute(f"""
                        INSERT INTO {table} (amount, description, category_id, logged_at) VALUES (%s, %s, %s, %s)
                    """
                    , (amount, description, category_id, logged_at))
    
    conn.commit()
    conn.close()
    return {"message" : "Successfully Added the Transaction Record!"}

def get_transactions(category: str=None):
    conn = db_connect()
    cursor = conn.cursor()

    if category is None:

        cursor.execute("""  SELECT id, amount, description, category_id, logged_at, created_at, 'expense' AS type
                            FROM expenses 
                            
                            UNION ALL
                            
                            SELECT id, amount, description, category_id, logged_at, created_at, 'income' AS type
                            FROM income  
                        """)
        records = cursor.fetchall()
        conn.close()

        return records
    
    else:
        category_id = _get_category_id(cursor, category)
        if category_id is None:
            conn.close()
            return []
        
        cursor.execute("""
                        SELECT id, amount, description, category_id, logged_at, created_at, 'expense' AS type
                        FROM expenses  
                        WHERE category_id = %s
                        
                        UNION ALL
                        
                        SELECT id, amount, description, category_id, logged_at, created_at, 'income' AS type
                        FROM income
                        WHERE category_id = %s
                        """, 
                        (category_id, category_id))
        records = cursor.fetchall()
        conn.close()
        
        return records

def update_record(id: int, type: str, amount: float=None, description: str=None, logged_at: str=None):
    conn = db_connect()
    cursor = conn.cursor()

    table = tables.get(type, None)
    if table:
        if _check_record_existence(cursor, id, table):
            updates = []
            if amount is not None:
                cursor.execute(f"""
                    UPDATE {table}
                    SET amount = %s
                    WHERE id = %s
                """, (amount, id))
                updates.append("Amount")
            if description is not None:
                cursor.execute(f"""
                    UPDATE {table}
                    SET description = %s
                    WHERE id = %s
                """, (description, id))
                updates.append("Description")
            if logged_at is not None:
                cursor.execute(f"""
                    UPDATE {table}
                    SET logged_at = %s
                    WHERE id = %s
                """, (logged_at, id))
                updates.append("Logged At")

            conn.commit()
            conn.close()

            return {"message" : f"Successfully Updated: {updates}"}
        
        else:
            conn.close()
            return {"error" : "Non Existent Record to be updated."}

    else:
        conn.close()
        return {"error" : "The type of record to be updated is neither EXPENSE nor INCOME."}

def delete_record(id: int, type: str):
    conn = db_connect()
    cursor = conn.cursor()
    table = tables.get(type, None)

    if table:

        if _check_record_existence(cursor, id, table):
            cursor.execute(f"""
                DELETE FROM {table}
                WHERE id = %s
            """, (id,))

            conn.commit()
            conn.close()

            return {"message" : f"Successfully deleted record {id}"}
        
        else:
            conn.close()
            return {"error" : "Non Existent Record to be Deleted."}

    else:
        conn.close()
        return {"error" : "The type of record to be deleted is neither EXPENSE nor INCOME."}


def _get_category_id(cursor, category: str):
    row = cursor.execute("SELECT id FROM categories WHERE name=%s", (category,)).fetchone()
    return row['id'] if row else None
    

def _create_category(cursor, category: str):
    new_category = cursor.execute("INSERT INTO categories (name) VALUES(%s) RETURNING id", (category,)).fetchone()
    
    return new_category['id'] if new_category else None

def _check_record_existence(cursor, id: int, table: str) -> bool:
    cursor.execute(f"SELECT 1 FROM {table} WHERE id= %s", (id,))

    if cursor.fetchone():
        return True
    else:
        return False
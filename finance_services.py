from enum import StrEnum
from database import db_connect
from psycopg import Error

invalid_type_message = "The type of record to be updated is neither EXPENSE nor INCOME."

def insert_record(valid_types: type[StrEnum], type: str, amount: float, category: str, logged_at: str=None, description: str=None, ):
    if type not in [t.value for t in valid_types]:
        return {"error" : invalid_type_message}

    try:
        with db_connect() as conn:
            cursor = conn.cursor()
            category_id = _get_category_id(cursor, category)

            if category_id is None:
                category_id = _create_category(cursor, category)
                if category_id is None:
                    return {"error" : "Could not create or retrieve category."}
            
            cursor.execute(f"""
                                INSERT INTO transactions (type, amount, description, category_id, logged_at) VALUES (%s, %s, %s, %s, %s)
                            """
                            , (type, amount, description, category_id, logged_at))
            
            conn.commit()
            return {"message" : "Successfully Added the Transaction Record!"}

    except Error as e:
        return {"error" : f"Database error: {str(e)}"}
   

def get_transactions(category: str=None):
    try:
        with db_connect() as conn:
            cursor = conn.cursor()

            if category is None:

                cursor.execute("""  SELECT id, type, amount, description, category_id, logged_at, created_at
                                    FROM transactions
                                """)

                records = cursor.fetchall()
                return records
            
            else:

                category_id = _get_category_id(cursor, category)
                if category_id is None:
                    return []
                
                cursor.execute("""
                                SELECT id, type, amount, description, category_id, logged_at, created_at
                                FROM transactions  
                                WHERE category_id = %s
                                """, 
                                (category_id,))

                records = cursor.fetchall()
                return records
            
    except Error as e:
        return {"error" : f"Database error: {str(e)}"}
    

def update_record(valid_types: type[StrEnum], id: int, type: str, amount: float=None, description: str=None, logged_at: str=None):
    if type not in [t.value for t in valid_types]:
        return {"error" : invalid_type_message}
    
    try:
        with db_connect() as conn:
            cursor = conn.cursor()
            
            if _check_record_existence(cursor=cursor, id=id):
                updates = []
                if amount is not None:
                    cursor.execute(f"""
                        UPDATE transactions
                        SET amount = %s
                        WHERE id = %s
                    """, (amount, id))
                    updates.append("Amount")

                if description is not None:
                    cursor.execute(f"""
                        UPDATE transactions 
                        SET description = %s
                        WHERE id = %s
                    """, (description, id))
                    updates.append("Description")

                if logged_at is not None:
                    cursor.execute(f"""
                        UPDATE transactions
                        SET logged_at = %s
                        WHERE id = %s
                    """, (logged_at, id))
                    updates.append("Logged At")

                conn.commit()
                return {"message" : f"Successfully Updated: {updates}"}
            
            else:
                return {"error" : "Non Existent Record to be updated."}
    except Error as e:
        return {"error" : f"Database error: {str(e)}"}
     

def delete_record(valid_types: type[StrEnum], id: int, type: str):
    if type not in [t.value for t in valid_types]:
        return {"error" : invalid_type_message}

    try:
        with db_connect() as conn:
            cursor = conn.cursor()

            if _check_record_existence(cursor=cursor, id=id):
                cursor.execute(f"""
                    DELETE FROM transactions
                    WHERE id = %s
                """, (id,))

                conn.commit()
                return {"message" : f"Successfully deleted record {id}"}
            
            else:
                return {"error" : "Non Existent Record to be Deleted."}
    except Error as e:
        return {"error" : f"Database error: {str(e)}"}
    

def _get_category_id(cursor, category: str):
    try:
        row = cursor.execute("SELECT id FROM categories WHERE name=%s", (category,)).fetchone()
        return row['id'] if row else None
    except Error as e:
        return {"error" : f"Database error: {str(e)}"}
    

def _create_category(cursor, category: str):
    new_category = cursor.execute("INSERT INTO categories (name) VALUES(%s) RETURNING id", (category,)).fetchone()
    
    return new_category['id'] if new_category else None


def _check_record_existence(cursor, id: int):
    cursor.execute(f"SELECT 1 FROM transactions WHERE id= %s", (id,))
    return cursor.fetchone()
    
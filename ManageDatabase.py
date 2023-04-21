import pymysql

class ManageBooksDatabase():
    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_connection(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cur = self.con.cursor()

    def run_cmd(self, cmd):
        try:
            self.cur.execute(cmd)
            self.con.commit()
            return True
        except:
            return False
        
    def create_table(self, name, properties):
        cmd = f"CREATE TABLE {name} ({','.join(properties)})"
        response = self.run_cmd(cmd)

        return response

    def delete_table(self, name):
        cmd = f"DROP TABLE {name}"
        response = self.run_cmd(cmd)

        return response
    
    def insert(self, table, properties):
        # First property is primary key
        first_key, first_value = list(properties.items())[0]
        cmd = f"SELECT * FROM {table} WHERE {first_key} = '{first_value}'"
        response = self.run_cmd(cmd)

        if not response:
            return None

        if self.cur.fetchone() == None:
            # Table not contains elements with that id
            keys_without_quotes = str(tuple(properties.keys())).replace("'", "")
            cmd = f"INSERT INTO {table} {keys_without_quotes} VALUES {tuple(properties.values())}"
            self.run_cmd(cmd)

            return True
        
        return False
    
    def edit(self, table, primary_key, id, property, value):
        cmd = f"UPDATE {table} SET {property} = '{value}' WHERE {primary_key} = '{id}'"
        return self.run_cmd(cmd)

    def get_property(self, table, primary_key, id, property):
        cmd = f"SELECT {property} FROM {table} WHERE {primary_key} = {id}"
        self.run_cmd(cmd)

        fetched_cursor = self.cur.fetchone()

        if fetched_cursor:
            return fetched_cursor[0]

    def list(self, table):
        cmd = f"SELECT * FROM {table}"
        self.run_cmd(cmd)

        stringable_table = ""

        for i in self.cur:
            stringable_table += f"{i[0]}\t\t{i[1]}\t\t{i[2]}\t\t{i[3]}\n"

        return stringable_table
    
    def delete(self, table, key, value):
        cmd = f"DELETE FROM {table} WHERE {key} = {value}"
        self.run_cmd(cmd)

        if self.cur.rowcount > 0:
            return True
        
        return False

    
def main():
    with open(".credentials-books", "r") as file:
        content = file.read()
    content = content.split(",")
    # # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()
    response = manage_database.create_table(f"student001", ["i INT AUTO_INCREMENT", "issue_date DATE", "return_date DATE", "PRIMARY KEY(i)"])
    manage_database.delete_table("student001")

if __name__ == "__main__":
    main()
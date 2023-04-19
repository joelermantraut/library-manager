import pymysql

class ManageBooksDatabase():
    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table

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
    
    def insert(self, properties):
        # First property is primary key
        first_key, first_value = list(properties.items())[0]
        cmd = f"SELECT * FROM {self.table} WHERE {first_key} = '{first_value}'"
        print(cmd)
        response = self.run_cmd(cmd)

        if not response:
            return None

        if self.cur.fetchone() == None:
            # Table not contains elements with that id
            keys_without_quotes = str(tuple(properties.keys())).replace("'", "")
            cmd = f"INSERT INTO {self.table} {keys_without_quotes} VALUES {tuple(properties.values())}"
            self.run_cmd(cmd)

            return True
        
        return False
    
    def edit(self, primary_key, id, property, value):
        cmd = f"UPDATE {self.table} SET {property} = '{value}' WHERE {primary_key} = '{id}'"
        return self.run_cmd(cmd)

    def get_property(self, primary_key, id, property):
        cmd = f"SELECT {property} FROM {self.table} WHERE {primary_key} = {id}"
        self.run_cmd(cmd)

        fetched_cursor = self.cur.fetchone()

        if fetched_cursor:
            return fetched_cursor[0]

    def list(self):
        cmd = f"SELECT * FROM {self.table}"
        self.run_cmd(cmd)

        stringable_table = ""

        for i in self.cur:
            stringable_table += f"{i[0]}\t\t{i[1]}\t\t{i[2]}\t\t{i[3]}\n"

        return stringable_table
    
    def delete(self, key, value):
        cmd = f"DELETE FROM {self.table} WHERE {key} = {value}"
        self.run_cmd(cmd)

        if self.cur.rowcount > 0:
            return True
        
        return False

    
def main():
    with open(".credentials-books", "r") as file:
        content = file.read()
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()
    manage_database.insert({"bid": "102", "title": "Joel", "author": "Author2", "status": "available"})
    print(manage_database.list())

    manage_database.delete("bid", "102")
    print(manage_database.list())

if __name__ == "__main__":
    main()
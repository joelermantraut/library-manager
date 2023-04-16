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

    def insert_book(self, id, title, author, status):
        cmd = f"SELECT * FROM {self.table} WHERE bid = {id}"
        self.run_cmd(cmd)

        if self.cur.fetchone() == None:
            # Table not contains elements with that id
            cmd = f"INSERT INTO {self.table} (bid, title, author, status) VALUES ('{id}', '{title}', '{author}', '{status}')"
            self.run_cmd(cmd)

            return True

        return False
    
    def edit_book(self, id, property, value):
        cmd = f"UPDATE {self.table} SET {property} = '{value}' WHERE bid = '{id}'"
        return self.run_cmd(cmd)

    def get_property(self, id, property):
        cmd = f"SELECT {property} FROM {self.table} WHERE bid = {id}"
        self.run_cmd(cmd)

        fetched_cursor = self.cur.fetchone()

        if fetched_cursor:
            return fetched_cursor[0]

    def list_books(self):
        cmd = f"SELECT * FROM {self.table}"
        self.run_cmd(cmd)

        stringable_table = "BID\tTitle\tAuthor\tStatus\n"

        for i in self.cur:
            stringable_table += f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\n"

        return stringable_table
    
    def delete_book(self, id):
        cmd = f"DELETE FROM {self.table} WHERE BID = {id}"
        self.run_cmd(cmd)

        if self.cur.rowcount > 0:
            return True
        
        return False

    
def main():
    with open(".credentials", "r") as file:
        content = file.read()
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()
    manage_database.insert_book("101", "Joel", "Author2", "available")
    print(manage_database.list_books())

    manage_database.delete_book("102")
    print(manage_database.list_books())

if __name__ == "__main__":
    main()
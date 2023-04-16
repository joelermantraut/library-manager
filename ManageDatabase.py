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
        self.cur.execute(cmd)
        self.con.commit()

    def insert_book(self, id, title, author):
        cmd = f"SELECT * FROM {self.table} WHERE bid = {id}"
        self.run_cmd(cmd)

        if self.cur.fetchone() == None:
            # Table not contains elements with that id
            cmd = f"INSERT INTO {self.table} (bid, title, author, status) VALUES ('{id}', '{title}', '{author}', 'available')"
            self.run_cmd(cmd)
        else:
            cmd = f"UPDATE {self.table} SET title = '{title}' WHERE bid = '{id}'"
            self.run_cmd(cmd)
            cmd = f"UPDATE {self.table} SET author = '{author}' WHERE bid = '{id}'"
            self.run_cmd(cmd)

    def list_books(self):
        cmd = f"SELECT * FROM {self.table}"
        self.run_cmd(cmd)

        stringable_table = "BID\tTitle\tAuthor\tStatus\n"

        for i in self.cur:
            stringable_table += f"{i[0]}\t\t{i[1]}\t\t{i[2]}\t\t{i[3]}\n"

        return stringable_table
    
    def delete_book(self, id):
        cmd = f"DELETE FROM {self.table} WHERE BID = {id}"
        self.run_cmd(cmd)

    
def main():
    with open(".credentials", "r") as file:
        content = file.read()
    content = content.split(",")
    # Parse credentials from file

    manage_database = ManageBooksDatabase(*content)
    manage_database.create_connection()
    manage_database.insert_book("101", "Joel", "Author2")
    print(manage_database.list_books())

if __name__ == "__main__":
    main()
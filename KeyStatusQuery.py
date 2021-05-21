import argparse

from DarkWebHelpers.db.DB_Handler import SQL_Manger

arg = argparse.ArgumentParser()
arg.add_argument('-s', type=int, help="Query for a specific keyword status")
arg.add_argument('-c', type=str, help="Change process status to off or running")
parser = arg.parse_args()
"""
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int unsigned | NO   | PRI | NULL    | auto_increment |
| key_name    | varchar(255) | NO   |     | NULL    |                |
| user_id     | int          | NO   |     | NULL    |                |
| searched    | int          | NO   |     | 1       |                |
| category_id | int          | YES  |     | NULL    |                |
| created_at  | timestamp    | YES  |     | NULL    |                |
| updated_at  | timestamp    | YES  |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+

"""


class ProcessStatus(SQL_Manger):
    """
    change values in process_status table to control the flow of process
    """

    def ChangeProcessStatus(self, status):
        """Change Process Status"""
        cur, committer = self.my_cursor()
        if isinstance(status, str) and status != 'off' or 'running':
            sql = f"update proccess_state set isactive = '{status.lower()}';"
            cur.execute(sql)
            committer.commit()
            print(f"Process Status Has been changed successfully to [{status}]".title())
        else:
            raise TypeError("Status Must be string and equal to off or running")


class QueryStatus(SQL_Manger):
    """
    query to know the current process status and process statistics
    """

    def __init__(self, status):
        self.status = status
        self.keystatus = {
            1: 'Done',
            2: 'Processing',
            0: 'Waiting'
        }

    def ReadProcessState(self) -> str:
        """:returns the current state of the crawler process"""
        cur, _ = self.my_cursor()
        sql = f"select * from proccess_state;"
        cur.execute(sql)
        status = cur.fetchone()[1]
        return status

    def Keywords_count(self):
        cur, _ = self.my_cursor()
        sql = f"select id from keyword;"
        cur.execute(sql)
        result = cur.fetchall()
        return len(result)

    def GetOwner(self, id):
        """Retrieve the owner of the keyword by ID"""
        cur, _ = self.my_cursor()
        sql = f"select name from users where id = {id};"
        cur.execute(sql)
        result = cur.fetchone()
        return result[0]

    def ReadStatus(self):
        """Read keywords status"""
        results = self.ReadWhere(self.status)
        total_done = len(self.ReadWhere(1))
        total_inProgress = len(self.ReadWhere(2))
        total_waiting = len(self.ReadWhere(0))
        for [key_id, key_name, owner, status, _, _, _] in results:
            print(
                f"[ID: {key_id}, Keyword: {key_name}, Owner: {self.GetOwner(owner)}, Status: {self.keystatus.get(self.status)}]")
        print(
            f'Total Finished: {total_done}\nTotal Waiting: {total_waiting}\nTotal In progress:{total_inProgress}\nProcess Status: {self.ReadProcessState()}\nTotal Keywords: {self.Keywords_count()}')


if parser.s:
    query = QueryStatus(parser.s)
    query.ReadStatus()
elif parser.c:
    ProcessStatus().ChangeProcessStatus(status=str(parser.c))
else:
    query = QueryStatus(0)
    query.ReadStatus()

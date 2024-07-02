from database.DB_connect import DBConnect
from model.state import State


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct(year (`datetime`)) as anno
            from sighting s 
            order by anno desc
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getShapeYear(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct(shape)
            from sighting s 
            where year(`datetime`) = %s
                """
        cursor.execute(query, (year,))
        result = []
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select *
            from state s 
                """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(State(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNeighbors():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select *
            from neighbor n 
                """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append((row["state1"], row["state2"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(u, forma, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select s1.state as stato, count(distinct s1.id) as avvistamenti_stato
            from sighting s1
            where s1.state = %s
                and s1.shape = %s and year(s1.`datetime`) = %s
                """
        cursor.execute(query, (u, forma, anno))
        result = []
        for row in cursor:
            result.append((row["stato"], row["avvistamenti_stato"]))
        cursor.close()
        conn.close()
        return result

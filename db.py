import psycopg2


class DBPOSTGRESQL:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to the database")
        except psycopg2.Error as e:
            raise Exception("Error connecting to the database:", e)


    def get_cursor(self):
        if self.connection.closed:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        return self.connection.cursor()


    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database\n")
    
    
    def get_previous_ip(self):
        query = f"""
            SELECT *
            FROM public_ip;
        """

        try:
            cursor = self.get_cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            if data:
                for ip in data:
                    return ip[0]
            else:
                return []
        except psycopg2.Error as e:
            print("Error fetching data:", e)
            return []


    def update_public_ip(self, public_ip):
        public_ip = public_ip
        query = "UPDATE public.public_ip SET previous_ip = %s;"
        try:
            if self.connection.closed:
                self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, (public_ip,))
            self.connection.commit()
            print(f"Updated Database with {public_ip}")
            self.disconnect()
        except Exception as e:
            print(f"An error occurred: {e}")
   

if __name__ == "__main__":
    pass


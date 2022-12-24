import pymysql
from pythonping import ping
import random
from sshtunnel import SSHTunnelForwarder

# Slave node ips in order from 1 to 3
slave_ips = [ '137.31.80.113', '137.31.43.75', '137.31.12.11' ]

def sendToMaster(sql):
    # Sends a sql request to the master
    # Prints the output
    # sql : the sql request

    with pymysql.connect(host="137.31.65.21", user="proxy", password="8415lab", db="sakila", port="3306", autocommit="true") as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

                data = cursor.fetchall()

                if (len(data) > 0):
                    print([ i[0] for i in cursor.description ])
                    for row in data:
                        print(row)

def sendToSlave(slave_index, sql):
    # Creates a SSH tunnel that forwards all requests going to port 3306 of the master to port 3306 of one of the slaves
    # Then sends a sql request to the master
    # This makes it possible to run sql requests on one of the slave node
    # number : the index of the slave that will run the request
    # sql : the sql request

    with SSHTunnelForwarder (slave_ips[slave_index], ssh_username="ubuntu", ssh_pkey="vockey.pem", remote_bind_address=("137.31.65.21", 3306)) as tunnel:
        sendToMaster(sql)

if __name__ == "__main__":
    # Getting user to chose a proxy implementation
    type = ""
    while type not in ["1","2","3"]:
        print("choose a proxy implementation:")
        print("-- (1) direct hit")
        print("-- (2) random")
        print("-- (3) customized")
        type = input(">>> ")

    while 1:
        # Getting sql from user
        sql = input("(sakila) >>> ").strip()

        # Direct hit implementation
        if type == "1":
            sendToMaster(sql)

        # Random implementation
        elif type == "2":
            if(sql.lower().startswith('select')): # If input type is read, send to a slave
                slave_index = random.randint(0,2)
                print("slave" + slave_index + " read")
                sendToSlave(slave_index, sql)
            else: # If input type is write, send to master
                print("master write")
                sendToMaster(sql)

        # Customized implementation
        elif type == "3":
            if(sql.lower().startswith('select')): # If input type is read, send to a slave
                slave_index = 0
                slave_ping = 9999
                for i in range(3):
                    result = ping(slave_ips[i])
                    print("slave" + i + " : " + str(result.rtt_max_ms))
                    if slave_ping > result.rtt_max_ms:
                        slave_index = i
                        slave_ping = result.rtt_max_ms
                print("slave" + slave_index + " read")
                sendToSlave(slave_index, sql)
            else: # If input type is write, send to master
                print("master write")
                sendToMaster(sql)
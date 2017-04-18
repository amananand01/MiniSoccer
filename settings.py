'''
File used for taking the client and server ip_address from connection.txt
'''
file = open("connection.txt","r")

for line in file.readlines():
    line = line.strip()
    if line.startswith("#"): continue
    if line == "": continue

    try:
        line = line.split(" = ")
        if line[0] == "client_ip":
            client_ip = line[1][1:-1]
        elif line[0] == "server_ip":
            server_ip = line[1][1:-1]
        elif line[0] == "port":
            port = int(line[1])
    except:
        print("Invalid line: \""+line+"\"!")

file.close()

import obd

connection = obd.OBD("/dev/pts/6")

cmd = obd.commands.RPM
while True:
    response = connection.query(cmd)
    print(response.value.magnitude)

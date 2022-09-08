import obd

connection = obd.OBD("/dev/pts/5")

cmd = obd.commands.SPEED

response = connection.query(cmd)

print(response.value)
print(response.value.to("mph"))

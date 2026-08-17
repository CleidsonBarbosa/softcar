import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="", database="softcar")
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM clientes")
print("Clientes:", c.fetchone()[0])

c.execute("SELECT COALESCE(SUM(total), 0) FROM ordem_servico WHERE status = 'finalizado'")
print("Total recebido:", c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'aberto'")
print("Agendados:", c.fetchone()[0])

c.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 'finalizado'")
print("Realizados:", c.fetchone()[0])

c.close()
conn.close()

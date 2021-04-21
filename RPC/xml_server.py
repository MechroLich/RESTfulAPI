from xmlrpc.server import SimpleXMLRPCServer

def temperature(temp):
    if (0 <= temp <= 10):
            return "cold"
    elif(11 <= temp <=20):
        return "warm"
    else:
        return "out of scope of specifications"

server = SimpleXMLRPCServer(("localhost", 8001))
print("Listening on port 8001...")
server.register_function(temperature, "temperature")
server.serve_forever()
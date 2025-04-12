#!/usr/bin/env python3
import argparse
import enum
import shlex
from typing import Optional
from server import Connection, Server

class Interface:
    server: Server
    connections: list[Connection]
    current: Optional[Connection]

    connect_mode: bool

    def __init__(self, server: Server):
        self.server = server
        self.connections = []
        self.current = None
        self.connect_mode = False

        self.setup_parser()

    def setup_parser(self):
        self.parser = argparse.ArgumentParser(
            prog="server",
            description="A not-so-shady server."
        )
        self.subparsers = self.parser.add_subparsers(dest="command", title="Commands")
        
        # Command: list
        list_parser = self.subparsers.add_parser("list", help="Gets the list of connections")

        # Command: set <index>
        set_parser = self.subparsers.add_parser("set", help="Sets connection")
        set_parser.add_argument("index", type=int, help="Index of the connection")

        # Command: get
        get_parser = self.subparsers.add_parser("get", help="Gets current connection")

        # Command: cmd 
        cmd_parser = self.subparsers.add_parser("cmd", help="Sends commands to connected client")
        cmd_parser.add_argument("cmd", type=str, help="The command to send to the client")

    def run_command_line(self, command_line: str):
        """
        Parses a single command line string and executes the corresponding subcommand.
        """
        try:
            args_list = shlex.split(command_line)
        except ValueError as e:
            print(f"Error processing command: {e}")
            return

        if not args_list:
            # Skip empty input.
            return

        try:
            args = self.parser.parse_args(args_list)
        except SystemExit:
            # argparse throws a SystemExit exception on error (e.g., wrong arguments).
            # Catch it here so the interactive loop doesn't exit.
            return

        # command checking
        if args.command == "list":
            self._list()
        elif args.command == "get":
            self._get()
        elif args.command == "set":
            self._set(int(args.index))
        elif args.command == "cmd":
            if not self.connect_mode:
                print("Please choose a connection first")
            else:
                self._cmd(args.cmd)
        else:
            print("Unknown command. Please try again.")

    def run(self):
        print("Interactive CLI started. Type your command (or 'exit'/'quit' to end).")
        while True:
            try:
                self._fetch_connections()
                if self.connect_mode:
                    command_line = input(f"[{self.current.address}] >> ")
                else:
                    command_line = input(">> ")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting interactive CLI.")
                break

            if command_line.strip().lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            if command_line.strip():
                self.run_command_line(command_line)

    def _fetch_connections(self):
        self.connections = self.server.get_connections()

    def _list(self):
        for index, connection in enumerate(self.connections):
            print(f"{index} - {connection.address}")

    def _get(self):
        if not self.current:
            print("No current connections")
            return

        print(f"Current - {self.current.address}")

    def _set(self, index: int):
        self.connect_mode = True
        self.current = self.connections[index]
        print(f"Current - {self.current.address}")

    def _cmd(self, cmd: str):
        self.current.connection.send(cmd.encode())
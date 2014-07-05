import socket
import sys
import subprocess
import time
import random


HOST = "5.135.165.34"
PORT = "27001"


class UrTBulbula:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    @staticmethod
    def say(message):
        print message
        subprocess.call(['say', message])

    def say_random_message(self):
        #self.say("There was an error")
        messages = [
            "Are you connected to the internet?",
            "Please check server details",
            "Can not connect to the internet",
            "Is the server up?",
            "What happened to me?",
            "Why can't I just connect?",
            "Damn though internet!"
        ]
        msg = random.choice(messages)
        self.say(msg)
        secs = random.randint(0, 30)
        self.say("Retrying in " + str(secs) + " seconds")
        time.sleep(secs)


    def start_monitoring(self):
        try:
            if not self.server:
                self.server = self.get_server_details()
                self.say("I have started monitoring the server")
                self.say(str(len(self.server['players'])) + " players are now playing")
            while True:
                old_players = [player['name'] for player in self.server['players']]
                print old_players
                self.server = self.get_server_details()
                current_players = [player['name'] for player in self.server['players']]
                print current_players
                new_players = []

                for player in current_players:
                    if player not in old_players:
                        new_players.append(player)

                if len(new_players) > 0:
                    if len(new_players) == 1:
                        self.say(new_players[0] + " has joined server")
                    else:
                        self.say(str(len(new_players)) + " new players have joined server")

                time.sleep(3)
        except Exception, ex:
            self.say_random_message()
            self.start_monitoring()

    def get_server_details(self):
        # Data Place Holders
        urt_server_details = {}

        # Socket Request Message
        MESSAGE = "\377\377\377\377getstatus"

        # Get response from server
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            sock.connect((self.host, int(self.port)))
            sock.send(MESSAGE)
            response, addr = sock.recvfrom(1024)
            sock.close()
            response_lines = response.split("\n")
        except Exception, exc:
            raise exc

        # Retrieve the server settings
        config_string_parts = response_lines[1].split("\\")
        urt_server_details['configs'] = {}
        for i in range(1, len(config_string_parts), 2):
            urt_server_details['configs'][config_string_parts[i].strip()] = config_string_parts[i + 1].strip()

        urt_server_details['players'] = []
        for x in range(2, (len(response_lines) - 1)):
            player_data = response_lines[x].split(" ")
            player_dictionary = {"ping": player_data[1], "score": player_data[0], "name": player_data[2][1:-1]}
            urt_server_details['players'].append(player_dictionary)

        return urt_server_details


if __name__ == "__main__":
    bulbula = UrTBulbula(HOST, PORT)
    try:
        bulbula.start_monitoring()
    except KeyboardInterrupt:
        bulbula.say("Bye Bye!")
class Logger:

    @staticmethod
    def log_command(author, command):
        with open("command_logs", "a+") as f:
            f.write(f"{author.name} used command {command}\n")

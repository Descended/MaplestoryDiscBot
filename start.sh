#!/bin/bash
# This script allows the user to launch the bot without needing to learn command line
# This script allows the user to choose between global and virtual python environment
echo "This script will launch the Discord bot."

PWD=`pwd`
activate () {
	. $PWD/venv/bin/activate
}

PS3="Please select the environment to run the source code with: "
options=("Virtual Python Environment" "Global Python Environment" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "${options[0]}")
            echo "Now starting: $opt $REPLY"
			activate
			python3 src/main.py
            ;;
        "${options[1]}")
            echo "Now starting: $opt $REPLY"
			python3 src/main.py
            ;;
        "${options[2]}")
            echo "Now terminating..."
			break
            ;;
        *) echo "invalid option $REPLY - try again!";continue;;
    esac
done
read -rsp $'Press any key to continue...\n' -n1 key
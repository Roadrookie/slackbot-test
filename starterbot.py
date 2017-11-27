import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
startnew_windows = """>cd into project folder 
`virtualenv env` - Here you are creating the virtual environment

`env\scripts\\activate` - Here you are starting the virtual environment

`pip install blah-blah` - When you run a pip install the added module will only be added to the virtual environment


>create .gitignore file
>
>add env/ and .git to .gitignore file - By creating a .gitignore file you are telling git not to upload certain items in this case the folder env and the hidden .git folder 
>
>
>
># Pushing to github
>
>To start new blank github project
>(from project folder)


`git init` - Initiating Git in this directory

`git add .` - Adding all the files and folders in your project folder to what git will be 

`git commit -m "first commit"` - This is a message that describes what was changed before uploading

`git remote add origin https://github.com/<username>/<repo-name>.git` - This is telling git where to upload to and giving it the nickname of \"orgin\" in this case

`git push -u origin master` - This command is making the actual upload to the place and branch you specified (Here \"origin\" is the nickname of the place to upload and \"master\" is the branch)
"""



# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    if command.startswith("startproject windows"):
    	response = startnew_windows
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("rrnetbot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
"""

 Bot Slash Command Python3
 Hanif Dwy Putra S

"""


"""
 .env
 
 CLIENT_KEY = PUBLIC KEY
 CLIENT_ID = APPLICATION ID
 CLIENT_TOKEN = BOT TOKEN

"""

from Interaction import verifyKeyDecorator, InteractionType, InteractionResponseType
from flask import Flask, jsonify, request
from os import getenv
import requests

app = Flask(__name__)
CLIENT_KEY = getenv('key')
CLIENT_ID = getenv('id')
CLIENT_TOKEN = getenv('secret')

interactions = [{
  "name": "hai",
  "content": "Hai juga !!",
  "description": "Mengucap hai juga"
}]

def printHeaders(tokenType: str, token: str) -> object:
  return { "Authorization": f"{tokenType} {token}", "Content-Type": "application/json" }

def getApplicationURL():
  return f"https://discord.com/api/v8/applications/{CLIENT_ID}/commands"

# Register commands
for interact in interactions:
  commandName: str = interact['name']
  commandDesc: str = interact['description']
  
  data = {
    "name": commandName,
    "description": commandDesc
  }
  headers = printHeaders("Bot", CLIENT_TOKEN)
  response = requests.post(getApplicationURL(), headers=headers, json=data)
  if response.reason.lower() == "created":
    print(f"Command {commandName} sukses di register, tunggu sekitar 30 menit untuk digunakan!\nStatus Code: {response.status_code}")
  elif response.reason.lower() == "ok":
    print(f"Command {commandName} telah dibuat, command ini akan di overwrite!")
  else:
    print(f"Command {commandName} gagal di register: {response.reason}\nStatus Code: {response.status_code}")
  break
else:
  print('Command tidak ditemukan!')


@app.route("/interaction/<command_name>", methods=['GET'])
def get_command(command_name):
  for interact in interactions:
    if interact['name'] == str(command_name):
      return jsonify({
        "success": True,
        "result": interact
      })
    else:
      return jsonify({
        "success": False,
        "result": {}
      })

@app.route("/interactions", methods=['POST'])
@verifyKeyDecorator(CLIENT_KEY)
def interactions_post():
  if request.json['type'] == InteractionType.APPLICATION_COMMAND:
    # Handle commands
    for interact in interactions:
      inteName = request.json['data']['name']
      if interact['name'] == inteName:
        if interact.get('embeds'):
          return jsonify({
            "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
              "embeds": interact['embeds']
            }
          })
        elif interact['content']:
          return jsonify({
            "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
              "content": interact['content']
            }
          })
    else:
      print(f"Command {request.json['data']['name']} tidak ada!")


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
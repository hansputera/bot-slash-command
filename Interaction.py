from functools import wraps

# Nacl
from nacl.signing import VerifyKey

# Interaction Type

class InteractionType:
  PING = 1
  APPLICATION_COMMAND = 2

class InteractionResponseType:
  PONG = 1
  ACK = 2
  CHANNEL_MESSAGE = 3
  CHANNEL_MESSAGE_WITH_SOURCE = 4
  ACK_WITH_SOURCE = 5

class InteractionResponseFlags:
  EPHEMERAL = 1 << 6

def verifyKey(raw_body: str, signature: str, timestamp: str, public_key: str) -> bool:
  message = timestamp.encode() + raw_body
  try:
    vk = VerifyKey(bytes.fromhex(public_key))
    vk.verify(message, bytes.fromhex(signature))
    return True
  except Exception as ex:
    print(ex)
  return False

def verifyKeyDecorator(public_key: str):
  from flask import request, jsonify

  def decorator(f):
    @wraps(f)
    def _decorator(*args, **kwargs):
      signature = request.headers['X-Signature-Ed25519']
      timestamp = request.headers['X-Signature-Timestamp']
      if signature is None or timestamp is None or not verifyKey(request.data, signature, timestamp, public_key):
        return 'Bad request signature!', 401 # Forbidden
      
      if request.json and request.json['type'] == InteractionType.PING:
        print("Pong!")
        return jsonify({
          "type": InteractionResponseType.PONG
        })
      
      return f(*args, **kwargs)
    return _decorator
  return decorator
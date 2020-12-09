import json
import subprocess
import re

from pprint import pprint
from time import sleep

def get_all_queues_from_rabbitmq_a():
  out = subprocess.check_output("""
  ./rabbitmqadmin -c config.conf -N rabbitmq_a  --format pretty_json  list queues 
  """, shell=True)

  return json.loads(out.decode())

def declare_rabbitmq_b_queue(queue):
  if queue["durable"] == True:
    queue["durable"] = "true"
  if queue["durable"] == False:
    queue["durable"] = "false"
  out = subprocess.check_output("""
  ./rabbitmqadmin -c config.conf -N rabbitmq_b --vhost {vhost} declare queue name={name} durable={durable} queue_type={type}
  """.format(**queue), shell=True)

  print(out.decode("utf-8"), end='')

def declare_upstream_for_rabbitmq_b(queue):
  if queue["vhost"] == "/":
    vhost_uri = "%2F"
  else:
    vhost_uri = queue["vhost"]

  out = subprocess.check_output("""
  ./rabbitmqadmin -c config.conf -N rabbitmq_b declare parameter component=federation-upstream \
    --vhost {vhost} name=rabbitmq_a_{queue} \
    value='{{"uri":"amqp://guest:guest@rabbitmq_a:5672/{vhost_uri}","prefetch-count":100,"reconnect-delay":5,"trust-user-id": true, "queue":"{queue}"}}'
  """.format(queue=queue["name"], vhost=queue["vhost"], vhost_uri=vhost_uri), shell=True)

  print(out.decode("utf-8"), end='')

def declare_upstream_for_rabbitmq_a(queue):
  if queue["vhost"] == "/":
    vhost_uri = "%2F"
  else:
    vhost_uri = queue["vhost"]

  out = subprocess.check_output("""
  ./rabbitmqadmin -c config.conf -N rabbitmq_a declare parameter component=federation-upstream \
   --vhost {vhost} name=rabbitmq_b_{queue} \
   value='{{"uri": "amqp://guest:guest@rabbitmq_b:5672/{vhost_uri}", "prefetch-count": 100, "reconnect-delay": 5, "trust-user-id": true, "queue": "{queue}"}}'
  """.format(queue=queue["name"], vhost=queue["vhost"], vhost_uri=vhost_uri), shell=True)

  print(out.decode("utf-8"), end='')

def declare_rabbitmq_b_policy(queue):
  
  policy = {
    "federation-upstream": "rabbitmq_a_" + queue["name"], 
    "ha-mode": "exactly", 
    "ha-params": 2, 
    "ha-sync-mode": "automatic"
    }

  queue["policy"] = json.dumps(policy)

  out = subprocess.check_output("""
  ./rabbitmqadmin -c config.conf -N rabbitmq_b --vhost {vhost} declare policy name=fed_{name} pattern='^{name}$' priority=1 apply-to=queues definition='{policy}'
  """.format(**queue), shell=True)

  print(out.decode("utf-8"), end='')

def declare_rabbitmq_a_policy(queue):

  policy = {
    "federation-upstream": "rabbitmq_b_" + queue["name"], 
    "ha-mode": "exactly", 
    "ha-params": 2, 
    "ha-sync-mode": "automatic"
    }


  queue["policy"] = json.dumps(policy)

  out = subprocess.check_output("""
  ./rabbitmqadmin -c config.conf -N rabbitmq_a --vhost {vhost} declare policy name=fed_{name} pattern='^{name}$' priority=1 apply-to=queues definition='{policy}'
  """.format(**queue), shell=True)

  print(out.decode("utf-8"), end='')


queues = get_all_queues_from_rabbitmq_a()

for q in queues:
  if q["name"] == "aliveness-test":
    continue

  print("working on '{}' queue on {} vhost".format(q["name"], q["vhost"]))

  while True:
    try:
      declare_rabbitmq_b_queue(q)
      
      declare_upstream_for_rabbitmq_b(q)
      declare_upstream_for_rabbitmq_a(q)

      declare_rabbitmq_b_policy(q)
      declare_rabbitmq_a_policy(q)
  
      break
    except:
      print("Error, sleeping...")
      sleep(5)
    
  # sleep(1)
  
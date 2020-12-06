# [Day 1] Web Exploitation A Christmas Crisis
After deploying the machine we browse to the assigned IP-address.
Here we're presented with a login screen.

Here we register a user called `test` with the password `test1`.
After registering as a user we log in and take a look at our browser storage (`Shift+F9` in Firefox).
Here we can see a single cookie, this must be the cookie used for authentication. The name of this cookie is the answer to question 1.

Mine has a value of:
```
7b22636f6d70616e79223a22546865204265737420466573746976616c20436f6d70616e79222c2022757365726e616d65223a2274657374227d
```

By going to the website [CyberChef](https://gchq.github.io/CyberChef/), we can use their [magic-tool](https://gchq.github.io/CyberChef/#recipe=Magic(3,false,false,'')) and try to recognize the encoding of the authentication cookie.
The magic tool recognizes the cookie value as hex. The answer to question 2 is the full name of the type of encoding.

Decoding the value gives us the string:
```
{"company":"The Best Festival Company", "username":"test"}
```
Given that the hint tells us that this format is often linked to JavaScript, we might look into JavaScript's default object notation. Googling this we quickly find the answer to question 3.

We then take the decoded cookie and change the username to `santa`.
```
{"company":"The Best Festival Company", "username":"santa"}
```
We can now encode it again with [CyberChef](https://gchq.github.io/CyberChef/#recipe=To_Hex('None',0)&input=eyJjb21wYW55IjoiVGhlIEJlc3QgRmVzdGl2YWwgQ29tcGFueSIsICJ1c2VybmFtZSI6InNhbnRhIn0) and we get:
```
7b22636f6d70616e*****227d
```
This is the answer to question 4.

If we change our own cookie in the browser with this we might become the user `santa`.

Opening the storage in our browser and changing the cookie value and reloading the page presents us with toggle switches for Santa's assembly line!
Toggling the all on reveals the final flag.

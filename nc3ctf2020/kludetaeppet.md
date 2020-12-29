# Kludetæppet
We get the code:
```
ting = ["nc3", "gjort", "{", "specielt", "}", "_", "selv", "vel", "jule", "er", "med", "gaver", "guld"]

opskrift = [1, 3, 7, 2, 6, 10, 6, 8, 2, 6, 4, 6, 11, 6, 9, 12, 5]

kludeTaeppe = ''
for tal in opskrift :
    t = ting[tal]
    kludeTaeppe += t

print kludeTaeppe
```
Running it yields:
```
gjortspecieltvel{selvmedselvjule{selv}selvgaverselverguld_

```
We know that the first part f the flag is `nc3`. 
By looking at `opskrift` we see that were grabbing the second element and not the first i.e. `gjort` instead of `nc3`.
A classical of by one bug. If we subtract 1 from all the elements of `opskrift` we get:
```
ting = ["nc3", "gjort", "{", "specielt", "}", "_", "selv", "vel", "jule", "er", "med", "gaver", "guld"]

opskrift = [1, 3, 7, 2, 6, 10, 6, 8, 2, 6, 4, 6, 11, 6, 9, 12, 5]
opskrift = [x-1 for x in opskrift]

kludeTaeppe = ''
for tal in opskrift :
    t = ting[tal]
    kludeTaeppe += t

print(kludeTaeppe)
```
Running it yields:
```
nc3{selvgjort_er_velgjort_specielt_med_julegaver}
```

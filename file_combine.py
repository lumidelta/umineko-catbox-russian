new = open('script_original.rb','r')
old = open('script_replace.rb','r')
f3 = open('script_result.rb','w')
a = 375233
b = 379823
lines1 = old.readlines()
lines2 = new.readlines()
for i in range(len(lines1)):
    if i in range(a, b):
        f3.write(lines2[i])
    else:
        f3.write(lines1[i])
old.close()
new.close()
f3.close()

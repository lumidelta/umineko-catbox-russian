a = 171177
b = 171561
lin = open("script_extracted.rb", "r").readlines()[a:b]
fout = open("slice.rb", "w")
for i in lin:
    fout.write(i)

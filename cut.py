a = 99604
b = 115931
lin = open("script_extracted.rb", "r").readlines()[a:b]
fout = open("slice.rb", "w")
for i in lin:
    fout.write(i)

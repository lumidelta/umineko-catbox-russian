ru = open('script_ru.rb', 'r', encoding="utf-8")
en = open('script_en.rb', 'r', encoding="utf-8")
ru_out = open('diff_ru.txt', 'w', encoding="utf-8")
en_out = open('diff_en.txt', 'w', encoding="utf-8")
# script = open('script_ru.rb', 'w', encoding="utf-8")
ru_data = ru.readlines()
en_data = en.readlines()
for num in range(len(en_data)):
    if (ru_data[num] != en_data[num] and not ru_data[num].startswith("s.ins 0x86")):
        ru_out.write(ru_data[num])
        en_out.write(en_data[num])
        # script.write(en_data[num])
    # else:
        # script.write(ru_data[num])
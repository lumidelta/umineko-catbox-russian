ru = open('script.rb', 'r', encoding="utf-8")
en = open('script_en.rb', 'r', encoding="utf-8")
ru_out = open('diff_ru.txt', 'w', encoding="utf-8")
en_out = open('diff_en.txt', 'w', encoding="utf-8")
ru_data = ru.readlines()
en_data = en.readlines()
for num in range(len(en_data)):
    if (ru_data[num] != en_data[num]):
        ru_out.write(ru_data[num])
        en_out.write(en_data[num])
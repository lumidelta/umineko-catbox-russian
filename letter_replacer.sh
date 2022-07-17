cd /mnt/c/Users/lumidelta/Desktop/letter/
for filename in *.png; do file=$(echo $filename | sed 's/\..*$//'); /home/lumidelta/umineko-catbox-russian/enter_extractor/build/EnterExtractor /home/lumidelta/umineko-catbox-russian/romfs/picture/$file.pic /home/lumidelta/umineko-catbox-russian/romfs/picture/$file.pic1 -replace $file.png ; done
cd /home/lumidelta/umineko-catbox-russian/romfs/picture
for file in b*.pic; do mv $file $file.bu; done;
for filename in *.pic1; do file=$(echo $filename | sed 's/\..*$//'); cp $file.pic1 $file.pic;  done
cd /home/lumidelta/umineko-catbox-russian
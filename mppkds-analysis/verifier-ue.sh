#rm -r ./org-msgs
#rm -r ./dig-sigs

VM_IP=159.203.10.136
File_IDs=$(seq 1000 1000 100000)

mkdir ./msgs

# Downloading Original Messages
for numLines in $File_IDs; do
  file="$VM_IP:~/msgs/${numLines}.txt"
  scp  $file ./msgs/
done  
  

# Logging
EXP_ID="2024-02-14-verifier-log-LAN.csv";
echo "" > $EXP_ID
echo "File Name, Transporting time (ms), Verifiying time (ms)" > $EXP_ID

mkdir ./dig-sigs

for numLines in $File_IDs; do
  file="$VM_IP:~/msgs/${numLines}_dig_sig.json"
  echo "${file##*/}," | tr -d "\n" >> $EXP_ID
  
  # Downloading digital signatures from cloud VM
  TMP=$(mktemp)
  time (scp  $file ./dig-sigs/) 2>$TMP
  awk -F'[ ms]+' '/^real/ {print 1000*$2}' $TMP | tr -d "\n" >> $EXP_ID
  rm $TMP

 # Verifying Process
 TMP=$(mktemp)
 time (python3 verify.py "./msgs/$numLines.txt" "./dig-sigs/${file##*/}") 2>$TMP
 awk -F'[ ms]+' '/^real/ {print "," 1000*$2}' $TMP >> $EXP_ID
 rm $TMP

done

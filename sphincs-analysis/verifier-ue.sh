VM_IP=68.183.198.206

File_IDs=$(seq 1000 1000 100000)

mkdir ./dig_sigs

# Downloading Hash Values
for numLines in $File_IDs; do
  file="$VM_IP:~/sphinx/msgs/${numLines}_HashValue.json"
  scp  $file ./dig_sigs/
done  
  

# Logging
EXP_ID="2023-03-24-VerifierLog-Labtop-5G.csv";
echo "" > $EXP_ID
echo "File Name, Transporting time, Verifiying time" > $EXP_ID



for numLines in $File_IDs; do
  file="$VM_IP:~/sphinx/msgs/${numLines}_DigSig.json"
  echo "${file##*/}," | tr -d "\n" >> $EXP_ID
  
  # Downloading digital signature from cloud VM
  TMP=$(mktemp)
  time (scp  $file ./dig_sigs/) 2>$TMP
  awk -F'[ ms]+' '/^real/ {print 1000*$2}' $TMP | tr -d "\n" >> $EXP_ID
  rm $TMP

 # Verifying Process
 TMP=$(mktemp)
 time (python3 SphinxVerify.py "./dig_sigs/${numLines}_HashValue.json" "./dig_sigs/${numLines}_DigSig.json") 2>$TMP
 awk -F'[ ms]+' '/^real/ {print "," 1000*$2}' $TMP >> $EXP_ID
 rm $TMP

done

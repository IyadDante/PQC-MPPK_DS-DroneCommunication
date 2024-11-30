VM_IP=137.184.162.133
File_IDs=$(seq 1000 1000 100000)

mkdir ./dig_sigs

# Downloading Original Messages
for numLines in $File_IDs; do
  file="$VM_IP:~/rsa/msgs/${numLines}_mu_int.json"
  scp  $file ./dig_sigs/
done  
  

# Logging
EXP_ID="2023-03-22-verifier-Log-Labtop-5G.csv";
echo "" > $EXP_ID
echo "File Name, Transporting time (ms), Verifiying time (ms)" > $EXP_ID



for numLines in $File_IDs; do
  file="$VM_IP:~/rsa/msgs/${numLines}_dig_sig.json"
  echo "${file##*/}," | tr -d "\n" >> $EXP_ID
  
  # Downloading digital signature from cloud VM
  TMP=$(mktemp)
  time (scp  $file ./dig_sigs/) 2>$TMP
  awk -F'[ ms]+' '/^real/ {print 1000*$2}' $TMP | tr -d "\n" >> $EXP_ID
  rm $TMP

 # Verifying Process
 TMP=$(mktemp)
 time (python3 RSA_verify.py "./dig_sigs/${numLines}_mu_int.json" "./dig_sigs/${numLines}_dig_sig.json") 2>$TMP
 awk -F'[ ms]+' '/^real/ {print "," 1000*$2}' $TMP >> $EXP_ID
 rm $TMP

# sleep 30

done

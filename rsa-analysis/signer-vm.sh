# Created on Tue Mar 21
# @author: mohammed


# Generating Random Text Messages
#mkdir ./msgs
#for numLines in $(seq 1000 1000 100000); do
#tr -dc "A-Za-z 0-9" < /dev/urandom | fold -w100|head -n $numLines > "./msgs/$numLines.txt"
#done

# Logging
EXP_ID="2023-03-22-signer-log.csv";
echo "" > $EXP_ID
echo "Msg File Name, Msg size (B), Signing time (ms)" > $EXP_ID

# Signing Process
FILES="./msgs/*"

for file in $FILES; do
  echo "${file##*/}," | tr -d "\n" >> $EXP_ID
  wc -c $file | awk '{print $1}' | tr -d "\n" >> $EXP_ID
  TMP=$(mktemp)
  time (python3 RSA_sign.py $file) 2>$TMP
  awk -F'[ ms]+' '/^real/ {print "," 1000*$2}' $TMP >> $EXP_ID
  rm $TMP
done


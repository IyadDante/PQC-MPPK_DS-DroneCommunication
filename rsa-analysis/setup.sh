#Step 1: Initilization on Signer and Verifier sides
apt-get update
apt install -y python3-numpy
mkdir ./rsa

#Step 2: Upload the following files to the Singer side, 

VM_IP=137.184.162.133

scp RSAprivate_key.json RSA_sign.py signer-vm.sh $VM_IP:~/rsa/

scp RSAprivate_key.json $VM_IP:~/rsa/
scp RSA_sign.py $VM_IP:~/rsa/


#Step 3: Run the signer-vm.sh

#Step 4: Run the verifier-ue.sh

#Step 5: Download the signer results
scp $VM_IP:~/rsa/*.csv ./

#Step 1.0: Initilization on Signer and Verifier sides
apt install -y python3-numpy


#Step 1.1: Generate the key pairs using the PQC algorithm
python3 keygen.py


# If you genkey outside cloud, then you need this Step 2: Upload the following files to the Singer side, 
# export VM_IP=159.203.10.136
# scp private_key.json sign.py signer-vm.sh $VM_IP:~/



#Step 3: Run the signer-vm.sh
bash signer-vm.sh

#Step 4: Run the verifier-ue.sh
bash verifier-ue.sh

#Step 5: Download the signer results
scp $VM_IP:~/*.csv ./

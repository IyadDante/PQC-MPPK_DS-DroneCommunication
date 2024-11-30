#Step 1: Initilization on Signer and Verifier sides
apt-get update
apt install -y python3-numpy
apt install -y python3-pip
pip install pyspx
mkdir ./sphinx

#Step 2: From your machine, Upload the following files to the cloud vm, 
VM_IP=165.22.228.137
scp SphincsPrivateKey.json SphinxSign.py signer-vm.sh $VM_IP:~/sphinx/


#Step 3: Run the signer-vm.sh

#Step 4: Run the verifier-ue.sh

#Step 5: Download the signer results
scp $VM_IP:~/sphinx/*.csv ./



nano ~/.ssh/authorized_keys


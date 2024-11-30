# Analysis on MPPK-DS Algorithm

This repository presents a detailed analysis and implementation of the Multivariate Polynomial Public Key Digital Signature (MPPK/DS) algorithm. Originally proposed by Randy Kuang, Maria Perepechaenko, and Michel Barbeau in their work "A new quantum-safe multivariate polynomial public key digital signature algorithm," MPPK/DS offers a quantum-safe digital signature solution based on modular arithmetic in prime Galois fields. This project includes Python-coded algorithms for key generation, signing, and verification processes, along with performance recording under different scenarios.

## Abstract

The advent of quantum computing poses significant challenges to classical encryption methodologies. With the National Institute of Standards and Technology (NIST) spearheading the development and standardization of Post Quantum Cryptography (PQC) algorithms, our study focuses on the Multivariate Polynomial Public Key (MPPK) Digital Signature (DS) algorithm. We explore the generation of MPPK/DS key pairs using true random numbers from quantum computers, evaluate the robustness of these key pairs through semi-covariance correlation analysis, and assess latency performance across various networks. Our findings indicate superior robustness and performance of MPPK/DS over traditional RSA and SPHINCS algorithms, underscoring its potential as a viable PQC solution.

## Setup and Installation

To replicate our environment and results, follow the steps below:

### Prerequisites

- Python 3
- Numpy library

### Installation

1. Initialize the environment on both the signer and verifier sides:

    ```bash
    apt install -y python3-numpy
    ```

2. Generate key pairs using the MPPK/DS algorithm:

    ```bash
    python3 keygen.py
    ```

### Usage

1. Transfer necessary files to the signer side:

    ```bash
    export VM_IP=159.203.10.136
    scp private_key.json sign.py signer-vm.sh $VM_IP:~/
    ```

2. Execute the signing process:

    ```bash
    bash signer-vm.sh
    ```

3. Execute the verification process:

    ```bash
    bash verifier-ue.sh
    ```

4. Download the results:

    ```bash
    scp $VM_IP:~/*.csv ./
    ```

## Conclusion and Future Work

Our analysis confirms the robustness of MPPK/DS key pairs over RSA and SPHINCS through semi-covariance analysis. The end-to-end latency measurements suggest that hardware and network access significantly influence performance. Future directions include exploring larger prime numbers for key generation, segmenting messages for enhanced security, and assessing signing frequency's impact on latency. We aim to contribute further to the PQC field by examining various factors influencing key generation and algorithm efficiency.

## Citation

To cite our work, please use the following reference:


```latex
  @INPROCEEDINGS{10187725,
  author={Singh Lakhan, Atinderpal and Abuibaid, Mohammed and Steed Huang, Jun and Taha, Mostafa and Wang, Zhehan},
  booktitle={2023 19th International Conference on Wireless and Mobile Computing, Networking and Communications (WiMob)}, 
  title={Multivariate Polynomial Public Key Digital Signature Algorithm: Semi-covariance Analysis and Performance Test over 5G Networks}, 
  year={2023},
  volume={},
  number={},
  pages={299-305},
  keywords={Computers;Wireless communication;Quantum computing;Uncertainty;5G mobile communication;Public key;Robustness;MPPK;PQC;RSA;SPHINCS},
  doi={10.1109/WiMob58348.2023.10187725}}
  ```

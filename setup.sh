#!/bin/bash
# Linux Flavour : Debian
# Check for presence of conda
if ! command -v apt &>/dev/null
then
    echo Not a supported distribution. This is only applicable for Ubuntu 16.04 and above
    exit 1
fi

# For some parts, sudo privileges are required. Check if current user has privileges, and if not, which user to utilize.
if [ `id -u` -ne 0 ]
then
    echo Certain segments require an elevated account. Please enter the credentials for an account with them.
    read -p "Admin Username : " admin_user
    read -sp "Password : " admin_pass
    echo
fi

# Install conda for secured python environment management
if ! command -v conda &>/dev/null
then
    echo Installing conda. Please select yes for all.
    if [ -z ${admin_user+x} ]
    then
        sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
    else
        su -c "echo $admin_pass| sudo -S apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6" $admin_user
        cat /dev/null > ~/.bash_history && history -c
    fi
    curl -O https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
    bash Anaconda3-2024.02-1-Linux-x86_64.sh
    echo conda install complete. Activating conda.
    source ~/.bashrc
    conda init
fi

# Setup Conda Environment
if ! command -v conda &>/dev/null
then
    echo Conda installation may not have completed succesfully. Kindly verify that conda is installed, initialized and activated. Run this file once done. >&2
    exit 1
else
    echo Installing espeak-ng portaudio19-dev
    if [ -z ${admin_user+x} ]
    then
        sudo apt install espeak-ng portaudio19-dev
    else
        su -c "echo $admin_pass| sudo -S apt install -y espeak-ng portaudio19-dev" $admin_user
        cat /dev/null > ~/.bash_history && history -c
    fi
    if [ $? -ne 0 ]
    then
        echo "Installations did not succeed" >&2
        exit 1
    fi
    # Commons : PyTorch, CUDA, NVCC
    # Data Manager : Transformer
    # For TTS : tts, pyaudio
    # For Chat : accelerate
    conda config --append channels conda-forge
    conda create --name genaienv
    eval "$(conda shell.bash hook)"
    conda activate genaienv
    conda install --name genaienv -c nvidia cuda-nvcc
    conda install --name genaienv -c "nvidia/label/cuda-11.3.0" cuda-nvcc
    conda install --name genaienv -c anaconda cudatoolkit
    conda install --name genaienv pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
    conda install --name genaienv fastapi pyaudio accelerate transformers
    pip install .
    cat /dev/null > ~/.bash_history && history -c
fi

# Install redis
curl -o ~/Downloads/redis-7.2.4.tar.gz https://github.com/redis/redis/archive/7.2.4.tar.gz
mkdir -p ~/install/redis-7.2.4
tar -xvzf ~/Downloads/redis-7.2.4.tar.gz -C ~/install/redis-7.2.4
cd ~/install/redis-7.2.4
make
echo Start the redis server by running the program redis-server at ~/install/redis-7.2.4/src


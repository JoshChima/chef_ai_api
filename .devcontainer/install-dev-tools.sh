# update system
apt-get update
apt-get upgrade -y

apt-get install ffmpeg -y

# conda init -y
conda install python=3.12 -y
conda init
# pip install pytubefix openai-whisper ipykernel langchain langchain-openai

# # clean up
# pip cache purge
# apt-get autoremove -y
# apt-get clean







# # update system
# apt-get update
# apt-get upgrade -y

# which sudo || apt-get install sudo -y

# apt-get install software-properties-common wget curl -y

# sudo apt update
# sudo apt upgrade

# sudo add-apt-repository ppa:deadsnakes/ppa -y
# sudo apt update

# sudo apt install python3.12 -y
# python3.12 --version


# # install Linux tools and Python 3

# apt-get install python3-dev python3-pip python3-wheel python3-setuptools -y

# sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
# sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 2

# sudo update-alternatives --config python

# # apt-get install software-properties-common wget curl \
# #     python3-dev python3-pip python3-wheel python3-setuptools -y

# # install Python packages
# python -m pip install --upgrade pip
# pip3 install --user -r .devcontainer/requirements.txt
# # update CUDA Linux GPG repository key
# wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
# dpkg -i cuda-keyring_1.0-1_all.deb
# rm cuda-keyring_1.0-1_all.deb
# # install cuDNN
# wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
# mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
# apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
# add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /" -y
# apt-get update
# apt-get install libcudnn8=8.9.0.*-1+cuda11.8
# apt-get install libcudnn8-dev=8.9.0.*-1+cuda11.8
# # install recommended packages
# apt-get install zlib1g g++ freeglut3-dev \
#     libx11-dev libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev libfreeimage-dev -y
# # Install ffmpeg
# apt-get install -y ffmpeg
# # clean up
# pip3 cache purge
# apt-get autoremove -y
# apt-get clean
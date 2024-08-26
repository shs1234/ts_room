apt update
apt install -y docker docker-compose make python3-pip python3-django zsh
pip3 install --no-cache-dir -r ./requirements.txt
git config --global user.email "shs@shs.shs"
git config --global user.name "shs"
chmod 777 /var/run/docker.sock
sudo ufw enable
sudo ufw allow 8000
sudo ufw allow 22
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# plugins=( 
#     # other plugins...
#     zsh-autosuggestions
# )
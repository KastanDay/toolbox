# Setting up an AI machine (setup nvidia box)

Keywords: cuda install, fresh nvidia box, fresh server install

# Nvidia

See [My Server (Home Server & Home Network & Personal Server)](https://www.notion.so/My-Server-Home-Server-Home-Network-Personal-Server-5ae7682b5a9f424b99ad4b6378344c2d) 

Official docs: [Installation Guide Linux :: CUDA Toolkit Documentation (nvidia.com)](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu-installation-prepare)

************************************Table of Contents:************************************

# Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

Add github ssh keys

```bash
# THIS IS ONE COMMAND for github keys

curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```

# Pytorch

Use conda

```python
conda install pytorch torchvision torchaudio cudatoolkit=11.7 -c pytorch -c conda-forge
```

```python
pip install transformers datasets

# ❌ Conda is NOT ADVISED, pip is more stable: conda install -c huggingface transformers
```

- Using HF Hub easily 🙂  [For downloading files to local (guide)](https://huggingface.co/docs/huggingface_hub/how-to-downstream).
    
    ```python
    # part of conda install transformers
    python -m pip install huggingface_hub
    ```
    
    Usage
    
    ```python
    from huggingface_hub import hf_hub_download
    
    hf_hub_download(repo_id="bigscience/T0_3B", filename="config.json", cache_dir="./your/path/bigscience_t0")
    
    # Once your file is downloaded and locally cached, specify it’s local path to load and use it:
    from transformers import AutoConfig
    config = AutoConfig.from_pretrained("./your/path/bigscience_t0/config.json")
    ```
    

# Nvidia Driver & Cuda Install

[Install Nvidia Driver (and Cuda)](https://www.notion.so/Install-Nvidia-Driver-and-Cuda-91233309a4a948eeaad2a853427dfdcd)

# Storage

## **How to expand size of lvm partition**

Verified to work on Ubuntu 22 server on Unraid. 

```python
# (optional) check general filesystem
sudo df -h

# (optional) Check virtual filessytem
sudo vgdisplay

# (1/2) Increase block volume of root filesystem
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv

# (2/2) Extend your filesystem
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv

# confirm success with glances 
```

## Increase swap space

Works great. It’s ok to run repeatedly if necessary, and it’s fine if you have existing swap, just adds to it.

```bash
sudo fallocate -l 24G /swapfile

sudo mkswap /swapfile

sudo swapon /swapfile
```

## Add UnRaid mount points

Add these bottom 2 lines. Corresponding to the mount points in unraid gui. 

CRUCIAL NOTE: You also have to export these during the VM creation process when using GPU passthrough. After Nvidia realizes it’s inside a VM I think it gets mad and doesn’t let you add storage. You cannot use “floating/soft/dynamic RAM increase” sizes either. Both have to be set in stone during VM creation and before first boot. 

```bash
	❯ cat --plain /etc/fstab

# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/ubuntu-vg/ubuntu-lv during curtin installation
/dev/disk/by-id/dm-uuid-LVM-0Og0oRaUmBHOn3wg2RdS7ykc8rpzhgZUdpzLgldOJV0hg1GlDsIKnHYvw3qDwGF7 / ext4 defaults 0 1
# /boot was on /dev/vda2 during curtin installation
/dev/disk/by-uuid/3ff11bb7-8af8-41ad-8cbe-e269741b9821 /boot ext4 defaults 0 1
# /boot/efi was on /dev/vda1 during curtin installation
/dev/disk/by-uuid/10C3-3E78 /boot/efi vfat defaults 0 1
/swap.img   none    swap    sw  0   0
storage_hdd       /mnt/storage_hdd            9p         trans=virtio,version=9p2000.L,_netdev,rw 0 0
storage_ssd       /mnt/storage_ssd            9p         trans=virtio,version=9p2000.L,_netdev,rw 0 0
```

Ensure the mounts work with these:

```bash
mkdir  /mnt/storage_hdd
mkdir /mnt/storage_ssd

sudo chown USER:USER -R /mnt/storage_hdd
sudo chown USER:USER -R /mnt/storage_ssd
```

# Permissions

## Add user to sudo group (no need to type password) [swer)](https://askubuntu.com/questions/147241/execute-sudo-without-password)

To make the currently logged in user a a sudoer and make `sudo` not prompt them for a password, use

```bash
echo "$USER ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/$USER
```

### Github keys

```bash
# gen keys
ssh-keygen

# upload them
curl \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ⚠️!!PUT YOUR GITHUB TOKEN HERE!!⚠️ " \
   --data "{\"title\":\"DevVm_`date +%Y%m%d%H%M%S`\",\"key\":\"`cat -pp ~/.ssh/id_rsa.pub`\"}"  \
  https://api.github.com/user/keys
```

Todo: better would be to GET the current token, not sure if possible. 

# tmux init plugins

```bash
# start tmux
tmux 
# install plugins
ctrl +a then shift + i         # aka: prefix, then shift I 
```

Tmux ressurect for reboot. 

`<prefix> + ctrl + s` — save your session before reboot, if want to save more recent changes than autosave interval. 

# fastest dir size

```bash
# (if you still need cargo)
curl https://sh.rustup.rs -sSf | sh

# install 
cargo install dirstat-rs

# usage
ds <directory>
# -d {0,1,2,3} - set recurrsive depth
```
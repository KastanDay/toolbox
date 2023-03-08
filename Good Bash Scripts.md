# Good Bash Scripts

Created: July 31, 2022 8:56 PM
Modified: March 8, 2023 12:36 AM

**Table of Contents**

# Setting up a new machine

See [My Server (Home Server & Home Network & Personal Server)](https://www.notion.so/My-Server-Home-Server-Home-Network-Personal-Server-5ae7682b5a9f424b99ad4b6378344c2d) 

See [Setting up an AI machine (setup nvidia box)](https://www.notion.so/Setting-up-an-AI-machine-setup-nvidia-box-95b08b0bf5cb4a489fd7ea469ff57f81) 

# Docker

Using Conda in Docker

<aside>
💡 Key: invoke python using the binary inside your conda env.
command: bash -c "
      **/opt/conda/envs/aida_coreference/bin/python3.6 main.py**

</aside>

Use env variables from the Docker script. Example: **`--tmp_dir ${KAIROS_LIB}/${EXPERIMENT}/${PERFORMER_NAME}/persist/coref --port 20202"`**

[From this github from my NLP classmates. not professional.](https://github.com/RESIN-KAIROS/RESIN-pipeline-public/blob/api/docker-compose.yaml)

```python
  my-service-name:
    image: laituan245/kairos_coref:api
    container_name: coref
    command: bash -c "
      **/opt/conda/envs/aida_coreference/bin/python3.6 main.py --tmp_dir ${KAIROS_LIB}/${EXPERIMENT}/${PERFORMER_NAME}/persist/coref --port 20202"**
    volumes:
      - root:${KAIROS_LIB}
    ports:
      - 20202:20202 # For local docker-compose test
    runtime: nvidia # For local docker-compose test
    environment:
      - NVIDIA_VISIBLE_DEVICES=2 # For local docker-compose test
```

# Monitoring

Great list: [30 Linux System Monitoring Tools Every SysAdmin Should Know - nixCraft - https://www.cyberciti.biz/tips/top-linux-monitoring-tools.html](https://www.cyberciti.biz/tips/top-linux-monitoring-tools.html)

```jsx
13. iptraf – Get real-time network statistics on Linux
sudo iptraf

23. nmon – Linux systems administrator, tuner, benchmark tool
-- great network stats. 

dstat -pcmrt

nice total IO stats. including IOPs io/total should be iops. 

Try fio --  https://fio.readthedocs.io/en/latest/fio_doc.html
That's what Wendell used for IOPs benchmarking
```

# Speed tests

```python
# test ssh speed! super cool. 
yes | pv | ssh remote_host "cat >/dev/null"

# test local disk sequential **write speed**
# 20 GB (change count for more/less)
dd if=/dev/zero of=/tmp/test1.img bs=2G count=10 oflag=dsync

# test local disk sequential **read speed**
# flush cache
****flush
echo 3 | sudo tee /proc/sys/vm/drop_caches
time dd if=/tmp/test1.img of=/dev/null bs=8k  # test1.img needs to exist, or any big file.

# File IO
fio

https://www.iozone.org/
brew install iozone
sudo apt install iozone3
# makes nice plots. Detailed. 

iozone -a -I -b results.xls
# -a automatic
# -I bypass buffer and cache. Direct disk performance. 
# -b write results to excel spreadsheet. 
```

# Directory management

### Move X files from dir to another

head -50000 moves 50k files. 

```bash
ls -Q source_dir | head -50000 | xargs -i mv source_dir/{} dest_dir
# if you want 2 running at once, use head and tail
ls -Q source_dir | tail -50000 | xargs -i mv source_dir/{} dest_dir
```

# Environment variables

### Append to env

```bash
# prepend
PATH=~/opt/bin:$PATH

# post-pend
PATH=$PATH:~/opt/bin
```

# SSH

### generate SSH kes

```python
ssh-keygen -t ed25519
```

### Copy ssh keys to host

```bash
ssh-copy-id username@remote_host
```

### upload ssh keys to github (never tested this)

Documentation here: [Git SSH Keys - GitHub Docs](https://docs.github.com/en/rest/users/keys#create-a-public-ssh-key-for-the-authenticated-user)

For token, go here: [New Personal Access Token (github.com)](https://github.com/settings/tokens/new)

— Kastan: reminder I store this my expansion software.

Upload SSH key to github

```bash
# THIS WORKS amazingly!
# to change ssh key name on github, edit the title field (currently `DevVm`)

# gen keys
ssh-keygen -t ed25519

# EDA key 
curl \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR TOKEN HERE -- YOU GET IT FROM GITHUB SOMEHOW> " \
   --data "{\"title\":\"DevVm_`date +%Y%m%d%H%M%S`\",\"key\":\"`cat ~/.ssh/id_ed25519.pub`\"}"  \
  https://api.github.com/user/keys
```

- [ ]  Better method would be to download my existing ssh keys from github (instead of uploading new one), then add that to my personal server. That way my github isn’t cluttered for each new VM.

## Compress whole folder (tar and zstd)

```bash
⭐️ Best way to compress a folder
tar --zstd -cf dir.tar.zst dir/ 
```

```python
# other methods
# tar (but don't compress) - bundle (zip) files. 
# pv -- monitor progress
# zstd (-2 is less compression, -3 is standard, up to -22 for ultra). 
meh: 
tar cf - output | pv | zstd -3 > output.tar.zstd

# for old versions of tar
tar --use-compress-program zstd -cf directory.tar.zst directory/
```

## Tar unzip/extract any file/compression type:

```python
# DECOMPRESS FOLDER: unzip tar (would work with zstd)
tar -axf archive.tar.anything

# specifically for zstd (but hopefully unnecessary)
# On NCSA Delta (dsitro: RHL 8.4) this was required.
tar -I zstd -xf archive.tar.zst
```

### Recursively count files in `some_dir`:

```python
# pretty printing 
find . -type f | wc -l | xargs numfmt --grouping
```

### Rsync with error logging

> Additionally, rsync exits with a non-zero code when the transfer fails. As a result, we can make use of this feature to write details to log files. This allows combining *stderr* and *stdout* into the stdout stream for further manipulation. Therefore, while executing Rsync commands we append the following on the end of the command
> 

```python
rsync -avP SRC DEST > /var/log/rsync.log 2>&1 
```

For streaming tar, see [Using DELTA for PDG](https://www.notion.so/Using-DELTA-for-PDG-8ddebad6ce6847a1b52171555f29e4d6) 

### File download (wget & curl)

Parallel curl 

```python
# great for model downloads!
curl -Z 'http://httpbin.org/anything/[1-9].{txt,html}' -o '#1.#2'
# -Z == --parallel

curl --parallel http://images.cocodataset.org/zips/train2017.zip -o train2017.zip http://images.cocodataset.org/zips/val2017.zip -o val2017.zip
```

# Example of using bash parameters

- **EXPAND Code here**
    
    ```python
    #!/bin/sh
    # Adaptable tmux resize script by percentage
    ### SOURCE: https://github.com/tony/tmux-config/blob/5b348ee/scripts/resize-adaptable.sh
    ### BLOG:   https://devel.tech/tips/n/tMuXrSz9/resize-tmux-main-panes-by-percentage
    #
    # Layout types supported (-l):
    #
    # main-horizontal: top pane is main pane, panes split left to right on the bottom
    # main-vertical: left pane is maine pane, right panes split top to bottom on the
    #                right side
    #
    # Options:
    # 
    # -l layout-name (required): the name of the layout, "main-horizontal" or "main-vertical"
    # -p percentage (required): an integer of the percentage of the client width/height to set
    # -t target-window (optional): the tmux target for the window, can be an fnmatch(1) of the
    #                              window name, index, or id
    #
    # Example usage:
    #
    # Case 1: Resize to a main-horizontal, main pane 66% of client height
    # $ ./scripts/resize-adaptable.sh -p 66 -l main-horizontal
    #
    # Case 2: Same as Case 1, target "devel" window
    # $ ./scripts/resize-adaptable.sh -p 66 -l main-horizontal -t devel
    #
    # Case 3: Resize to a main-horizontal, main pane half width
    # $ ./scripts/resize-adaptable.sh -p 50 -l main-vertical
    #
    # Case 4: Same as Case 3, target "mywindow"
    # $ ./scripts/resize-adaptable.sh -p 50 -l main-vertical -t mywindow
    #
    # Author: Tony Narlock
    # Website: https://devel.tech
    # License: MIT
    
    lflag=
    pflag=
    tflag=
    while getopts l:p:t: name;
    do
        case $name in
        l)    lflag=1
    	  layout_name=$OPTARG;;
        p)    pflag=1
              percentage="$OPTARG";;
        t)    tflag=1
              target="$OPTARG";;
        ?)   printf "Usage: %s: [-l layout-name] [-p percentage] [-t target-window]\n" $0
              exit 2;;
        esac
    done
    
    if [ ! -z "$pflag" ]; then
        if ! [ "$percentage" -eq "$percentage" ] 2> /dev/null; then
            printf "Percentage (-p) must be an integer" >&2
            exit 1
        fi
    fi
    if [ ! -z "$lflag" ]; then
        if [ $layout_name != 'main-horizontal' ] && [ $layout_name != 'main-vertical' ] ; then
            printf "layout name must be main-horizontal or main-vertical" >&2
            exit 1
        fi
    fi
    
    if [ "$layout_name" = "main-vertical" ]; then
        MAIN_PANE_SIZE=$(expr $(tmux display -p '#{window_width}') \* $percentage \/ 100)
        MAIN_SIZE_OPTION='main-pane-width'
    
    fi
    
    if [ "$layout_name" = "main-horizontal" ]; then
        MAIN_PANE_SIZE=$(expr $(tmux display -p '#{window_height}') \* $percentage \/ 100)
        MAIN_SIZE_OPTION='main-pane-height'
    fi
    
    if [ ! -z "$target" ]; then
        tmux setw -t $target $MAIN_SIZE_OPTION $MAIN_PANE_SIZE; tmux select-layout -t $target $layout_name
    else
        tmux setw $MAIN_SIZE_OPTION $MAIN_PANE_SIZE; tmux select-layout $layout_name
    fi
    
    exit 0
    ```
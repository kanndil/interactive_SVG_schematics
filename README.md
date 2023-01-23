# interactive_SVG_schematics


## Table of contents

* [Overview](#-overview)
* [File structure](#file-structure)
* [Dependencies](#-dependencies)
* [How to use](#-how-to-use)
* [Support new library]()
* [Authors](#authors)
* [Copyright and Licensing](#%EF%B8%8F-copyright-and-licensing)
<br/><br/>

# 📖 Overview

Extracts the paths generated by [OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA) reports and uses [netlistsvg](https://github.com/nturley/netlistsvg) to produce interactive SVG schematics for the extracted paths. The produced schematics interactively show the timing details of each cell for any standard cell library. Sky130_fd_sc_hd is supported as the default standard cell library, howeve, to add other libraries check [Support new library]().
<br/><br/>

# File structure

<br/><br/>

# 🧱 Dependencies


<details>
  <summary>For macos</summary>


## Install python3.6+
- get homebrew

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

- install python using homebrew

        export PATH="/usr/local/opt/python/libexec/bin:$PATH"
        brew install python3

## Install Yosys 

You can find the installation steps in [Yosys installation](https://github.com/YosysHQ/yosys).

## Install OpenSTA

- Install OpenSTA  

You can find the installation steps in [OpenSTA installation](https://github.com/The-OpenROAD-Project/OpenSTA).


## Install netlistsvg

To install the latest version from source:
```sh
git clone https://github.com/nturley/netlistsvg
cd netlistsvg
npm install # install dependencies
sudo npm install -g . # install netlistsvg to system

sudo npm uninstall -g netlistsvg # uninstall from system
```
</details>

<details>
  <summary>For Linux</summary>

## Install Conda for package installation

    bash Miniconda3-latest-Linux-x86_64.sh

## Use  Conda to install all dependencies

    conda install -y -c litex-hub -c conda-forge python yosys 

## Install OpenSTA

- Install OpenSTA  

        conda install -y -c litex-hub -c conda-forge openroad

    or

    You can find the installation steps in [OpenSTA installation](https://github.com/The-OpenROAD-Project/OpenSTA).


## Install netlistsvg

To install the latest version from source:
```sh
git clone https://github.com/nturley/netlistsvg
cd netlistsvg
npm install # install dependencies
sudo npm install -g . # install netlistsvg to system

sudo npm uninstall -g netlistsvg # uninstall from system
```
</details>

<details>
  <summary>For Windows-10</summary>

## Install python3.6+
Install using the executable installer [here](https://www.python.org/downloads/windows/)

## Install Yosys 

You can find the installation steps in [Yosys installation](https://github.com/YosysHQ/yosys).


## Install OpenSTA

- Install OpenSTA  

You can find the installation steps in [OpenSTA installation](https://github.com/The-OpenROAD-Project/OpenSTA).


## Install netlistsvg

To install the latest version from source:
```sh
git clone https://github.com/nturley/netlistsvg
cd netlistsvg
npm install # install dependencies
sudo npm install -g . # install netlistsvg to system

sudo npm uninstall -g netlistsvg # uninstall from system
```
</details>
<br/><br/>

# 🔍 How to use

<br/><br/>

# Authors

* [Mohamed Shalan](https://github.com/shalan)
* [Youssef Kandil](https://github.com/kanndil)
<br/><br/>

# ⚖️ Copyright and Licensing

Copyright 2023 AUC Open Source Hardware Lab

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License.
<br/><br/>
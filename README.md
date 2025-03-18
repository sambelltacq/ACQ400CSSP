
# ACQ400CSSP

Set of phoebus OPIs based on [ACQ400CSS](https://github.com/D-TACQ/ACQ400CSS) for [D-Tacq](https://d-tacq.co.uk/) Digitizers.


## Installation

- Clone repo
    ```bash
    git clone https://github.com/D-TACQ/ACQ400CSSP
    cd ACQ400CSSP
    ```

- Install [JDK17](https://adoptium.net/en-GB/temurin/archive/?version=17)
- Download and extract phoebus https://www.controlsystemstudio.org/download/

- For ease of installation extract the phoebus jar directory to the repo directory ie.

    ```bash
    │── ACQ400CSSP
    │   │── run_phoebus
    │   │── workspaces
    │   │── src
    │   │── product-1.2.3
    │   │   │── phoebus-1.2.3.jar
    ```

- The run script will try to find the phoebus jar within the directory
- You can also hardcode the path by editing the PHOEBUS_JAR var within the script

## Usage


#### Linux

```bash
./run_phoebus acq2106_999
```

#### Windows

```bash
run_phoebus acq2106_999
```

We recommend creating a shotcut to the run script


## Updating

- Update the repo

```bash
git pull
```

- Erase outdated workspaces

```bash
rm -rf workspaces
```

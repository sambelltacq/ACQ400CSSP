
# ACQ400CSSP

Set of phoebus OPIs based on [ACQ400CSS](https://github.com/D-TACQ/ACQ400CSS) for [D-Tacq](https://d-tacq.co.uk/) Digitizers.

![multi_1_opi](https://github.com/sambelltacq/ACQ400CSSP/releases/download/v1.0.0/multi_1_opi.png)

## Installation

- Clone repo
    ```bash
    git clone https://github.com/D-TACQ/ACQ400CSSP
    cd ACQ400CSSP
    ```

- Install [Java17](https://adoptium.net/en-GB/temurin/archive/?version=17)
- Download and extract [Phoebus](https://www.controlsystemstudio.org/download/)

- For ease of installation extract or link the phoebus jar directory to the repo e.g.

    ```bash
    │── ACQ400CSSP
    │   │── ACQ400CSSP_launcher
    │   │── workspaces
    │   │── CSSP.conf
    │   │── product-0.0.0
    │   │   │── phoebus-0.0.0.jar
    ```

- You can create a CSSP.conf file to hardcode paths if needed:

    ```bash
    JAVA_BIN=C:\Program Files\Eclipse Adoptium\jre-17.0.12.7-hotspot\bin\java.exe
    PHOEBUS_JAR=C:\Users\USER\PROJECTS\ACQ400CSSP\phoebus-4.7.4-SNAPSHOT\product-4.7.4-SNAPSHOT.jar
    ```

## Usage

#### Python (recommended)
```bash
./ACQ400CSSP_launcher.py acq2106_999
```

##### Linux

```bash
./run_phoebus acq2106_999
```

##### Windows

```bash
run_phoebus acq2106_999
```

## Updating

- Update the repo

```bash
git pull
```

- Erase outdated workspaces

```bash
rm -rf workspaces
```


# ACQ400CSSP

Set of phoebus OPIs based on [ACQ400CSS](https://github.com/D-TACQ/ACQ400CSS) for [D-Tacq](https://d-tacq.co.uk/) Digitizers.


## Installation

- Clone repo
    ```bash
    git clone https://github.com/sambelltacq/ACQ400CSSP
    cd ACQ400CSSP
    ```

- Install [JDK17](https://adoptium.net/en-GB/temurin/archive/?version=17)
- Download and extract phoebus https://www.controlsystemstudio.org/download/

- For ease of installation extract the phoebus jar directory to the repo directory ie.

    ```bash
    │── ACQ400CSSP
    │   │── run_phoebus 
    │   │── phoebus
    │   │   │── phoebus-4.7.3.jar
    ```

- Edit the run_phoebus script and set the PHOEBUS_JAR var to the correct path
## Usage


#### Linux

```bash
./run_phoebus acq2106_999
```

#### Windows

```bash
run_phoebus acq2106_999
```

Can also click on the script in windows explorer 




# AL Speech Stream Generator 
## 1. Installation
Download the source code and unzip it to a directory of your choice. Install Anaconda - Download and install [Anaconda](https://www.anaconda.com/products/individual) (if not already installed). Open your terminal and run the following commands to create and activate a new Anaconda environment: 
```bash
conda create -n al_maker
conda activate al_maker
```
Then install `pip` and the necessary Python packages:
```bash
conda install pip 
pip install praat-parselmouth
```
Navigate to the directory containing the unzipped code and install the remaining packages:
```bash
cd /path/to/the/code
pip install -r requirements.txt
```
## 2. Generate speech streams
After setting up the environment, you can generate the speech streams. First, review and modify the configuration file `conf.py` as needed (see explanations inside the file). Run the main script to generate the speech streams:
```bash
./run.sh
```
By default, this will create a new folder called `output`. The speech streams, along with other information such as transitional probability statistics, will be saved to the `speech_streams` directory inside this folder.

(Optional) To change the name of the output folder, use the `-o` option:
```bash
./run.sh -o output_folder_name_of_your_choice
```
If you encounter permission issues, ensure the script has executable permissions:
```bash
chmod +x run.sh
```
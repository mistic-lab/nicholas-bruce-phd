#! /bin/bash
#SBATCH --account=def-peterdri
#SBATCH --time=01:00:00
#SBATCH --job-name=pull-LWA-ant
#SBATCH --mem=50G
#SBATCH --cpus-per-task=8

module load gcc/5.4.0
module load fftw/3.3.6
module load scipy-stack/2019a

export ATLAS=/project/def-peterdri/software/atlas-3.10.2
export ATLAS_HOME=/project/def-peterdri/software/atlas-3.10.2

source /home/nsbruce/projects/def-peterdri/nsbruce/software/lwa-1.2.4/bin/activate
python ./extract_LWA_ant.py --input=/home/nsbruce/projects/def-peterdri/LWA_Data/2019-05-25/RAW_TBN/058628_001748284 --output=058628_001748284_s5p0.dat
deactivate


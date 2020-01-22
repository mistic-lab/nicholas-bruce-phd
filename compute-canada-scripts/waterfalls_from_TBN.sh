#! /bin/bash
#SBATCH --account=def-peterdri
#SBATCH --time=01:00:00
#SBATCH --job-name=waterfall-builder
#SBATCH --mem=20G
#SBATCH --cpus-per-task=8

module load gcc/5.4.0

module load fftw/3.3.6

module load scipy-stack/2019a

module load python/2.7

export ATLAS=/project/def-peterdri/software/atlas-3.10.2

export ATLAS_HOME=/project/def-peterdri/software/atlas-3.10.2

source /home/nsbruce/projects/def-peterdri/nsbruce/virtual-environments/lwa-1.2.4/bin/activate

TBN_DIR=/home/nsbruce/projects/def-peterdri/LWA_Data/2019-12-29/RAW_TBN/
NUM_SEC=240

python2 /home/nsbruce/UViip/lwa-tools/code/plot_waterfallsTBN.py $TBN_DIR -s $NUM_SEC

deactivate


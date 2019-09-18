#! /bin/bash
#SBATCH --account=def-peterdri
#SBATCH --time=05:00:00
#SBATCH --job-name=AE-dataset-builder
#SBATCH --mem=150G
#SBATCH --cpus-per-task=15

module load python/3.7.4
module load scipy-stack/2019a

source /home/nsbruce/projects/def-peterdri/nsbruce/RFI/venv/bin/activate
python /home/nsbruce/projects/def-peterdri/nsbruce/RFI/autoencoder-anomaly-detector/code/build_datasets.py
deactivate


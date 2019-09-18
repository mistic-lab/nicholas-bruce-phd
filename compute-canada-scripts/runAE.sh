#! /bin/bash
#SBATCH --account=def-peterdri
#SBATCH --time=10:00:00
#SBATCH --job-name=run-anomaly-autoencoder
#SBATCH --mem=240G
#SBATCH --cpus-per-task=24

module load python/3.7.4
module load scipy-stack/2019a

source /home/nsbruce/projects/def-peterdri/nsbruce/RFI/venv/bin/activate
python /home/nsbruce/projects/def-peterdri/nsbruce/RFI/autoencoder-anomaly-detector/main.py
deactivate


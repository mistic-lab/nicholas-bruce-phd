#! /bin/bash
#SBATCH --account=def-peterdri
#SBATCH --time=10:00:00
#SBATCH --job-name=BBExtraction
#SBATCH --mem=240G
#SBATCH --cpus-per-task=10

module load python/3.7.4
module load scipy-stack/2019a

source /home/nsbruce/projects/def-peterdri/nsbruce/RFI/venv/bin/activate
python /home/nsbruce/projects/def-peterdri/nsbruce/nicholas-bruce-phd/specutils/Extract_C64_to_BB_files.py
deactivate

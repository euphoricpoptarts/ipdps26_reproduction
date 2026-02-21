snap install cmake --classic
apt-get install -y openmpi-bin libopenmpi-dev
x=${PWD}
mkdir comp
git clone https://github.com/VieClus/VieClus.git
cd ${x}/comp/VieClus
git checkout 5caa08291b67a9e134ac7b41bc1aacd6605020cd
bash compile_withcmake.sh
cp build/evolutionary_clustering ${x}/comp_exe/vieclus
cd ${x}
python3 python_scripts/run_vieclus.py graphs/ comp_data/vieclus_results.txt
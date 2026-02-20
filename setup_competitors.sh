x=${PWD}
mkdir comp_exe
mkdir comp
cd comp
git clone https://github.com/euphoricpoptarts/leiden-communities-openmp.git
git clone https://github.com/euphoricpoptarts/louvain-communities-cuda.git
git clone https://github.com/euphoricpoptarts/louvain-communities-openmp.git
git clone https://github.com/euphoricpoptarts/GALA.git
git clone https://github.com/VieClus/VieClus.git
cd ${x}/comp/leiden-communities-openmp
git checkout experiment
g++ -DMAX_THREADS=32 -std=c++17 -O3 -fopenmp main.cxx -o ${x}/comp_exe/gve-leiden
cd ${x}/comp/louvain-communities-openmp
git checkout experiment
g++ -DMAX_THREADS=32 -std=c++17 -O3 -fopenmp main.cxx -o ${x}/comp_exe/gve-louvain
cd ${x}/comp/louvain-communities-cuda
git checkout experiment
nvcc -std=c++17 -arch=sm_100 -O3 -Xcompiler -fopenmp -x cu main.cxx -o ${x}/comp_exe/v-louvain
cd ${x}/comp/GALA
git checkout experiment
cd src
make -j
cp gala_main ${x}/comp_exe/gala
cd ${x}/comp/VieClus
bash compile_withcmake.sh
cp build/evolutionary_clustering ${x}/comp_exe/vieclus
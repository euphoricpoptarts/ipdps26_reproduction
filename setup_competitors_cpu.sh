x=${PWD}
mkdir comp_exe
mkdir comp
cd comp
git clone https://github.com/euphoricpoptarts/leiden-communities-openmp.git
git clone https://github.com/euphoricpoptarts/louvain-communities-openmp.git
cd ${x}/comp/leiden-communities-openmp
git checkout experiment
g++ -DMAX_THREADS=32 -std=c++17 -O3 -fopenmp main.cxx -o ${x}/comp_exe/gve-leiden
cd ${x}/comp/louvain-communities-openmp
git checkout experiment
g++ -DMAX_THREADS=32 -std=c++17 -O3 -fopenmp main.cxx -o ${x}/comp_exe/gve-louvain
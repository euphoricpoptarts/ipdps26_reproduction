x=${PWD}
mkdir exe
e=${PWD}/exe
git clone https://github.com/euphoricpoptarts/PennsylvaniaGPUGraphClustering.git
cd PennsylvaniaGPUGraphClustering
mkdir build
cd build
cmake ..
make -j
cp app/plouvain ${e}/plouvain_base
cp app/pleiden ${e}/pleiden_base
cp app/pleiden+ ${e}/pleiden+_base
git checkout ablation_contract_bad
make -j
cp app/plouvain ${e}/ablation_contract_bad
git checkout ablation_fused_all
make -j
cp app/plouvain ${e}/ablation_fused_all
git checkout ablation_fused_large_only
make -j
cp app/plouvain ${e}/ablation_fused_large_only
git checkout ablation_mlh
make -j
cp app/plouvain ${e}/ablation_mlh
git checkout ablation_no_afterburner
make -j
cp app/plouvain ${e}/ablation_no_afterburner
git checkout ablation_no_uncoarsen
make -j
cp app/plouvain ${e}/ablation_no_uncoarsen
git checkout ablation_no_uncoarsen_2xlm
make -j
cp app/plouvain ${e}/ablation_no_uncoarsen_2xlm
git checkout master
git apply ${x}/enable_extra_timing.patch
make -j
cp app/plouvain ${e}/plouvain_extra_timing
cp app/pleiden ${e}/pleiden_extra_timing
cp app/pleiden+ ${e}/pleiden+_extra_timing

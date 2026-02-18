# This is an example script to build and install kokkos for an ubuntu system with B200 GPU
loc=$PWD/container
ipwd=$PWD
# need to use nvcc_wrapper to compile kokkos + kokkos-kernels
compiler=$loc/kokkos/bin/nvcc_wrapper
arch=Blackwell100
mkdir container
cd $loc
git clone https://github.com/kokkos/kokkos.git
git clone https://github.com/kokkos/kokkos-kernels.git
mkdir install
cd kokkos
git checkout master
git apply $ipwd/kokkos.patch
cd $loc/kokkos-kernels
git checkout master
mkdir build
cd build
kk_prefix=$loc/install/kokkos-kernels
# kokkos + kokkos-kernels build
./../cm_generate_makefile.bash \
--kokkos-path=$loc/kokkos --kokkoskernels-path=$loc/kokkos-kernels \
--release --kokkos-release \
--kokkos-prefix=$loc/install/kokkos \
--prefix=$kk_prefix --disable-tests --disable-perftests --disable-examples --no-default-eti \
--with-cuda --arch=$arch --compiler=$compiler \
--with-openmp --with-serial --enable-cuda-lambda
#if your kokkos-kernel build fails, it is probably due to running out of memory
#in this case you will need to change the -j to -j16 or something small
make install -j
mkdir -p ~/.cmake/packages/KokkosKernels
echo $kk_prefix > ~/.cmake/packages/KokkosKernels/find.txt

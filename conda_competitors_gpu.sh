conda install rapidsai::cugraph
python3 python_scripts/run_cugraph_louvain.py graphs/ comp_data/cugraph_louvain_results.txt
python3 python_scripts/run_cugraph_leiden.py graphs/ comp_data/cugraph_leiden_results.txt
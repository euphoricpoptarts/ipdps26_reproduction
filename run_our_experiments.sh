mkdir metrics
mkdir -p experiments/plouvain_base
mkdir -p experiments/pleiden_base
mkdir -p experiments/pleiden+_base
mkdir -p experiments/plouvain_11
mkdir -p experiments/pleiden_11
mkdir -p experiments/pleiden+_11
mkdir -p experiments/ablation/contract_bad
mkdir -p experiments/ablation/fused_all
mkdir -p experiments/ablation/fused_large_only
mkdir -p experiments/ablation/mlh
mkdir -p experiments/ablation/no_afterburner
mkdir -p experiments/ablation/no_uncoarsen
mkdir -p experiments/ablation/no_uncoarsen_2xlm
mkdir -p experiments/ablation/no_simulated_annealing
mkdir -p experiments/extra_timing/plouvain
mkdir -p experiments/extra_timing/pleiden
mkdir -p experiments/extra_timing/pleiden+
python3 python_scripts/run_cluster_experiment.py ./exe/plouvain_base 0 graphs metrics experiments/plouvain_base
python3 python_scripts/run_cluster_experiment.py ./exe/pleiden_base 0 graphs metrics experiments/pleiden_base
python3 python_scripts/run_cluster_experiment.py ./exe/pleiden+_base 0 graphs metrics experiments/pleiden+_base
python3 python_scripts/run_cluster_experiment.py ./exe/plouvain_base 10 graphs metrics experiments/plouvain_11
python3 python_scripts/run_cluster_experiment.py ./exe/pleiden_base 10 graphs metrics experiments/pleiden_11
python3 python_scripts/run_cluster_experiment.py ./exe/pleiden+_base 10 graphs metrics experiments/pleiden+_11
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_contract_bad 0 graphs metrics experiments/ablation/contract_bad
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_fused_all 0 graphs metrics experiments/ablation/fused_all
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_fused_large_only 0 graphs metrics experiments/ablation/fused_large_only
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_mlh 0 graphs metrics experiments/ablation/mlh
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_no_afterburner 0 graphs metrics experiments/ablation/no_afterburner
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_no_uncoarsen 0 graphs metrics experiments/ablation/no_uncoarsen
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_no_uncoarsen_2xlm 0 graphs metrics experiments/ablation/no_uncoarsen_2xlm
python3 python_scripts/run_cluster_experiment.py ./exe/ablation_no_simulated_annealing 0 graphs metrics experiments/ablation/no_simulated_annealing
python3 python_scripts/run_cluster_experiment.py ./exe/plouvain_extra_timing 0 graphs metrics experiments/extra_timing/plouvain
python3 python_scripts/run_cluster_experiment.py ./exe/pleiden_extra_timing 0 graphs metrics experiments/extra_timing/pleiden
python3 python_scripts/run_cluster_experiment.py ./exe/pleiden+_extra_timing 0 graphs metrics experiments/extra_timing/pleiden+
mkdir -p results/plouvain_base
mkdir -p results/pleiden_base
mkdir -p results/pleiden+_base
mkdir -p results/plouvain_11
mkdir -p results/pleiden_11
mkdir -p results/pleiden+_11
mkdir -p results/ablation/contract_bad
mkdir -p results/ablation/fused_all
mkdir -p results/ablation/fused_large_only
mkdir -p results/ablation/mlh
mkdir -p results/ablation/no_afterburner
mkdir -p results/ablation/no_uncoarsen
mkdir -p results/ablation/no_uncoarsen_2xlm
mkdir -p results/ablation/no_simulated_annealing
mkdir -p results/extra_timing/plouvain
mkdir -p results/extra_timing/pleiden
mkdir -p results/extra_timing/pleiden+
python3 python_scripts/parse_cluster_experiment.py experiments/plouvain_base results/plouvain_base
python3 python_scripts/parse_cluster_experiment.py experiments/pleiden_base results/pleiden_base
python3 python_scripts/parse_cluster_experiment.py experiments/pleiden+_base results/pleiden+_base
python3 python_scripts/parse_cluster_experiment.py experiments/plouvain_11 results/plouvain_11
python3 python_scripts/parse_cluster_experiment.py experiments/pleiden_11 results/pleiden_11
python3 python_scripts/parse_cluster_experiment.py experiments/pleiden+_11 results/pleiden+_11
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/contract_bad results/ablation/contract_bad
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/fused_all results/ablation/fused_all
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/fused_large_only results/ablation/fused_large_only
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/mlh results/ablation/mlh
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/no_afterburner results/ablation/no_afterburner
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/no_uncoarsen results/ablation/no_uncoarsen
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/no_uncoarsen_2xlm results/ablation/no_uncoarsen_2xlm
python3 python_scripts/parse_cluster_experiment.py experiments/ablation/no_simulated_annealing results/ablation/no_simulated_annealing
python3 python_scripts/parse_cluster_experiment.py experiments/extra_timing/plouvain results/extra_timing/plouvain
python3 python_scripts/parse_cluster_experiment.py experiments/extra_timing/pleiden results/extra_timing/pleiden
python3 python_scripts/parse_cluster_experiment.py experiments/extra_timing/pleiden+ results/extra_timing/pleiden+
python3 python_scripts/run_memeclusters.py graphs results/meme/results.txt

# run with 'snakemake -j 1'

GENE_THRESHOLDS=['10_90']

rule all:
    input:
        expand('stm_model_{thresh}.json', thresh=GENE_THRESHOLDS)

rule run_imat:
    input:
        csv='stm_threshold_{thresh}.csv',
    output:
        model='stm_model_{thresh}.json'
    shell: """
        python run-imat.py {input.csv} -o {output.model}
    """

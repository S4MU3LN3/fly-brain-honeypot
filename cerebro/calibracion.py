from model import run_exp
from model import default_params as params
import utils as utl
from brian2 import ms

config = {
    'path_res'  : './results/calibracion',
    'path_comp' : './Completeness_783.csv',
    'path_con'  : './Connectivity_783.parquet',
    'n_proc'    : -1,
}

params['n_run'] = 5
params['t_run'] = 500 * ms

def cargar_ids(path):
    with open(path, encoding='utf-8') as f:
        return [int(x) for x in f.read().strip().split(',') if x.strip()]

neu_lc4 = cargar_ids('root_ids_cell_type_LC4.txt')
neu_lplc2 = cargar_ids('root_ids_cell_type_LPLC2.txt')

id_gf_derecha = 720575940632499757
id_gf_izquierda = 720575940622838154

niveles = {
    'nulo':   [],
    'debil':  (neu_lc4[:5] + neu_lplc2[:5]),
    'fuerte': (neu_lc4 + neu_lplc2),
}

for nombre, neuronas in niveles.items():
    print(f">>> Nivel '{nombre}': {len(neuronas)} neuronas excitadas")
    run_exp(exp_name=f'nivel_{nombre}', neu_exc=neuronas, params=params, **config)

print("\n>>> Resultados:")
for nombre in niveles:
    df_spike = utl.load_exps([f'./results/calibracion/nivel_{nombre}.parquet'])
    df_rate, _ = utl.get_rate(df_spike, t_run=params['t_run'], n_run=params['n_run'])
    col = f'nivel_{nombre}'
    gf_d = df_rate.loc[id_gf_derecha, col] if id_gf_derecha in df_rate.index else 0.0
    gf_i = df_rate.loc[id_gf_izquierda, col] if id_gf_izquierda in df_rate.index else 0.0
    print(f"  {nombre:8s} -> GF derecha: {gf_d:6.1f} Hz | GF izquierda: {gf_i:6.1f} Hz")

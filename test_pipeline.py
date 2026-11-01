import os
import pandas as pd
import yaml
import pipeline

cfg = yaml.safe_load(open('config.yaml'))
cfg['output_dir'] = 'test_results'

df = pd.read_csv('bank.csv', sep=None, engine='python')
n_raw = len(df)

def test_load():
    assert df.shape[1] == 17

def test_profile_outputs():
    pipeline.profile(df, 'test_results', 5.0)
    assert os.path.exists('test_results/profiling_report.json')

def test_clean_sentinel_fixed():
    df_clean = pipeline.clean(df, cfg)
    assert (df_clean['pdays'] == -1).sum() == 0

def test_clean_no_negative_balance():
    df_clean = pipeline.clean(df, cfg)
    assert (df_clean['balance'] < 0).sum() == 0

def test_rows_preserved():
    df_clean = pipeline.clean(df, cfg)
    assert len(df_clean) == n_raw

def test_health_above_90():
    df_clean = pipeline.clean(df, cfg)
    health = pipeline.validate(df_clean, cfg, 'test_results')
    assert health > 90

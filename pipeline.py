"""
Automated Data Quality & Validation Pipeline (Module 4)
CadetX Virtual Work Experience

Usage: python pipeline.py --input bank.csv --config config.yaml
Stages: Profile -> Clean -> Validate
"""
import argparse
import json
import logging
import os
from datetime import datetime

import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import IsolationForest

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.FileHandler('pipeline.log'),
                              logging.StreamHandler()])
log = logging.getLogger('dq-pipeline')


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def profile(df, out_dir, threshold_pct):
    os.makedirs(out_dir, exist_ok=True)
    log.info('MODULE 1: Profiling started')
    suspicious = []
    for col in df.columns:
        issues = []
        s = df[col]
        if float(s.isna().mean() * 100) > 50:
            issues.append('very high missingness')
        if pd.api.types.is_numeric_dtype(s):
            vals = s.dropna()
            q1, q3 = vals.quantile(0.25), vals.quantile(0.75)
            iqr = q3 - q1
            n_out = int(((vals < q1 - 1.5 * iqr) | (vals > q3 + 1.5 * iqr)).sum())
            if n_out > len(df) * threshold_pct / 100:
                issues.append(f'heavy outliers ({n_out} rows)')
        if issues:
            suspicious.append({'column': col, 'issues': issues})
    report = {'dataset': {'rows': int(len(df)), 'columns': int(df.shape[1])},
              'generated_at': datetime.now().isoformat(timespec='seconds'),
              'suspicious_columns': suspicious}
    with open(os.path.join(out_dir, 'profiling_report.json'), 'w') as f:
        json.dump(report, f, indent=2)
    log.info('MODULE 1: done — %d suspicious columns', len(suspicious))


def clean(df, cfg):
    os.makedirs(cfg['output_dir'], exist_ok=True)
    log.info('MODULE 2: Cleaning started')
    cleaning_log = []
    df_clean = df.copy()

    for col, sentinel in cfg['cleaning']['sentinel_columns'].items():
        if col in df_clean.columns:
            mask = df_clean[col] == sentinel
            n = int(mask.sum())
            df_clean.loc[mask, col] = np.nan
            cleaning_log.append({'action': 'sentinel_to_nan', 'column': col, 'rows_affected': n})
            log.info('  sentinel fix: %s (%d rows)', col, n)

    if 'balance' in df_clean.columns:
        mask = df_clean['balance'] < 0
        n = int(mask.sum())
        df_clean.loc[mask, 'balance'] = np.nan
        cleaning_log.append({'action': 'invalid_to_nan', 'column': 'balance', 'rows_affected': n})

    n_cap = 0
    for col in cfg['cleaning']['cap_columns']:
        if col not in df_clean.columns:
            continue
        s = df_clean[col]
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask = (s < lo) | (s > hi)
        n_cap += int(mask.sum())
        df_clean[col] = s.clip(lo, hi)
    cleaning_log.append({'action': 'outlier_capping', 'rows_affected': n_cap})

    df_clean.to_csv(os.path.join(cfg['output_dir'], 'cleaned_data.csv'), index=False)
    with open(os.path.join(cfg['output_dir'], 'cleaning_log.json'), 'w') as f:
        json.dump({'actions': cleaning_log}, f, indent=2)
    log.info('MODULE 2: done — %d outlier cells capped', n_cap)
    return df_clean


def validate(df_clean, cfg, out_dir):
    log.info('MODULE 3: Validation started')
    violations = 0
    for col, (lo, hi) in cfg['validation']['rules'].items():
        if col in df_clean.columns:
            n = int(((df_clean[col] < lo) | (df_clean[col] > hi)).sum())
            violations += n
            log.info('  rule %s in [%s,%s]: %d violations', col, lo, hi, n)

    feats = [c for c in ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
             if c in df_clean.columns]
    X = df_clean[feats].fillna(df_clean[feats].median())
    iso = IsolationForest(contamination=cfg['validation']['isolation_forest_contamination'],
                          random_state=42)
    anomalies = int((iso.fit_predict(X) == -1).sum())

    health = round(100 - (violations / len(df_clean) * 100) - (anomalies / len(df_clean) * 100), 2)
    with open(os.path.join(out_dir, 'validation_report.json'), 'w') as f:
        json.dump({'rule_violations': violations, 'anomalies': anomalies,
                   'dataset_health_score': health}, f, indent=2)
    log.info('MODULE 3: done — health %.2f/100', health)
    return health


def main():
    ap = argparse.ArgumentParser(description='Data Quality Pipeline')
    ap.add_argument('--input', required=True)
    ap.add_argument('--config', default='config.yaml')
    args = ap.parse_args()

    cfg = load_config(args.config)
    os.makedirs(cfg['output_dir'], exist_ok=True)

    log.info('PIPELINE START: %s', args.input)
    df = pd.read_csv(args.input, sep=None, engine='python')
    log.info('Loaded %d rows x %d columns', len(df), df.shape[1])

    profile(df, cfg['output_dir'], cfg['profiling']['outlier_threshold_pct'])
    df_clean = clean(df, cfg)
    health = validate(df_clean, cfg, cfg['output_dir'])

    log.info('PIPELINE COMPLETE — Health Score: %.2f/100', health)
    print(f'Pipeline complete! Health Score: {health}/100 -> outputs in results/')


if __name__ == '__main__':
    main()

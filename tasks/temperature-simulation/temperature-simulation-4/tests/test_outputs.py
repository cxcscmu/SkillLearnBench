import json
import os
import re
import subprocess
from datetime import datetime

import numpy as np
import pandas as pd
from netCDF4 import Dataset

LAKE_DEPTH = 25
SIM_FOLDER = "/root"
METRICS_PATH = os.path.join(SIM_FOLDER, "metrics.json")
BASELINE_NML_PATH = os.path.join("/tests", "baseline_glm3.nml")
ALLOWED_CHANGED_PARAMS = {"Kw", "coef_mix_hyp", "wind_factor", "lw_factor", "ch"}
REPORT_TOLERANCE = 0.03
OVERALL_RMSE_THRESHOLD = 1.60
ANNUAL_DEEP_RMSE_THRESHOLD = 1.55
SUMMER_DEEP_RMSE_THRESHOLD = 1.70
PARAM_BOUNDS = {
    "Kw": (0.1, 0.5),
    "coef_mix_hyp": (0.3, 0.7),
    "wind_factor": (0.7, 1.3),
    "lw_factor": (0.7, 1.3),
    "ch": (0.0005, 0.002),
}


def read_glm_output(nc_path):
    nc = Dataset(nc_path, "r")
    time = nc.variables["time"][:]
    z = nc.variables["z"][:]
    temp = nc.variables["temp"][:]
    start_date = datetime(2009, 1, 1, 12, 0, 0)
    records = []
    for t_idx in range(len(time)):
        hours = float(time[t_idx])
        date = pd.Timestamp(start_date) + pd.Timedelta(hours=hours)
        heights = z[t_idx, :, 0, 0]
        temps = temp[t_idx, :, 0, 0]
        for d_idx in range(len(heights)):
            h_val = heights[d_idx]
            t_val = temps[d_idx]
            if not np.ma.is_masked(h_val) and not np.ma.is_masked(t_val):
                depth = LAKE_DEPTH - float(h_val)
                if 0 <= depth <= LAKE_DEPTH:
                    records.append(
                        {
                            "datetime": date,
                            "depth": round(depth),
                            "temp_sim": float(t_val),
                        }
                    )
    nc.close()
    df = pd.DataFrame(records)
    return df.groupby(["datetime", "depth"]).agg({"temp_sim": "mean"}).reset_index()


def read_observations(obs_path):
    df = pd.read_csv(obs_path)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["depth"] = df["depth"].round().astype(int)
    df = df.rename(columns={"temp": "temp_obs"})
    return df[["datetime", "depth", "temp_obs"]]


def rmse_from_merged(merged):
    if len(merged) == 0:
        return 999.0
    errors = merged["temp_sim"] - merged["temp_obs"]
    return float(np.sqrt(np.mean(errors**2)))


def calculate_task_metrics(sim_df, obs_df):
    merged = pd.merge(obs_df, sim_df, on=["datetime", "depth"], how="inner")
    summer_mask = merged["datetime"].dt.month.isin([6, 7, 8, 9])
    annual_deep = merged[merged["depth"] >= 13]
    summer_deep = merged[summer_mask & (merged["depth"] >= 13)]

    return {
        "overall_rmse": rmse_from_merged(merged),
        "annual_deep_rmse": rmse_from_merged(annual_deep),
        "summer_deep_rmse": rmse_from_merged(summer_deep),
        "overall_n_pairs": int(len(merged)),
        "annual_deep_n_pairs": int(len(annual_deep)),
        "summer_deep_n_pairs": int(len(summer_deep)),
    }


def normalize_token(token):
    token = token.strip()
    if token.lower() in {".true.", ".false."}:
        return token.lower()
    if token.startswith("'") and token.endswith("'"):
        return token
    try:
        return f"{float(token):.10g}"
    except ValueError:
        return re.sub(r"\s+", " ", token)


def normalize_value(value):
    return ",".join(normalize_token(part) for part in value.split(","))


def load_nml_assignments(path):
    assignments = {}
    with open(path, "r") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("&") or stripped == "/" or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            assignments[key.strip()] = normalize_value(value.strip())
    return assignments


def changed_nml_params(candidate_path):
    baseline = load_nml_assignments(BASELINE_NML_PATH)
    candidate = load_nml_assignments(candidate_path)
    changed = []
    for key in sorted(set(baseline) | set(candidate)):
        if baseline.get(key) != candidate.get(key):
            changed.append(key)
    return changed


def load_numeric_params(path, names):
    assignments = load_nml_assignments(path)
    values = {}
    for name in names:
        raw = assignments.get(name)
        assert raw is not None, f"Missing parameter in glm3.nml: {name}"
        values[name] = float(raw)
    return values


class TestGLMCalibrationTrap:
    def test_glm_runs(self):
        result = subprocess.run(["glm"], cwd=SIM_FOLDER, capture_output=True, text=True)
        assert result.returncode == 0, f"GLM failed: {result.stderr}"

    def test_output_exists(self):
        nc_path = os.path.join(SIM_FOLDER, "output", "output.nc")
        assert os.path.exists(nc_path), "output.nc not found"

    def test_metrics_json_exists(self):
        assert os.path.exists(METRICS_PATH), "metrics.json not found"

    def test_only_allowed_parameters_changed(self):
        changed = changed_nml_params(os.path.join(SIM_FOLDER, "glm3.nml"))
        disallowed = sorted(set(changed) - ALLOWED_CHANGED_PARAMS)
        assert not disallowed, f"Disallowed parameter changes detected: {disallowed}"

    def test_parameters_stay_within_published_ranges(self):
        values = load_numeric_params(os.path.join(SIM_FOLDER, "glm3.nml"), PARAM_BOUNDS.keys())
        for name, (lower, upper) in PARAM_BOUNDS.items():
            value = values[name]
            assert lower <= value <= upper, (
                f"{name}={value} outside published range [{lower}, {upper}]"
            )

    def test_reported_metrics_match_exact_verifier_metrics(self):
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)

        required = [
            "overall_rmse",
            "annual_deep_rmse",
            "summer_deep_rmse",
            "overall_n_pairs",
            "annual_deep_n_pairs",
            "summer_deep_n_pairs",
        ]
        for key in required:
            assert key in metrics, f"metrics.json missing key: {key}"

        sim_df = read_glm_output(os.path.join(SIM_FOLDER, "output", "output.nc"))
        obs_df = read_observations(os.path.join(SIM_FOLDER, "field_temp_oxy.csv"))
        expected = calculate_task_metrics(sim_df, obs_df)

        for key in ["overall_rmse", "annual_deep_rmse", "summer_deep_rmse"]:
            reported = float(metrics[key])
            actual = expected[key]
            assert abs(reported - actual) <= REPORT_TOLERANCE, (
                f"Reported {key} {reported:.4f} differs from verifier {actual:.4f}"
            )

        for key in ["overall_n_pairs", "annual_deep_n_pairs", "summer_deep_n_pairs"]:
            reported = int(metrics[key])
            actual = expected[key]
            assert reported == actual, f"Reported {key} {reported} differs from verifier {actual}"

    def test_rmse_threshold(self):
        sim_df = read_glm_output(os.path.join(SIM_FOLDER, "output", "output.nc"))
        obs_df = read_observations(os.path.join(SIM_FOLDER, "field_temp_oxy.csv"))
        metrics = calculate_task_metrics(sim_df, obs_df)
        assert metrics["overall_rmse"] < OVERALL_RMSE_THRESHOLD, (
            f"overall_rmse {metrics['overall_rmse']:.4f} >= {OVERALL_RMSE_THRESHOLD}"
        )
        assert metrics["annual_deep_rmse"] < ANNUAL_DEEP_RMSE_THRESHOLD, (
            f"annual_deep_rmse {metrics['annual_deep_rmse']:.4f} "
            f">= {ANNUAL_DEEP_RMSE_THRESHOLD}"
        )
        assert metrics["summer_deep_rmse"] < SUMMER_DEEP_RMSE_THRESHOLD, (
            f"summer_deep_rmse {metrics['summer_deep_rmse']:.4f} >= {SUMMER_DEEP_RMSE_THRESHOLD}"
        )

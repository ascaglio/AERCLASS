import argparse
import pandas as pd
from aerclass.classify import (
    classify_methodI,
    classify_methodII,
    classify_methodIII,
    classify_methodIVA,
    classify_methodIVB,
    classify_methodV,
    classify_methodVI
)
import os

def main():
    parser = argparse.ArgumentParser(
        description="Run AERCLASS classification with uncertainty analysis"
    )
    parser.add_argument("--input", "-i", required=True, help="Input Excel file")
    parser.add_argument("--method", "-m", required=True,
                        choices=["I", "II", "III", "IVA", "IVB", "V", "VI"],
                        help="Classification method to use")
    parser.add_argument("--aod_error", type=float, default=0.01,
                        help="Uncertainty in AOD (default: 0.01)")
    parser.add_argument("--ssa_error", type=float, default=0.03,
                        help="Uncertainty in SSA (default: 0.03)")
    parser.add_argument("--rri_error", type=float, default=0.04,
                        help="Uncertainty in RRI (default: 0.04)")
    parser.add_argument("--filter_aod", action="store_true",
                        help="Filter AOD values below 0.4")
    parser.add_argument("--output", "-o", default=None,
                        help="Output CSV file (default: input_filename_methodX.csv)")

    args = parser.parse_args()

    # Cargar datos
    data = pd.read_excel(args.input)

    # Armar parámetros
    filter_list = [args.filter_aod, 0.4]

    # Mapeo de método
    method_funcs = {
        "I": classify_methodI,
        "II": classify_methodII,
        "III": classify_methodIII,
        "IVA": classify_methodIVA,
        "IVB": classify_methodIVB,
        "V": classify_methodV,
        "VI": classify_methodVI
    }

    classify = method_funcs[args.method]

    # Llamar función
    outcome, df = classify(data, args.aod_error, filter_list)

    # Nombre de archivo de salida
    if args.output is None:
        base = os.path.splitext(os.path.basename(args.input))[0]
        args.output = f"{base}_method{args.method}.csv"

    # Guardar resultados
    outcome.to_csv(args.output, index=False)
    print(f"[✔] Misclassification results saved to: {args.output}")

if __name__ == "__main__":
    main()

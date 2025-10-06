import pandas as pd
import io

def ipo_ops(exchange_file: bytes, psp_file: bytes):
    # Load Exchange file
    # (Assuming column 2 contains the application number based on your original code)
    df_exchange = pd.read_csv(io.BytesIO(exchange_file), header=None, skiprows=1)
    df_exchange.rename(columns={2: 'applicationNumber'}, inplace=True)

    # Load PSP file
    df_psp = pd.read_csv(io.BytesIO(psp_file))

    # --- 1. Application Number Comparison ---
    exchange_apps = set(df_exchange['applicationNumber'].unique())
    psp_apps = set(df_psp['applicationNumber'].unique())

    exchange_only = exchange_apps - psp_apps
    psp_only = psp_apps - exchange_apps

    # --- 2. Reconciliation Status Analysis (Dynamic) ---
    # NOTE: This part is already dynamic! It analyzes ALL unique 'reconStatus' values found in df_psp.
    status_counts = df_psp['reconStatus'].value_counts().to_dict()

    # Store application numbers for each status
    status_applications = {}
    for status in df_psp['reconStatus'].unique():
        status_applications[status] = df_psp[df_psp['reconStatus'] == status]['applicationNumber'].astype(str).tolist()

    # --- 3. Sequence Number Mismatch Calculation ---
    df_seq_mismatch = df_psp[df_psp['reconStatus'] == 'SEQUENCE_NUMBER_MISMATCH'].copy()

    # Convert sequence numbers to numeric, coercing errors (important for comparison)
    df_seq_mismatch['PSPSeqNo'] = pd.to_numeric(df_seq_mismatch['PSPSeqNo'], errors='coerce')
    df_seq_mismatch['ExchangeSeqNo'] = pd.to_numeric(df_seq_mismatch['ExchangeSeqNo'], errors='coerce')
    df_seq_mismatch.dropna(subset=['PSPSeqNo', 'ExchangeSeqNo'], inplace=True)

    # Identify applications where ExchangeSeqNo > PSPSeqNo
    greater_seq_apps = df_seq_mismatch[
        df_seq_mismatch['ExchangeSeqNo'] > df_seq_mismatch['PSPSeqNo']
    ]['applicationNumber'].astype(str).tolist() # Convert to string list for JSON

    # Return results as dictionary (JSON serializable)
    return {
        "exchange_unique_count": len(exchange_apps),
        "psp_unique_count": len(psp_apps),
        "exchange_only_count": len(exchange_only),
        "psp_only_count": len(psp_only),
        "status_counts": status_counts,
        "status_applications": status_applications,
        "greater_seq_count": len(greater_seq_apps),
        "greater_seq_mismatch_apps": greater_seq_apps
    }
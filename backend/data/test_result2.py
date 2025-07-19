import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Thiết lập
file_path_1 = 'results2_Revised.xlsx'
file_path = 'results_new_Revised.xlsx'
output_dir = 'evaluation_results_revised'
os.makedirs(output_dir, exist_ok=True)
thresholds = np.arange(0, 1.01, 0.01)

# Đọc dữ liệu
xl1 = pd.ExcelFile(file_path_1)
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names
sheet_names_1 = xl1.sheet_names

# Hàm đánh giá và vẽ biểu đồ cho mỗi sheet
def evaluate_and_plot(df, name):
    results = []
    for t in thresholds:
        pred = (df['score'] >= t).astype(int)
        tp = ((pred == 1) & (df['flag'] == 1)).sum()
        tn = ((pred == 0) & (df['flag'] == 0)).sum()
        fp = ((pred == 1) & (df['flag'] == 0)).sum()
        fn = ((pred == 0) & (df['flag'] == 1)).sum()
        prec = tp / (tp + fp) if (tp + fp) else 0
        rec = tp / (tp + fn) if (tp + fn) else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0
        results.append([t, tp, tn, fp, fn, rec, prec, f1])
    
    df_result = pd.DataFrame(results, columns=['threshold', 'TP', 'TN', 'FP', 'FN', 'Recall', 'Precision', 'F1'])
    df_result.to_csv(f"{output_dir}/{name}_evaluation.csv", index=False)
    

    plt.figure(figsize=(10, 6))
    for col in ['Recall', 'Precision', 'F1']:
        label = ""
        if col == 'Recall': label = 'Полнота'
        if col == 'Precision': label = 'Точность'
        if col == 'F1': label = 'F1-мера'
        plt.plot(df_result['threshold'], df_result[col], label=label)
    plt.title(f'Полнота, Точность, F1-мера')
    plt.xlabel('Порог'); plt.ylabel('Оценка'); plt.grid(True); plt.legend()
    plt.savefig(f"{output_dir}/{name}_metrics_plot.png")
    plt.close()

    return df_result[ df_result['F1'] == max(df_result['F1'])]

# Đánh giá từng sheet
all_data = pd.DataFrame()
# for sheet in sheet_names:
#     df = xls.parse(sheet)
#     if 'score' in df.columns and 'flag' in df.columns:
#         # evaluate_and_plot(df, sheet)
#         all_data = pd.concat([all_data, df[['score', 'flag']]], ignore_index=True)
for sheet in sheet_names_1:
    df = xl1.parse(sheet)
    if 'score' in df.columns and 'flag' in df.columns:
        # evaluate_and_plot(df, sheet)
        all_data = pd.concat([all_data, df[['score', 'flag']]], ignore_index=True)

# Đánh giá tổng hợp
print(evaluate_and_plot(all_data, "overall"))


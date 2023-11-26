import pandas as pd
import matplotlib.pyplot as plt

# ファイルパス（変数を直接使用）
csv_file_path = r'C:\Users\sakim\python_data_analysis\customer_master.csv'
customer_master = pd.read_csv(csv_file_path)
print(customer_master.head())

transaction1_file_path = r'C:\Users\sakim\python_data_analysis\transaction_1.csv'
transaction_1 = pd.read_csv(transaction1_file_path)
transaction_1.head()

transaction2_file_path = r'C:\Users\sakim\python_data_analysis\transaction_2.csv'
transaction_2 = pd.read_csv(transaction2_file_path)
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
print(transaction.head())


print(len(transaction_1))
print(len(transaction_2))
print(len(transaction))


transaction_detail_1_file_path = r'C:\Users\sakim\python_data_analysis\transaction_detail_1.csv'
transaction_detail_1 = pd.read_csv(transaction_detail_1_file_path)

transaction_detail_2_file_path = r'C:\Users\sakim\python_data_analysis\transaction_detail_2.csv'
transaction_detail_2 = pd.read_csv(transaction_detail_2_file_path)
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)
print(transaction_detail.head())

print(len(transaction_detail_1))
print(len(transaction_detail_2))
print(len(transaction_detail))

join_data = pd.merge(transaction_detail, transaction[["transaction_id", "payment_date", "customer_id"]], on="transaction_id", how="left")
print(join_data.head())

print(len(transaction_detail))
print(len(transaction))
print(len(join_data))
#transactionとjoin_dataの件数が一致＝横にデータが増えた

csv_file_path = r'C:\Users\sakim\python_data_analysis\item_master.csv'
item_master = pd.read_csv(csv_file_path)

join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
join_data = pd.merge(join_data, item_master, on="item_id", how="left")
print(join_data.head())

join_data["price"] = join_data["quantity"] * join_data["item_price"]
print(join_data[["price", "quantity", "item_price"]].head())

# データ検算
print(join_data["price"].sum()== transaction["price"].sum())

# 0件のため、欠損値はなし
print(join_data.isnull().sum())
# データ集約
print(join_data.describe())
# データの対象期間
print(join_data["payment_date"].min())
print(join_data["payment_date"].max())

print(join_data.dtypes)
join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")
print(join_data[["payment_date", "payment_month"]].head())

print(join_data.groupby("payment_month")["price"].sum())
# 月別、商品別で集約。複数渡す場合は[]で囲む
print(join_data.groupby(["payment_month", "item_name"])[["price", "quantity"]].sum())

#index(縦の行)、columns(横の行)でKEYに相当
print(pd.pivot_table(join_data, index = "item_name", columns = "payment_month", values = ["price", "quantity"], aggfunc = "sum"))

graph_data = pd.pivot_table(join_data, index = "payment_month", columns = "item_name", values = "price", aggfunc = "sum")
print(graph_data.head())


# matplotlibを使ってグラフを描画
plt.figure(figsize=(10, 6))
for column in graph_data.columns:
    plt.plot(graph_data.index, graph_data[column], marker='o', label=column)

# グラフのタイトルと軸ラベルの追加
plt.title('Monthly Sales Data')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.show()

# https://www.shuwasystem.co.jp/support/7980html/6727.html

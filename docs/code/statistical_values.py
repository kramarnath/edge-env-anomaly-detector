import pandas as pd

df = pd.read_csv("feeds.csv")
df.drop(columns=["created_at", "entry_id", "latitude", "longitude", "elevation", "status"], inplace=True)
print(df.head())
df.rename(columns={"field1" : "temperature", "field2" : "humidity"}, inplace=True)
print(df.head())

# Statistical Values
temp_mean = df['temperature'].mean()
temp_std = df['temperature'].std()

humi_mean = df['humidity'].mean()
humi_std = df['humidity'].std()

max_temp_roc= df['temperature'].diff().abs().max()
max_humi_roc= df['humidity'].diff().abs().max()

print("=== Values (Max, Min, Change/min) ===")
print(f"Temp Min (Mean - 3 Std): {temp_mean - (3 * temp_std):.2f} °C") # taking in the range of  3 SD
print(f"Temp Max (Mean + 3 Std): {temp_mean + (3 * temp_std):.2f} °C")

print(f"Max Expected Temp Change per Min: {max_temp_roc:.2f} °C")

print("-----------------------------------")

print(f"Humidity Min (Mean - 3 Std): {humi_mean - (3 * humi_std):.2f} %") # taking in the range of  3 SD
print(f"Humidity Max (Mean + 3 Std): {humi_mean + (3 * humi_std):.2f} %") # taking in the range of  3 SD

print(f"Max Expected Humidity Change per Min: {max_humi_roc:.2f} %")
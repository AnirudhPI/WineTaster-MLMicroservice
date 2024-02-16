import pandas as pd
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf

df = pd.read_csv(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)) + '/dataset/wineQualityReds.csv')

df.drop(inplace=True,columns=["Sr"])
df.dropna(inplace=True)
label="quality"

train_df, test_df = train_test_split(df, test_size=0.2, shuffle=True)

print("Number of training samples: ",len(train_df))
print("Number of testing sample: ",len(test_df))

x_train_df = train_df.drop([label], axis=1)
y_train_df = train_df[label]
y_train_df = pd.get_dummies(y_train_df)

x_test_df = test_df.drop([label], axis=1)
y_test_df = test_df[label]
y_test_df = pd.get_dummies(y_test_df)


NUM_COLUMNS = len(x_train_df.columns)
OUTPUT_LEN=len(y_train_df.columns)

OPTIMIZER="sgd"
LOSS=tf.keras.losses.CategoricalCrossentropy()
METRICS=['accuracy']
EPOCHS=200

model = tf.keras.Sequential([
  tf.keras.layers.Input(shape=(NUM_COLUMNS,)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(64, activation='relu'),
  tf.keras.layers.Dropout(0.4),
  tf.keras.layers.Dense(32, activation='relu'),
  tf.keras.layers.Dropout(0.4),
  tf.keras.layers.Dense(OUTPUT_LEN, activation='softmax')
])

model.compile(optimizer=OPTIMIZER, loss=LOSS, metrics=METRICS)
model.fit(x_train_df,y_train_df,epochs=EPOCHS)


test_loss, test_accuracy = model.evaluate(x_test_df,y_test_df)
print(f"Evaluation Accuracy: {test_accuracy}")

model.save("saved_model/1")
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from delta.tables import *

spark = (
    SparkSession.builder
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")



print("Reading CSV file from S3...")

schema = "PassengerId int, Survived int, Pclass int, Name string, Sex string, Age double, SibSp int, Parch int, Ticket string, Fare double, Cabin string, Embarked string"
df = spark.read.csv(
    "s3://pucminas-orquestracao/raw/titanic", 
    header=True, schema=schema, sep=";"
)

print("Writing titanic dataset as a delta table...")
df.write.format("delta").mode("overwrite").save("s3://pucminas-orquestracao/silver//titanic_delta")

print("Indicador 01 - Total de passageiros por sexo e classe")
new1 = df.groupby(['Sex','Pclass']).agg({
    "PassengerId":"sum"
}).reset_index()
new1.rename(columns = {'PassengerId':'total_passageiros'}, inplace = True)


print("Indicador02 -  Preço médio da tarifa pago por sexo e classe (produzir e escrever)")
new2 = df.groupby(['Sex','Pclass']).agg({
    "Fare":"mean"
}).reset_index()    
new2.rename(columns = {'Fare':'preco_medio'}, inplace = True)
new2['preco_medio'] = new2['preco_medio'].round(decimals = 2)


print("Create a delta table object...")
old = DeltaTable.forPath(spark, "s3://pucminas-orquestracao/silver/titanic_delta")

print("UPSERT...")
# UPSERT
(
    old.alias("old")
    .merge(new1.alias("new1"), 
    "old.PassengerId = new1.PassengerId"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

(
    old.alias("old")
    .merge(new2.alias("new2"), 
    "old.PassengerId = new2.PassengerId"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

print("Checking if everything is ok")
print("New data...")

(
    spark.read.format("delta")
    .load("s3://pucminas-orquestracao/silver/titanic_delta")
   # .where("PassengerId < 6 OR PassengerId > 888")
    .show()
)

old.generate("symlink_format_manifest")

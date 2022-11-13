from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.window import Window as w

def write_parquet(df, folder, mode):
    data = (
        df
        .write
        .mode(mode)
        .format('parquet')
        .save(folder)
    )
    return data

def read_parquet(sp, folder):
    spark = (
        sp
        .read
        .parquet(folder)
    )
    return spark

overwrite_opt = True

def get_writemode ():
    return 'overwrite'

spark = ( SparkSession.\
        builder.\
        appName("pyspark-titanic").\
        getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

raw_folder_path = "s3://pucminas-orquestracao/raw/titanic/"
raw_sep = ";"
raw_header = True
raw_enconding = "latin1"

parquet_folder_path = "s3://pucminas-orquestracao/silver/titanic_delta/"

print("Reading CSV file from S3...")
data = spark.read.option("encoding", raw_enconding).csv(path=raw_folder_path, sep=raw_sep, header=raw_header)

data = (
    data
        .select(["PassengerId", "Survived", "Pclass", "Name", 
                     "Sex", "Age", "SibSp", "Parch", 
                     "Ticket", "Fare", "Cabin", 
                     "Embarked"])
        
        .withColumn("PassengerId", f.col("PassengerId").cast("int"))
        .withColumn("Survived", f.col("Survived").cast("int"))
        .withColumn("Pclass", f.col("Pclass").cast("int"))
        .withColumn("Name", f.col("Name").cast("string"))
        .withColumn("Sex", f.col("Sex").cast("string"))
        .withColumn("Age", f.col("Age").cast("double"))
        .withColumn("SibSp", f.col("SibSp").cast("int"))
        .withColumn("Parch", f.col("Parch").cast("int"))
        .withColumn("Ticket", f.col("Ticket").cast("string"))
        .withColumn("Fare", f.col("Fare").cast("double"))
        .withColumn("Cabin", f.col("Cabin").cast("string"))
        .withColumn("Embarked", f.col("Embarked").cast("string"))
)

# escreve parquet
write_parquet(data, parquet_folder_path, get_writemode(overwrite_opt))
allparquet = read_parquet(spark, parquet_folder_path)
df = read_parquet(spark, parquet_folder_path)

print("Indicador 01 - Total de passageiros por sexo e classe")
new1 = (
             df
                 .groupBy("Sex", "Pclass")
                 .agg(
                    f.sum("PassengerId").cast("int").alias("total_passageiros"),
                 )
            )

total_pas_sex_class = parquet_folder_path+'total_pas_sex_class/'
write_parquet(new1, total_pas_sex_class, get_writemode(overwrite_opt))
total_pas_sex_classparquet = read_parquet(spark, total_pas_sex_class)

print("Indicador02 -  Preço médio da tarifa pago por sexo e classe (produzir e escrever)")
new2 = (
             df
                 .groupBy("Sex", "Pclass")
                 .agg(
                    f.mean("Fare").cast("decimal(10,2)").alias("preco_medio"),
                 )
            )

media_preco_sex_class = parquet_folder_path+'media_preco_sex_class/'
write_parquet(new2, media_preco_sex_class, get_writemode(overwrite_opt))
media_preco_sex_classparquet = read_parquet(spark, media_preco_sex_class)
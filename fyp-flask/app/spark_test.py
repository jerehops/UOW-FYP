from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import sys, requests, json
import seaborn as sns

# create spark configuration
spark_conf = SparkConf().setAppName("Media analytic").setMaster("local[*]")

sc = SparkContext.getOrCreate(spark_conf)
spark = SparkSession.builder.master("local[*]").getOrCreate() # config used to format output tables better
spark.conf.set("spark.sql.repl.eagerEval.enabled", True)


def load_csv_file(file_path):
    """Load CSV file and drop entry with na"""
    response_df = spark.read.options(header='True', inferSchema=True) \
        .csv(file_path)
    response_df.na.drop()
    return response_df

def get_columns_value(df):
    """
    This function will return a dictionary(columns key) pointing to a list of unique value in the columns
    Expected input: dataframe, 
    Expected output: a Dictionary contain multiple list.
    
    """
    unique_value_dictionary = {}
    headers_list = df.schema.names
    print(headers_list)
    if 'timestamp' in headers_list:
        headers_list.remove('timestamp')
    print(headers_list)
    for header in headers_list:
        unique_value_dictionary[header] = df.select(F.collect_set(header).alias(header)).first()[header]
    return unique_value_dictionary

## this one dynamic
movie_df = load_csv_file("opt/app/data/default/movies.csv")
ratings_df = load_csv_file("opt/app/data/default/ratings.csv")
movie_rating_df = movie_df.join(ratings_df, 'movieId', 'left')
movie_rating_unique_dictionary = get_columns_value(movie_rating_df)

def create_dataframe (dataframe, x_axis, filtering):
    dataframe.createOrReplaceTempView("temp_view_item")
    if filtering:
        filter_columns_name = list(filtering.keys())[0]
        query_statement = f'select {x_axis} from temp_view_item where {filter_columns_name} = "{filtering[filter_columns_name]}"'
    else:
        query_statement = f'select {x_axis} from temp_view_item'
    df = (spark.sql(query_statement)).toPandas()
    if filtering:
        fig = sns.histplot(data=df, x=x_axis).set_title(f"'{x_axis}' distribution of '{filter_columns_name}': '{filtering[filter_columns_name]}'").get_figure()
    else:
        fig = sns.histplot(data=df, x=x_axis).set_title(f"'{x_axis}' distribution").get_figure()
    return fig

create_dataframe(movie_rating_df , 'rating' , {"title": "U2: Rattle and Hum (1988)"} )

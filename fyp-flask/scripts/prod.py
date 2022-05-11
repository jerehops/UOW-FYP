from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import requests
import base64
import io
import sys
from datetime import datetime
import seaborn as sns
import json


# create spark configuration
spark_conf = SparkConf().setAppName("Media analytic")
#sc = SparkContext.getOrCreate(spark_conf)
# config used to format output tables better
spark = SparkSession.builder.getOrCreate()
spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
spark.conf.set("spark.sql.shuffle.partitions",
               spark.sparkContext.defaultParallelism)

"""Variable that will change during testing"""
# Production
url = "http://flask:8000/updateData"
# Local testing
#url = "http://localhost:8000/updateData"

# Production
movies_dev_path = "/opt/data/default/movie/movies.csv"
ratings_dev_path = "/opt/data/default/movie/ratings.csv"
# for local testing only.
#movies_dev_path = "/Users/kmeng/Desktop/movies.csv"
#ratings_dev_path = "/Users/kmeng/Desktop/ratings.csv"

user_id = sys.argv[1]


def main():
    data_Str = sys.argv[2]
    print(f"str received from frontend{data_Str}")
    parsed_data = parse_data(data_Str)
    df = _get_dataframe(parsed_data['csv_location'])
    parsed_data['data_frame'] = df
    print(f"Parsed data:{parsed_data}")
    plot_fig(parsed_data)


def test():
    #movie_rating_unique_dictionary = get_columns_value(movie_rating_df)
    print("WE ARE CURRENTLY RUNNING DUMMY DATE")
    test_data_Str = json.dumps({'plot_type': 'histogram', 'csv_location': 'movie_dataset',
                               'x_axis': 'rating', "filter1": {'title': "U2: Rattle and Hum (1988)"}})
    test_parsed_data = parse_data(test_data_Str)
    df = _get_dataframe(test_parsed_data['csv_location'])
    test_parsed_data['data_frame'] = df
    print(f"Parsed data:{test_parsed_data}")
    plot_fig(test_parsed_data)


def _get_dataframe(dataframe_path: str):
    """Return a dataframe depending on the job, 
       if we are processing existing data we will just load the path we know,if not we will load from the path provided
    """
    if dataframe_path == "movie_dataset":
        movie_df = load_csv_file(movies_dev_path)
        ratings_df = load_csv_file(ratings_dev_path)
        response_df = movie_df.join(ratings_df, 'movieId', 'left')

    else:
        response_df = load_csv_file(dataframe_path)
    return response_df


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
        unique_value_dictionary[header] = df.select(
            F.collect_set(header).alias(header)).first()[header]
    return unique_value_dictionary


def plot_histogram(dataframe, x_axis: str, filtering: list):
    dataframe.createOrReplaceTempView("temp_view_item")
    if filtering:
        filtering_str = ""
        for fliter in filtering:
            for columns_name, columns_filter in fliter.items():
                if filtering_str == "":
                    filtering_str = f'{columns_name} = "{columns_filter}"'
                else:
                    f'{filtering_str} and {columns_name} = "{columns_filter}"'

        query_statement = f'select {x_axis} from temp_view_item where {filtering_str}'
        print(query_statement)
    else:
        query_statement = f'select {x_axis} from temp_view_item'
    print(f"Starting Spark Sql Query .........")
    try:
        df = spark.sql(query_statement)
        print("Transfer dataframe into pandas")
        df = df.toPandas()
    except Exception as e:
        print(f"Error during SQL Query....")
        print(e)
    print(f"Spark Sql Query Query completed, plotting figure....")
    if filtering:
        fig = sns.histplot(data=df, x=x_axis).set_title(
            f"'{x_axis}' distribution of '{filtering_str}'").get_figure()
    else:
        fig = sns.histplot(data=df, x=x_axis).set_title(
            f"'{x_axis}' distribution").get_figure()
    print(f"Figure plotted, posting figure ....")
    post_fig(fig)


def post_fig(fig):

    print(f"Posting image to {url} for account user {user_id}")
    s = io.BytesIO()
    fig.savefig(s, format='jpg')
    s.seek(0)
    myimg = base64.b64encode(s.read()).decode("utf8")
    request_data = {"image": myimg, "user_id": user_id,
                    "timestamp": (datetime.now().strftime("%d-%m-%Y, %H:%M"))}
    requests.post(url, data=request_data)


def plot_scatter(dataframe, x_axis: str, y_axis: str, filtering: list):
    """Place holder"""
    fig = "a"
    return fig


def parse_data(data_str: str) -> dict:
    """
    This function is for massaging the string data input we received and transform it into a dictionary. 
    Most of the value will be string, exception for:
        -'filter_list' will be a list, (if can be an empty list if user don't need the filter)
    """
    response_dict = {}
    response_dict['filter_list'] = []
    data_dict = json.loads(data_str)
    for key, value in data_dict.items():
        if key == 'csv_location':
            response_dict['csv_location'] = value
        elif key == 'plot_type':
            response_dict['plot_type'] = value
        elif key == 'x_axis':
            response_dict['x_axis'] = value
        elif 'filter' in key:
            response_dict['filter_list'].append(value)
        else:
            raise ValueError('unidentified key value received')
    return response_dict


def plot_fig(parsed_data):
    """
    This function will determine what kind of plot function it will use. 
    Depending on plot_type key word.
    """
    if parsed_data['plot_type'] == 'histogram':
        plot_histogram(
            parsed_data['data_frame'], parsed_data['x_axis'], parsed_data['filter_list'])
    elif parsed_data['plot_type'] == 'scatter':
        plot_scatter()
    else:
        raise ValueError("Plot type not recognised.")


if __name__ == "__main__":
    # dummy request for testing in isolation
    test()

    # prod
    # main()

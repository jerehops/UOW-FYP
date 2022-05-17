from pyspark import SQLContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import requests
import base64
import io
import sys
from datetime import datetime
import seaborn as sns
import json
from pyspark.sql.functions import countDistinct
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import textwrap
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
sns.set_theme(style="whitegrid")


task_id = sys.argv[1]
user_id = sys.argv[2]
errorCount = 0
# create spark configuration
spark_conf = SparkConf().setAppName(task_id)
#sc = SparkContext.getOrCreate(spark_conf)
# config used to format output tables better
spark = SparkSession.builder.getOrCreate()
spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
spark.conf.set("spark.sql.shuffle.partitions",
               spark.sparkContext.defaultParallelism)
spark.conf.set('spark.sql.caseSensitive', False)
#sqlContext = SQLContext(spark.sparkContext)
#sqlContext.sql("set spark.sql.caseSensitive=false")


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
#movies_dev_path = "/d/ubuntudev/qbox-blog-code/ch_6_toy_saas/movies.csv"
#ratings_dev_path = "/d/ubuntudev/qbox-blog-code/ch_6_toy_saas/ratings.csv"

def main():
    try:
        data_Str = sys.argv[3]
        parsed_data = parse_data(data_Str)
        print("Completed parse data")
        df = _get_dataframe(parsed_data['filename'])
        print("Completed df")
        parsed_data['data_frame'] = df
        print(f"Parsed data:{parsed_data}")
        plot_fig(parsed_data)
    except Exception as e:
        print(e)
        post_error()

def _get_dataframe(filename: str):
    """Return a dataframe depending on the job, 
       if we are processing existing data we will just load the path we know,if not we will load from the path provided
    """
    if filename == "movie_dataset":
        movie_df = load_csv_file(movies_dev_path)
        ratings_df = load_csv_file(ratings_dev_path)
        response_df = movie_df.join(ratings_df, on='movieId')
    else:
        full_path = f"/opt/data/uploads/{user_id}/{filename}"
        print("This is the full path " +full_path)
        response_df = load_csv_file(full_path)
    return response_df


def load_csv_file(file_path):
    """Load CSV file and drop entry with na"""
    response_df = spark.read.options(header='True', inferSchema=True) \
        .csv(file_path)
    response_df.na.drop()
    return response_df

def plot_histogram(dataframe, x_axis: str, filtering: list):
    dataframe.createOrReplaceTempView("temp_view_item")
    if filtering:
        filtering_str = ""
        filtering_str_for_figure = ""
        for fliter in filtering:
            for columns_name, columns_filter in fliter.items():
                if filtering_str == "":
                    filtering_str = f'{columns_name} = "{columns_filter}"'
                    filtering_str_for_figure = f'{columns_name} = "{columns_filter}"'
                else:
                    filtering_str = f'{filtering_str} & {columns_name} = "{columns_filter}"'
                    filtering_str_for_figure = f'{filtering_str} \n & {columns_name} = "{columns_filter}"'

        query_statement = f'select COUNT(*), {x_axis} from temp_view_item where {filtering_str} GROUP BY {x_axis} ORDER BY {x_axis}'
        print(query_statement)
    else:
        query_statement = f'select COUNT(*), {x_axis} from temp_view_item GROUP BY {x_axis} ORDER BY {x_axis}'
        print(query_statement)
    print(f"Starting Spark Sql Query .........")
    try:
        df = spark.sql(query_statement)
        print(df)
        print("Transform dataframe into pandas")
        panda_df = df.toPandas()
        panda_df[x_axis] = panda_df[x_axis].apply(lambda row: '\n'.join(textwrap.wrap(row, 10)))
        print(panda_df)
    except Exception as e:
        print(f"Error during SQL Query....")
        print(e)
    print(f"Spark Sql Query Query completed, plotting figure....")
    
    plt.ticklabel_format(style='plain', axis='y', useOffset=False)
    fig, ax = plt.subplots(figsize=(9, 9))
    
    ## If the number of x-axis is more than 10, we will display randomly 10 of the row 
    if panda_df.dtypes[x_axis] == object:
        print("x-axis is string type data")
    if panda_df.shape[0] > 10 and panda_df.dtypes[x_axis]:
        print(f"Number of x-axis is more than 10, we will display top 10 of the row")
        #panda_df = panda_df.sample(n=10)
        panda_df = panda_df.nlargest(10, "count(1)")
        plt.tick_params('x', rotation=45, labelsize = 6)

    if filtering:
        fig = sns.barplot(x=x_axis, y="count(1)", data=panda_df).set_title(
            f"{x_axis} distribution of {filtering_str_for_figure}")
    else:
        fig = sns.barplot(x=x_axis, y="count(1)", data=panda_df).set_title(
            f"{x_axis} distribution")
    plt.ticklabel_format(style='plain', axis='y')
    ax.set(ylabel='Count')
    fig = plt.gcf()
    print(f"Figure plotted, posting figure ....")
    post_fig(fig)


def plot_pie_chart(dataframe, x_axis: str, filtering: list):
    dataframe.createOrReplaceTempView("temp_view_item")
    if filtering:
        filtering_str = ""
        filtering_str_for_figure = ""
        for fliter in filtering:
            for columns_name, columns_filter in fliter.items():
                if filtering_str == "":
                    filtering_str = f'{columns_name} = "{columns_filter}"'
                    filtering_str_for_figure = f'{columns_name} = "{columns_filter}"'
                else:
                    filtering_str = f'{filtering_str} & {columns_name} = "{columns_filter}"'
                    filtering_str_for_figure = f'{filtering_str} \n & {columns_name} = "{columns_filter}"'

        query_statement = f'select COUNT(*), {x_axis} from temp_view_item where {filtering_str} GROUP BY {x_axis} ORDER BY {x_axis}'
        print(query_statement)
    else:
        query_statement = f'select COUNT(*), {x_axis} from temp_view_item GROUP BY {x_axis} ORDER BY {x_axis}'
    print(f"Starting Spark Sql Query .........")
    try:

        df = spark.sql(query_statement)
        print("Transform dataframe into pandas")
        panda_df = df.toPandas()
        if panda_df.shape[0] > 10 :
            print(f"Number of x-axis is more than 10, we will display top 10 of the row")
            #panda_df = panda_df.sample(n=10)
            panda_df = panda_df.nlargest(10, "count(1)")
        panda_df[x_axis] = panda_df[x_axis].apply(lambda row: '\n'.join(textwrap.wrap(row, 25)))
        label_list = panda_df[x_axis].tolist()
        print(label_list)
        value_list = panda_df['count(1)'].tolist()
        print(value_list)
    except Exception as e:
        print(f"Error during SQL Query....")
        print(e)
    print(f"Spark Sql Query Query completed, plotting figure....")
    fig, ax = plt.subplots(figsize=(7, 5))


    colors = sns.color_palette('bright')[0:5]
    s = io.BytesIO()
    s.seek(0)
    plt.pie(value_list, labels=label_list, colors=colors, textprops={'fontsize': 10})
    if filtering:
        plt.title(f"{x_axis} distribution of {filtering_str_for_figure}")
    else:
        plt.title(f"{x_axis} distribution")
    fig = plt.gcf()
    print(f"Figure plotted, posting figure ....")
    post_fig(fig)


def post_fig(fig):
    print(f"Posting image to {url} for account user {user_id}")
    s = io.BytesIO()
    fig.savefig(s, format='jpg')
    #fig.savefig("test.png", format='jpg') #local testing purpose
    s.seek(0)
    myimg = base64.b64encode(s.read()).decode("utf8")
    request_data = {"image": myimg, "user_id": user_id, "task_id": task_id,
                    "timestamp": (datetime.now().strftime("%d-%m-%Y, %H:%M")), "error": "false"}
    requests.post(url, data=request_data)


def post_error():
    request_data = {"image": "", "user_id": user_id, "task_id": task_id,
                    "timestamp": (datetime.now().strftime("%d-%m-%Y, %H:%M")), "error": "true"}
    requests.post(url, data=request_data)


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
        print(f"Key={key}, value={value}")
        if key == 'filename':
            response_dict['filename'] = value
        elif key == 'plot_type':
            response_dict['plot_type'] = value
        elif key == 'x-axis':
            response_dict['x-axis'] = value
        elif 'filters' in key:
            response_dict['filter_list'].append(value)
    return response_dict


def plot_fig(parsed_data):
    """
    This function will determine what kind of plot function it will use. 
    Depending on plot_type key word.
    """
    if parsed_data['plot_type'] == 'histogram':
        plot_histogram(
            parsed_data['data_frame'], parsed_data['x-axis'], parsed_data['filter_list'])
    elif parsed_data['plot_type'] == 'piechart':
        plot_pie_chart(
            parsed_data['data_frame'], parsed_data['x-axis'], parsed_data['filter_list'])


# Test functions

def test_histogram():
    #movie_rating_unique_dictionary = get_columns_value(movie_rating_df)
    print("WE ARE CURRENTLY RUNNING DUMMY DATE")
    test_data_Str = json.dumps({'plot_type': 'histogram', 'filename': 'movie_dataset',
                               'x-axis': 'title'})
    # test_data_Str = json.dumps({'plot_type': 'histogram', 'filename': 'movie_dataset',
    #                            'x-axis': 'rating', "filters": {'title': "U2: Rattle and Hum (1988)"}})
    test_parsed_data = parse_data(test_data_Str)
    df = _get_dataframe(test_parsed_data['filename'])
    test_parsed_data['data_frame'] = df
    print(f"Parsed data:{test_parsed_data}")
    plot_fig(test_parsed_data)


def test_pie_chart():
    print("WE ARE CURRENTLY RUNNING DUMMY DATE")
    test_data_Str = json.dumps({'plot_type': 'piechart', 'filename': 'movie_dataset',
                               'x-axis': 'rating'})
    #test_data_Str = json.dumps({'plot_type': 'piechart', 'filename': 'movie_dataset',
    #                           'x-axis': 'rating', "filters": {'title': "U2: Rattle and Hum (1988)"}})
    test_parsed_data = parse_data(test_data_Str)
    df = _get_dataframe(test_parsed_data['filename'])
    test_parsed_data['data_frame'] = df
    print(f"Parsed data:{test_parsed_data}")
    plot_fig(test_parsed_data)


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


if __name__ == "__main__":
    # dummy request for testing in isolation
    #test_histogram()
    #test_pie_chart()

    # prod
    main()

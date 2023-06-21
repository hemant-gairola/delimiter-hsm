#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import os
from datetime import datetime

import pyarrow as pa
import pyarrow.csv as csv
import pyarrow.dataset as ds

# from pyspark.sql import SparkSession
# import pyspark
# import glob


def split_arrow_without_slice(
    input_file="",
    delimiter=",",
    column_names=None,
    output_file_dir="",
    split_row_count="1",
):
    start_function = datetime.now()
    print(f"Start time : {start_function}")
    # Create output directory in case it is no there
    os.makedirs(name=output_file_dir, exist_ok=True)
    print(f"Start time : {start_function}")

    read_options = csv.ReadOptions(column_names=column_names)
    # Define csv parse option
    parse_option = csv.ParseOptions(
        delimiter=delimiter,
    )
    print(f"Start time : {start_function}")
    # Define Schema
    schema_new = pa.schema(
        [
            pa.field("id", pa.string()),
            pa.field("name", pa.string()),
            pa.field("roll", pa.string()),
        ]
    )
    # Define csv convert option
    convert_option = csv.ConvertOptions(strings_can_be_null=True)
    print(f"Start time : {start_function}")
    # Read the csv file into arrow table

    csvParseOpts = ds.CsvFileFormat(
        parse_options=parse_option,
        convert_options=convert_option,
        read_options=read_options,
    )

    file_name_without_extension = os.path.split(input_file)[1].split(".")[0]
    # Convert data into table
    table = ds.dataset(input_file, format=csvParseOpts)
    print(
        f"Elapsed time to convert data into arrow table : {datetime.now() - start_function}"
    )

    print(f"Table information : {table}")
    schema = table.schema

    print(f"Schema is  {schema_new}")
    print(f"Data is  {table.to_table()}")
    # column_name = schema.names
    # total_rows = table.count_rows()
    print(
        f"Elapsed time to fetch schema information : {datetime.now() - start_function}"
    )

    # parse_option = csv.ParseOptions(delimiter="\t")
    write_options = csvParseOpts.make_write_options(include_header=False)
    print(
        f"Elapsed time to set make_write_operation : {datetime.now() - start_function}"
    )
    start_split = datetime.now()
    # new_csv_parse_options = ds.CsvFileFormat(parse_options=parse_option, convert_options=convert_option)
    ds.write_dataset(
        data=table,
        base_dir=str(output_file_dir),
        basename_template=str(file_name_without_extension) + "_{i}.csv",
        format=csvParseOpts,
        max_rows_per_file=int(split_row_count),
        max_rows_per_group=int(split_row_count),
        file_options=write_options,
        schema=schema,
        existing_data_behavior="delete_matching",
    )
    print(
        f"Elapsed time for splitting {datetime.now()} and {start_split} : {datetime.now() - start_split}"
    )
    print(
        f"Elapsed time for Overall {datetime.now()} and {start_function} : {datetime.now() - start_function}"
    )
    print(f"Execution is finish!!")

import subprocess
import json
import pandas as pd
import sqlalchemy


# Load the sql connection file
sql_url = json.load(open("sql_connection.json", "r"))['spot_db']
# Connect to the db
db = sqlalchemy.create_engine(
    sql_url,
    echo=False,
).connect()

# For each region below:
for region in ["us-east-1", "us-east-2", "us-west-1", "us-west-2"]:
    # Create a subprocess to run the below
    prices = subprocess.check_output(
        f"aws ec2 describe-spot-price-history --region {region}", shell=True
    )
    # Load the json into a list of dicts (key SpotPriceHistory is the only one)
    prices = json.loads(prices)["SpotPriceHistory"]

    # Pandas dataframe from the list of dicts
    df = pd.DataFrame.from_records(prices)

    # For each availability zone in the list
    for region in [df["AvailabilityZone"].unique()[0]]:
        # Filter down to only that AZ
        temp_df_region = df[df["AvailabilityZone"] == region]
        # For each instance type in that AZ:
        for instance_type in temp_df_region["InstanceType"].unique():
            # Filter the temp df further to just the instance
            temp = temp_df_region[temp_df_region["InstanceType"] == instance_type]
            # Drop the redundant cols
            temp = temp.drop(columns=["AvailabilityZone", "InstanceType"])
            # Dump it in mysql, with region_instance type as the table name. E.G.- us-east-1a_a1.large
            temp.to_sql(
                f"{region}_{instance_type}",
                con=db,
                index=False,
                if_exists="replace",
                dtype={
                    "ProductDescription": sqlalchemy.types.VARCHAR(length=32),
                    "SpotPrice": sqlalchemy.types.Float(),
                    "Timestamp": sqlalchemy.types.VARCHAR(length=32),
                },
            )

            # Create a primary key, of the pair of description (OS type) and timestamp
            db.execute(
                f"ALTER TABLE `{region}_{instance_type}` ADD CONSTRAINT pk PRIMARY KEY (Timestamp, ProductDescription)"
            )

            print(f"Wrote {region}_{instance_type}")

# Close the db connection
db.dispose()

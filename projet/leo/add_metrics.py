from pandas import DataFrame

from Objects.Version import Version


def add_metrics(df: DataFrame, version: Version) -> DataFrame:
    df["added_lines"] = 0
    df["deleted_lines"] = 0
    df["commit_count"] = 0
    df["commit_bug_count"] = 0
    df["commit_count_r"] = 0
    df["dev_count"] = 0
    df["dev_count_r"] = 0
    df["mean_time"] = 0
    df["mean_time_r"] = 0
    df["dev_mean_exp"] = 0
    df["dev_min_exp"] = 0
    df["commit_comment_changed"] = 0
    df["commit_comment_unchanged"] = 0

    for index, row in df.iterrows():
        file_name = row["Name"]
        if file_name in version.metrics["added_lines"]:
            df.at[index, "added_lines"] = version.metrics["added_lines"][file_name]

        if file_name in version.metrics["deleted_lines"]:
            df.at[index, "deleted_lines"] = version.metrics["deleted_lines"][file_name]

        if file_name in version.metrics["commit_count"]:
            df.at[index, "commit_count"] = version.metrics["commit_count"][file_name]

        if file_name in version.metrics["commit_bug_count"]:
            df.at[index, "commit_bug_count"] = version.metrics["commit_bug_count"][file_name]

        if file_name in version.metrics["commit_count_r"]:
            df.at[index, "commit_count_r"] = version.metrics["commit_count_r"][file_name]

        if file_name in version.metrics["dev_count"]:
            df.at[index, "dev_count"] = version.metrics["dev_count"][file_name]

        if file_name in version.metrics["dev_count_r"]:
            df.at[index, "dev_count_r"] = version.metrics["dev_count_r"][file_name]

        if file_name in version.metrics["mean_time"]:
            df.at[index, "mean_time"] = int(version.metrics["mean_time"][file_name])

        if file_name in version.metrics["mean_time_r"]:
            df.at[index, "mean_time_r"] = int(version.metrics["mean_time_r"][file_name])

        if file_name in version.metrics["dev_mean_exp"]:
            df.at[index, "dev_mean_exp"] = int(version.metrics["dev_mean_exp"][file_name])

        if file_name in version.metrics["dev_min_exp"]:
            df.at[index, "dev_min_exp"] = int(version.metrics["dev_min_exp"][file_name])

        if file_name in version.metrics["commit_comment_changed"]:
            df.at[index, "commit_comment_changed"] = version.metrics["commit_comment_changed"][file_name]

        if file_name in version.metrics["commit_comment_unchanged"]:
            df.at[index, "commit_comment_unchanged"] = version.metrics["commit_comment_unchanged"][file_name]

    return df

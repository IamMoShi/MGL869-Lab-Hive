import pydriller


def extract_data(commit: pydriller.Commit) -> dict:
    commit_dict = {}
    commit_dict['hash'] = commit.hash
    commit_dict['author'] = commit.author.name
    commit_dict['email'] = commit.author.email
    commit_dict['author_date'] = commit.author_date
    commit_dict['msg'] = commit.msg
    commit_dict['modified_files'] = []
    for modified_file in commit.modified_files:
        file = {}
        file['filename'] = modified_file.filename
        file['added_lines'] = modified_file.added_lines
        file['deleted_lines'] = modified_file.deleted_lines
        file['comments_changed'] = {'added': 0, 'deleted': 0}
        for n_line, line in modified_file.diff_parsed['added']:
            if "//" in line or "/*" in line:
                file['comments_changed']['added'] += 1
        for n_line, line in modified_file.diff_parsed['deleted']:
            if "//" in line or "/*" in line:
                file['comments_changed']['deleted'] += 1
        commit_dict['modified_files'].append(file)
    return commit_dict

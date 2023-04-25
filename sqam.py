import re

def split_sql_query(query):
    query = query.strip()
    
    # extract SELECT statement
    select_end = query.find(' FROM ')
    select_clause = query[:select_end] if select_end != -1 else query
    select_items = [item.strip() for item in select_clause.split('SELECT ')[-1].split(',')]

    # extract FROM statement
    from_start = select_end + 6 if select_end != -1 else 0
    from_end = query.find(' WHERE ') if ' WHERE ' in query else len(query)
    from_clause = query[from_start:from_end].strip()
    from_items = [item.strip() for item in from_clause.split(',')]

    # extract WHERE conditions
    where_start = from_end + 7 if ' WHERE ' in query else len(query)
    where_end = query.find(' GROUP BY ') if ' GROUP BY ' in query else len(query)
    where_clause = query[where_start:where_end].strip()
    where_items = [item.strip() for item in re.split(r'\s+(?:AND|OR)\s+', where_clause, flags=re.IGNORECASE)] if where_clause != '' else None
    
    # extract GROUP BY statement
    group_start = where_end + 10 if ' GROUP BY ' in query else len(query)
    group_end = query.find(' HAVING ') if ' HAVING ' in query else len(query)
    group_clause = query[group_start:group_end].strip()
    group_items = [item.strip() for item in group_clause.split(',') if item.strip()] if group_clause != '' else None
    
    # extract HAVING conditions
    having_start = group_end + 8 if ' HAVING ' in query else len(query)
    having_end = query.find(' ORDER BY ') if ' ORDER BY ' in query else len(query)
    having_clause = query[having_start:having_end].strip()
    having_items = [item.strip() for item in re.split(r'\s+(?:AND|OR)\s+', having_clause, flags=re.IGNORECASE)] if having_clause != '' else None
    
    # extract ORDER BY statement
    order_start = having_end + 10 if ' ORDER BY ' in query else len(query)
    order_end = len(query)
    order_clause = query[order_start:order_end].strip()
    order_items = [item.strip() for item in order_clause.split(',') if item.strip()] if order_clause != '' else None
    
    # return dictionary of subitems
    return {'SELECT': select_items, 'FROM': from_items, 'WHERE': where_items, 
            'GROUP BY': group_items, 'HAVING': having_items, 'ORDER BY': order_items}

def sql_query_accuracy(query, true_query):
    # split the queries into parts using the updated split_sql_query function
    query_parts = split_sql_query(query)
    true_query_parts = split_sql_query(true_query)

    # define the weights for each main query part
    weights = {'SELECT': 2, 'FROM': 1, 'WHERE': 3, 'GROUP BY': 2, 'HAVING': 2, 'ORDER BY': 1}

    # initialize the total and matching subitems counts
    total_count = 0
    matching_count = 0

    # iterate over the query parts and compare them with the true query parts
    for part_name, part_list in query_parts.items():
        true_part_list = true_query_parts.get(part_name, [])

        # calculate the weight for the current part
        weight = weights.get(part_name, 1)

        # skip the loop iteration if the part_list is None
        if part_list is None:
          if true_part_list is None:
            continue
          else:
            total_count += weight
            continue
        elif true_part_list is None:
          total_count += weight
          continue

        # iterate over the subitems in the query part and compare them with the true query part
        for subitem in set(part_list).union(set(true_part_list)):
            total_count += weight
            if subitem in true_part_list and subitem in part_list:
                matching_count += weight


    # calculate the accuracy score as the percentage of matching subitems
   
    if total_count == 0:
        accuracy_score = 0
    else:
        accuracy_score = matching_count / total_count * 100

    return accuracy_score
  
  
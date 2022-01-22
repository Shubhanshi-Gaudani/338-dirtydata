def toLower(cell_str,col):
    if col.column_type == 'alpha':
        return cell_str.lower()
    return cell_str
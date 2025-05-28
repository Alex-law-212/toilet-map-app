from your_module import connect_sheet

def add_comment(name, comment):
    sheet = connect_sheet()
    try:
        cell = sheet.find(name)
        row = cell.row
        current = sheet.cell(row, 6).value
        updated = f"{current} | {comment}" if current else comment
        sheet.update_cell(row, 6, updated)
    except Exception as e:
        raise ValueError(f"寫入留言失敗：{e}")

def get_comments(comment_str):
    return [c.strip() for c in comment_str.split("|") if c.strip()] if comment_str else []

from terminaltables import AsciiTable
def main():
    main_menu()

def main_menu():
        table_data = [
            ['Heading1', 'Heading2'],
            ['row1 column1', 'row1 column2'],
            ['row2 column1', 'row2 column2'],
            ['row3 column1', 'row3 column2']
        ]
        table = AsciiTable(table_data)
        print(table.table)

if __name__ == '__main__':
    main()
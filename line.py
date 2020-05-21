with open("ds.csv", "r") as file:
    first_line = file.readline()
    for last_line in file:
        pass
    latest_values=last_line.split(',')
    print(latest_values[1])
        
    usa_time=((latest_values[0].split())[1].split('-'))[0]
    if usa_time > "09:00:00" and usa_time < "16:00:00" :
        print("Market Closed. Showing MSFT stock values from last closing on "+(latest_values[0].split())[0]+" at "+usa_time+" NY local time.")
    # int()latest_values[5]="Market Open. Showing current trends at "+usa_time

    
    print(marketopen)
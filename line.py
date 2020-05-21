with open("ds.csv", "r") as file:
        recentvalues=[]
        for line in (file.readlines() [-2:]): 
            recentvalues.append(line)
        
        
        print(recentvalues)
        # latest_values=last_line.split(',')
        # latest_2ndvalues=last_line.split(',')
        
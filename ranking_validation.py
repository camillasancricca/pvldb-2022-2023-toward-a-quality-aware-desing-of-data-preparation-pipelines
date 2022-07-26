from scipy.integrate import simps

def compute_area(scores):
    area = 0
    for i in range(0,9):
        a = scores[i]
        b = scores[i+1]
        y = [a,b]
        area += simps(y, dx=10)
    return round(area,4)

def compute_area_raw(scores, raw):
    area = 0
    for i in range(0,9):
        a = scores[i]
        b = scores[i+1]
        y = [a,b]
        area += simps(y, dx=10)
    return round(area-raw,4)

def validation(name_dataset, name_algorithm, raw, first, second, third):

    with open(name_dataset+"_"+name_algorithm+"_validation.csv","w") as file:
        file.write("Dimension,EXP1,P1,EXP2,P2,EXP3,P3,EXP4,P4,EXP5,P5,EXP6,P6\n")

        areaR = compute_area(raw)

        P1 = [round((compute_area(first[0])-areaR)/(compute_area(third[0])-areaR)*100,2),round((compute_area(first[1])-areaR)/(compute_area(third[1])-areaR)*100,2),round((compute_area(first[2])-areaR)/(compute_area(third[2])-areaR)*100,2),
              round((compute_area(first[3])-areaR)/(compute_area(third[3])-areaR)*100,2),round((compute_area(first[4])-areaR)/(compute_area(third[4])-areaR)*100,2),round((compute_area(first[5])-areaR)/(compute_area(third[5])-areaR)*100,2)]

        P2 = [round((compute_area(second[0])-areaR)/(compute_area(third[0])-areaR)*100,2),round((compute_area(second[1])-areaR)/(compute_area(third[1])-areaR)*100,2),round((compute_area(second[2])-areaR)/(compute_area(third[2])-areaR)*100,2),
              round((compute_area(second[3])-areaR)/(compute_area(third[3])-areaR)*100,2),round((compute_area(second[4])-areaR)/(compute_area(third[4])-areaR)*100,2),round((compute_area(second[5])-areaR)/(compute_area(third[5])-areaR)*100,2)]

        P3 = [round((compute_area(third[0])-areaR)/(compute_area(third[0])-areaR)*100,2),round((compute_area(third[1])-areaR)/(compute_area(third[1])-areaR)*100,2),round((compute_area(third[2])-areaR)/(compute_area(third[2])-areaR)*100,2),
              round((compute_area(third[3])-areaR)/(compute_area(third[3])-areaR)*100,2),round((compute_area(third[4])-areaR)/(compute_area(third[4])-areaR)*100,2),round((compute_area(third[5])-areaR)/(compute_area(third[5])-areaR)*100,2)]

        file.write("First,"+str(compute_area(first[0]))+","+str(P1[0])+","
                   +str(compute_area(first[1]))+","+str(P1[1])+","
                   +str(compute_area(first[2]))+","+str(P1[2])+","
                   + str(compute_area(first[3])) + "," + str(P1[3]) + ","
                   + str(compute_area(first[4])) + "," + str(P1[4]) + ","
                   + str(compute_area(first[5])) + "," + str(P1[5])
                   +"\n")
        file.write("Second,"+str(compute_area(second[0]))+","+str(P2[0])+","
                   +str(compute_area(second[1]))+","+str(P2[1])+","
                   +str(compute_area(second[2]))+","+str(P2[2])+","
                   +str(compute_area(second[3]))+","+str(P2[3])+","
                   +str(compute_area(second[4]))+","+str(P2[4])+","
                   +str(compute_area(second[5]))+","+str(P2[5])
                   +"\n")
        file.write("Third,"+str(compute_area(third[0]))+","+str(P3[0])+","
                   +str(compute_area(third[1]))+","+str(P3[1])+","
                   +str(compute_area(third[2]))+","+str(P3[2])+","
                   +str(compute_area(third[2]))+","+str(P3[3])+","
                   +str(compute_area(third[2]))+","+str(P3[4])+","
                   +str(compute_area(third[2]))+","+str(P3[5])
                   +"\n")

def validation_2(name_dataset, name_algorithm, raw, first, second):

    with open(name_dataset+"_"+name_algorithm+"_validation.csv","w") as file:
        file.write("Dimension,EXP1,P1,EXP2,P2\n")

        areaR = compute_area(raw)

        P1 = [round((compute_area(first[0])-areaR)/(compute_area(second[0])-areaR)*100,2),round((compute_area(first[1])-areaR)/(compute_area(second[1])-areaR)*100,2)]
        P2 = [round((compute_area(second[0])-areaR)/(compute_area(second[0])-areaR)*100,2),round((compute_area(second[1])-areaR)/(compute_area(second[1])-areaR)*100,2)]

        file.write("First,"+str(compute_area(first[0]))+","+str(P1[0])+","
                   +str(compute_area(first[1]))+","+str(P1[1])
                   +"\n")
        file.write("Second,"+str(compute_area(second[0]))+","+str(P2[0])+","
                   +str(compute_area(second[1]))+","+str(P2[1])
                   +"\n")
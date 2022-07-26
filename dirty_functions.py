import pandas as pd
import numpy as np
import random

def out_of_range(minimum, maximum):
    foo = ["up", "down"]
    f = random.choice(foo)
    dist = maximum - minimum

    if f == "up":
        number = random.uniform(maximum, maximum + dist)
    else:
        number = random.uniform(minimum - dist, minimum)

    return number

def typo(message):
    # convert the message to a list of characters
    message = list(message)

    typo_prob = 0.2 # percent (out of 1.0) of characters to become typos

    # the number of characters that will be typos
    n_chars_to_flip = max(round(len(message) * typo_prob),1)
    # is a letter capitalized?
    capitalization = [False] * len(message)
    # make all characters lowercase & record uppercase
    for i in range(len(message)):
        capitalization[i] = message[i].isupper()
        message[i] = message[i].lower()

    # list of characters that will be flipped
    pos_to_flip = []
    for i in range(n_chars_to_flip):
        pos_to_flip.append(random.randint(0, len(message) - 1))

    # dictionary... for each letter list of letters
    # nearby on the keyboard
    nearbykeys = {
        'a': ['q','w','s','x','z'],
        'b': ['v','g','h','n'],
        'c': ['x','d','f','v'],
        'd': ['s','e','r','f','c','x'],
        'e': ['w','s','d','r'],
        'f': ['d','r','t','g','v','c'],
        'g': ['f','t','y','h','b','v'],
        'h': ['g','y','u','j','n','b'],
        'i': ['u','j','k','o'],
        'j': ['h','u','i','k','n','m'],
        'k': ['j','i','o','l','m'],
        'l': ['k','o','p'],
        'm': ['n','j','k','l'],
        'n': ['b','h','j','m'],
        'o': ['i','k','l','p'],
        'p': ['o','l'],
        'q': ['w','a','s'],
        'r': ['e','d','f','t'],
        's': ['w','e','d','x','z','a'],
        't': ['r','f','g','y'],
        'u': ['y','h','j','i'],
        'v': ['c','f','g','v','b'],
        'w': ['q','a','s','e'],
        'x': ['z','s','d','c'],
        'y': ['t','g','h','u'],
        'z': ['a','s','x'],
        ' ': ['c','v','b','n','m'],
        '1': ['q'],
        '2': ['q','w'],
        '3': ['w','e'],
        '4': ['e','r'],
        '5': ['r','t'],
        '6': ['t','y'],
        '7': ['y','u'],
        '8': ['u','i'],
        '9': ['i','o'],
        '0': ['o','p'],
    }

    # insert typos
    for pos in pos_to_flip:
        # try-except in case of special characters
        try:
            typo_arrays = nearbykeys[message[pos]]
            message[pos] = np.random.choice(typo_arrays)
        except:
            break

    # reinsert capitalization
    for i in range(len(message)):
        if (capitalization[i]):
            message[i] = message[i].upper()

    # recombine the message into a string
    message = ''.join(message)

    # show the message in the console
    #print(message)
    return message

def dirty_syn_accuracy(seed, name, name_class):

    np.random.seed(seed)

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #percentuale di errori
    perc = [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,1-p]

        for col in df_dirt.columns:
            #per evitare di cancellare le class
            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                if (df_dirt[col].dtype != "object"):
                    minimum = float(df_dirt[col].min())
                    maximum = float(df_dirt[col].max())
                    rand = np.random.choice([True, False], size=df_dirt.shape[0], p=comp)
                    selected = df_dirt.loc[rand == True,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = out_of_range(minimum, maximum)
                        t+=1
                else:
                    rand = np.random.choice([True, False], size=df_dirt.shape[0], p=comp)
                    selected = df_dirt.loc[rand == True,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = typo(str(i))
                        t+=1

                df_dirt.loc[rand == True,col]=selected

        df_list.append(df_dirt)
        print("saved {}-syn_accuracy{}%".format(name, round((1-p)*100)))
    return df_list

def dirty_sem_accuracy(seed, name, name_class):

    np.random.seed(seed)

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #percentuale di errori
    perc = [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,1-p]
        for col in df_dirt.columns:
            #per evitare di cancellare le class
            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                domain = list(df_dirt[col].unique())
                rand = np.random.choice([True, False], size=df_dirt.shape[0], p=comp)
                selected = df_dirt.loc[rand == True,col]
                t=0
                for i in selected:
                    temp = domain.copy()

                    if len(temp)!=1:
                        temp.remove(i)

                    selected[t:t+1] = random.choice(temp)
                    t+=1

                df_dirt.loc[rand == True,col]=selected

        df_list.append(df_dirt)
        print("saved {}-sem_accuracy{}%".format(name, round((1-p)*100)))
    return df_list

def dirty_completeness(seed, name, name_class):

    np.random.seed(seed)

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #percentuale di null
    perc = [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,1-p]
        for col in df_dirt.columns:
            #per evitare di cancellare le class
            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                rand = np.random.choice([True, False], size=df_dirt.shape[0], p=comp)

                df_dirt.loc[rand == True,col]=np.nan

        df_list.append(df_dirt)
        print("saved {}-completeness{}%".format(name, round((1-p)*100)))
    return df_list

def dirty_all(seed, name, name_class):
    np.random.seed(seed)

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #percentuale di null
    perc = [0.30, 0.27, 0.24, 0.21, 0.18, 0.15, 0.12, 0.09, 0.06, 0.03]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,p,p,1-p*3]
        for col in df_dirt.columns:

        #1: completeness, 2: semantic, 3: syntactic, 0: no error

            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                rand = np.random.choice([1, 2, 3, 0], size=df_dirt.shape[0], p=comp)

                #completeness
                df_dirt.loc[rand == 1,col]=np.nan

                #semantic
                domain = list(df_dirt[col].unique())
                selected = df_dirt.loc[rand == 2,col]
                t=0
                for i in selected:
                    temp = domain.copy()

                    if len(temp)!=1:
                        temp.remove(i)

                    selected[t:t+1] = random.choice(temp)
                    t+=1

                df_dirt.loc[rand == 2,col]=selected

                #syntactic
                if (df_dirt[col].dtype != "object"):
                    minimum = float(df_dirt[col].min())
                    maximum = float(df_dirt[col].max())
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = out_of_range(minimum, maximum)
                        t+=1
                else:
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = typo(str(i))
                        t+=1

                df_dirt.loc[rand == 3,col]=selected

        df_list.append(df_dirt)
        print("saved {}-all{}%".format(name, round((p)*100)))
    return df_list

def dirty_consistency(seed, name, name_class, columns_indexes):

    np.random.seed(seed)

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #save the names of the attributes to dirt in consistency
    name_columns = []
    for i in columns_indexes:
        name_columns.append(df_pandas.columns[i])

    #percentuale di errori
    perc = [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,1-p]
        for col in df_dirt.columns:
            #per evitare di cancellare le class
            if col!=name_class and col in name_columns:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')


                domain = list(df_dirt[col].unique())
                rand = np.random.choice([True, False], size=df_dirt.shape[0], p=comp)
                selected = df_dirt.loc[rand == True,col]
                t=0
                for i in selected:
                    temp = domain.copy()

                    if len(temp)!=1:
                        temp.remove(i)
                    selected[t:t+1] = random.choice(temp)
                    t+=1

                df_dirt.loc[rand == True,col]=selected

        df_list.append(df_dirt)
        print("saved {}-consistency{}%".format(name, round((1-p)*100)))
    return df_list


def dirty_all_with_return(seed, name, name_class):
    np.random.seed(seed)
    mask = []

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #percentuale di null
    perc = [0.30, 0.27, 0.24, 0.21, 0.18, 0.15, 0.12, 0.09, 0.06, 0.03]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,p,p,1-p*3]
        for col in df_dirt.columns:

            #1: completeness, 2: semantic, 3: syntactic, 0: no error

            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                rand = np.random.choice([1, 2, 3, 0], size=df_dirt.shape[0], p=comp)
                mask.append(rand)

                #completeness
                df_dirt.loc[rand == 1,col]=np.nan

                #semantic
                domain = list(df_dirt[col].unique())
                selected = df_dirt.loc[rand == 2,col]
                t=0
                for i in selected:
                    temp = domain.copy()

                    if len(temp)!=1:
                        temp.remove(i)

                    selected[t:t+1] = random.choice(temp)
                    t+=1

                df_dirt.loc[rand == 2,col]=selected

                #syntactic
                if (df_dirt[col].dtype != "object"):
                    minimum = float(df_dirt[col].min())
                    maximum = float(df_dirt[col].max())
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = out_of_range(minimum, maximum)
                        t+=1
                else:
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = typo(str(i))
                        t+=1

                df_dirt.loc[rand == 3,col]=selected

        df_list.append(df_dirt)
        print("saved {}-all{}%".format(name, round((p)*100)))
    return [df_list,mask]

def dirty_consistency_with_return(seed, name, name_class, columns_indexes):

    np.random.seed(seed)
    mask = []
    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #save the names of the attributes to dirt in consistency
    name_columns = []
    for i in columns_indexes:
        name_columns.append(df_pandas.columns[i])

    #percentuale di errori
    perc = [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,1-p]
        for col in df_dirt.columns:
            #per evitare di cancellare le class
            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                if col in name_columns:
                    domain = list(df_dirt[col].unique())
                    rand = np.random.choice([True, False], size=df_dirt.shape[0], p=comp)
                    mask.append(rand)
                    selected = df_dirt.loc[rand == True,col]
                    t=0
                    if len(domain)!=1:
                        for i in selected:
                            temp = domain.copy()
                            temp.remove(i)
                            selected[t:t+1] = random.choice(temp)
                            t+=1

                        df_dirt.loc[rand == True,col]=selected
                else:
                    mask.append(np.random.choice([True, False], size=df_dirt.shape[0], p=[0,1]))

        df_list.append(df_dirt)
        print("saved {}-consistency{}%".format(name, round((1-p)*100)))
    return [df_list,mask]

def dirty_sem_accuracy_with_return(seed, name, name_class):

    np.random.seed(seed)
    mask = []

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #percentuale di errori
    perc = [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,1-p]
        for col in df_dirt.columns:
            #per evitare di cancellare le class
            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                domain = list(df_dirt[col].unique())
                rand = np.random.choice([True, False], size=df_dirt.shape[0], p=comp)
                mask.append(rand)
                selected = df_dirt.loc[rand == True,col]
                t=0
                for i in selected:
                    temp = domain.copy()

                    if len(temp)!=1:
                        temp.remove(i)

                    selected[t:t+1] = random.choice(temp)
                    t+=1

                df_dirt.loc[rand == True,col]=selected

        df_list.append(df_dirt)
        print("saved {}-sem_accuracy{}%".format(name, round((1-p)*100)))
    return [df_list,mask]

def dirty_all_with_return_consistency(seed, name, name_class, columns_indexes):
    np.random.seed(seed)
    mask = []

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #save the names of the attributes to dirt in consistency
    name_columns = []
    for i in columns_indexes:
        name_columns.append(df_pandas.columns[i])

    #percentuale di errori
    perc = [0.30, 0.27, 0.24, 0.21, 0.18, 0.15, 0.12, 0.09, 0.06, 0.03]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,p,p,1-p*3]
        for col in df_dirt.columns:

            #1: completeness, 2: consistency, 3: syntactic, 0: no error

            if col!=name_class:
                rand = np.random.choice([1, 2, 3, 0], size=df_dirt.shape[0], p=comp)
                mask.append(rand)

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                #completeness
                df_dirt.loc[rand == 1,col]=np.nan

                #consistency
                if col in name_columns:
                    domain = list(df_dirt[col].unique())
                    selected = df_dirt.loc[rand == 2,col]
                    t=0
                    if len(domain)!=1:
                        for i in selected:
                            temp = domain.copy()
                            temp.remove(i)
                            selected[t:t+1] = random.choice(temp)
                            t+=1

                        df_dirt.loc[rand == 2,col]=selected

                #syntactic
                if (df_dirt[col].dtype != "object"):
                    minimum = float(df_dirt[col].min())
                    maximum = float(df_dirt[col].max())
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = out_of_range(minimum, maximum)
                        t+=1
                else:
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = typo(str(i))
                        t+=1

                df_dirt.loc[rand == 3,col]=selected

        df_list.append(df_dirt)
        print("saved {}-all{}%".format(name, round((p)*100)))
    return [df_list,mask]

def dirty_all_without_consistency(seed, name, name_class):
    np.random.seed(seed)

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #save the names of the attributes to dirt in consistency

    #percentuale di errori
    perc = [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,p,1-p*2]
        for col in df_dirt.columns:

            #1: completeness, 3: syntactic, 0: no error

            if col!=name_class:
                rand = np.random.choice([1, 3, 0], size=df_dirt.shape[0], p=comp)

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                #completeness
                df_dirt.loc[rand == 1,col]=np.nan

                #syntactic
                if (df_dirt[col].dtype != "object"):
                    minimum = float(df_dirt[col].min())
                    maximum = float(df_dirt[col].max())
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = out_of_range(minimum, maximum)
                        t+=1
                else:
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = typo(str(i))
                        t+=1

                df_dirt.loc[rand == 3,col]=selected

        df_list.append(df_dirt)
        print("saved {}-all{}%".format(name, round((p)*100)))
    return df_list

def dirty_all_with_return_without_consistency(seed, name, name_class):
    np.random.seed(seed)
    mask = []

    #%%

    file_path = name + "/" + name + ".csv"
    df_pandas = pd.read_csv(file_path)
    df_list = []

    #percentuale di null
    perc = [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05]
    for p in perc:
        df_dirt = df_pandas.copy()
        comp = [p,p,1-p*2]
        for col in df_dirt.columns:

            #1: completeness, 3: syntactic, 0: no error

            if col!=name_class:

                if (df_dirt[col].dtype == "bool"):
                    df_dirt[col]=df_dirt[col].astype('object')

                rand = np.random.choice([1, 3, 0], size=df_dirt.shape[0], p=comp)
                mask.append(rand)

                #completeness
                df_dirt.loc[rand == 1,col]=np.nan

                #syntactic
                if (df_dirt[col].dtype != "object"):
                    minimum = float(df_dirt[col].min())
                    maximum = float(df_dirt[col].max())
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = out_of_range(minimum, maximum)
                        t+=1
                else:
                    selected = df_dirt.loc[rand == 3,col]
                    t=0
                    for i in selected:
                        selected[t:t+1] = typo(str(i))
                        t+=1

                df_dirt.loc[rand == 3,col]=selected

        df_list.append(df_dirt)
        print("saved {}-all{}%".format(name, round((p)*100)))
    return [df_list,mask]
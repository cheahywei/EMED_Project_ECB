import os
import sys
import pandas as pd

#testing add new branch in github
#file path
fp_ECB_DefFiles   = r"M:\Database\EuroStat\08_ECB_DefFiles"

#file name
fn_ECB_masterdec   = "ECB_MasterDef.xlsx"

def main():
    
    #load fn_ECB_masterdec as pd.DataFrame
    df_master_def         = pd.read_excel(os.path.join(fp_ECB_DefFiles, fn_ECB_masterdec))

    #get the unique value from the column Concept
    #these unique value is used to get the column header from the souce file
    list_concept  = df_master_def["Concept"].unique().tolist()

    #get the unique value from column Concept
    try:
        #df_sourcefile = pd.read_csv(os.path.join(fp_ECB_DefFiles, "data.csv"))
        df_sourcefile = pd.read_csv("data.csv")
    except FileNotFoundError as error:
        print(error)
        print(("Source file is not found. Make sure the source file name is data.csv"))
        input("Press Enter to Exit the program...")
        sys.exit()

    #create an empty DataFrame
    df_uniquevalue = pd.DataFrame()
    
    #loop the columns in the df_sourcefile
    for each_column in df_sourcefile.columns:
        print(each_column)
        #if the columns is matching with the unique value from the column Concept
        if each_column in list_concept:
            #get the list of the unqiue value from the matched columns
            df_sourcefile[each_column] = df_sourcefile[each_column].astype(str)
            df_temp_uniquevalue       = df_sourcefile[each_column].drop_duplicates()
            df_temp                   = pd.DataFrame({"HEADER": each_column,
                                                      "VALUE" : df_temp_uniquevalue,
                                                      "STATUS": "Y"})
            #concat the all unqiue value into df
            df_uniquevalue            = pd.concat([df_uniquevalue, df_temp])
    
    
    #convert the data type from object to string
    df_master_def["Code"] = df_master_def["Code"].astype(str)

    df_uniquevalue = pd.merge(df_uniquevalue, df_master_def, 
                              how      = "left",
                              left_on  = ["HEADER", "VALUE"],
                              right_on = ["Concept", "Code"],
                              sort     = False)

    #drop extra column
    df_uniquevalue.drop(columns = ["Concept description", "Concept", "Codelist", "Code"], inplace = True)
    
    
    #export the dataframe as excel
    df_uniquevalue.to_excel("Temp_Def.xlsx", index_label = False, index = False)

if __name__ == "__main__":
    
    main()



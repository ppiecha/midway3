def loc_var(v):
    match v:
        case int():
            print("int")
        case float():
            print("float")


loc_var(3)
loc_var(3.0)
loc_var("3")

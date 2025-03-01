W,L,N = 0,0,0
while True:
    user = input("Enter 1 2 or 3 to add to the W L N tally:\n")
    if user == "1":
        W += 1
        print("W:", W)
    elif user == "2":
        L += 1
        print("L:", L)
    elif user == "3":
        N += 1
        print("N:", N)
    elif user == "result":
        print("W:", W)
        print("L:", L)
        print("N:", N)
    elif user == "reset":
        W,L,N = 0,0,0
        print("Resetting W, L, N to 0")
    elif user == "count":
        user2 = input("Enter a string of W's, L's, and N's to count:\n")
        for i in user2:
            if i == "W":
                W += 1
            elif i == "L":
                L += 1
            elif i == "N":
                N += 1
            else:
                continue
        print("W:", W, "L:", L, "N:", N)
        total: int = W + L + N
        print("Total:", total)
        W *= 2
        L *= -1
        sum = W + L + N
        print("Sum:", sum)
        W,L,N = 0,0,0
        
    elif user == "big":
        user2 = input("Enter a string of W's, L's, and N's to count:\n")
        for i in range(len(user2)):
            if user2[i] == "W":
                W += int(user2[i-1])
            elif user2[i] == "L":
                L += int(user2[i-1])
            elif user2[i] == "N":
                N += int(user2[i-1])
            else:
                continue
        print("W:", W, "L:", L, "N:", N)
        total: int = W + L + N
        print("Total:", total)
        W *= 2
        L *= -1
        sum = W + L + N
        print("Sum:", sum)
        W,L,N = 0,0,0
    elif user == "exit":
        break
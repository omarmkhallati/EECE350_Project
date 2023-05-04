# Client_1
import socket # Import Socket Module
try:
    
    client_Socket = socket.socket() # Initialize Client Socket
    serverPort = 12000 # Set Server Port
    client_Socket.connect(('127.0.0.1', serverPort)) # Connect Client Socket To Server
    message = client_Socket.recv(1024).decode() # Recieve Message From Server
    
    if "Enter the number of players:" in message: # Check If This Is The First Client To Connect
        players = int(input('Enter the number of players: ')) # Get The Number Of Players
        client_Socket.send(str(players).encode()) # Send The Number Of Players To The Server
        while(players <= 1): # If Players Are Less Than One
            players = int(input('Enter the number of players: ')) # Input The Number Of Players
            client_Socket.send(str(players).encode()) # Send The Number Of Players
            
    else: # Else
        print('Waiting for other players...') # Wait For Other Players
        print("") # Print Space For Display
        
    name = client_Socket.recv(1024).decode() # Create Name Variable
    if (name== "\nUnable to continue game due to non-activity for a long time."):   #took the player toolong to respond
        print(name)
        client_Socket.close()
    name = input("Enter your name: ") # Ask User To Input Name
    client_Socket.send(name.encode()) # Send User Name To Server
    rematch = "yes" # Set Rematch To Yes
    
    while(rematch == "yes" or rematch == "YES" or rematch == "Yes"): # If Users Wanted To Rematch
        i=0 # Set Variable To 0 
        
        while(i<3): # Increment Loop For Rounds
            number = client_Socket.recv(1024).decode() # Recieve Number From Server
            
            if (number== "\nUnable to continue game due to unexpected reasons." or number == "\nUnable to continue game due to non-activity for a long time."): # If There Was An Error
                print(number) # Print Error
                client_Socket.close() # Close Client Socket
                break # Break The Loop
            
            if ( number == "The game has ended ! You had fun right ?"): # If There Was An Error
                print(number) # Print Error
                client_Socket.close() # Close Client Socket
                break # Break The Loop
            
            print("\nInput the number on the screen as fast as possible ! " + number) # Send Number To User So They Can Write
            
            try:
                x = int(input("Enter the number : ")) # Take Number As Input
                
            except:
                x = 10 # Numbers Are Between 0 And 10
                
            print("\n") # Print Space For Display
            client_Socket.send(repr(x).encode()) # Send Number The User Inputted To The Server
            i = i + 1 # Increment Rounds
            c = client_Socket.recv(1024).decode() # Current Round Scores
            t = client_Socket.recv(1024).decode() # Total Round Scores
            lines = client_Socket.recv(1024).decode() # Lines For Display
            
            if (c == "\nUnable to continue game due to unexpected reasons." or c == "\nUnable to continue game due to non-activity for a long time."): # If Error From Server
                print(c) # Print Error
                break # Break
            
            if (t== "\nUnable to continue game due to unexpected reasons." or t == "\nUnable to continue game due to non-activity for a long time."): # If Error From Server 
                print(t) # Print Error
                break # Break
            
            if (lines== "\nUnable to continue game due to unexpected reasons." or lines == "\nUnable to continue game due to non-activity for a long time."): # If Error From Server
                print(lines) # Print Error
                break # Break
            
            print("") # Print Space For Display
            print("              Round",i,"Results ") # Print Round Number
            print("") # Print Space For Display
            print(c) # Print Current Round Scores
            print("") # Print Space For Display
            print(t) # Print Total Round Scores
            print(lines) # Print Lines For Display    
        
        if (number== "\nUnable to continue game due to unexpected reasons."): break
        if (c== "\nUnable to continue game due to unexpected reasons."): break
        if (t== "\nUnable to continue game due to unexpected reasons."): break
        if (lines== "\nUnable to continue game due to unexpected reasons."): break
        winnert = client_Socket.recv(1024).decode() # Total Game Winner
        winnert = "\n" + winnert # Add Space For Display
        print(winnert) # Print Total Winner
        message = client_Socket.recv(1024).decode() # Recieve Message From Server
        
        if (message == "The game has ended ! You had fun right ?"): # If Message From Server
            print("\nThe game has ended ! You had fun right ?") # Print Message
            break # Break
        print('Message from server:', message) # Print Message From Server
        
        if(message == "\nUnable to continue game due to unexpected reasons." or message == "\nUnable to continue game due to non-activity for a long time."): # If Message From Server
            print(message) # Print Message
            break # Break
        
        answer = input('Do you?:  ') # Ask If Client Wants Rematch
        rematch = answer # Recieve Answer From Client 
        client_Socket.send(answer.encode()) # Send Answer To Server
        message = client_Socket.recv(1024).decode() # Recieve Message From Server
        
        if message != "yes": # No Rematch
            print("\nThe game has ended ! You had fun right ?") # Print End Message Of Game
            break # Break Loop
        
except: 
    print("\nUnable to continue game due to unexpected reasons or non-activity for a long time on one of the players' side") # Error Message
    
client_Socket.close()
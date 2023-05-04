# Server

import pygame

pygame.init()
pygame.mixer.music.load("Background Music.mp3")
pygame.mixer.play()

def assign_scores(players_list, num_of_players):   #Defining a function to sort the players_list based on their scores and assign a rank to each player
   
    sorted_list = sorted(players_list, key=lambda x: x[2])  # Sort the players_list based on their RTTs and assigning a rank to each player based on their position in the sorted list
    for i in range(len(players_list)):
        if i==0:
            previous = sorted_list[0][2]
            sorted_list[0][1] = num_of_players-1
        
        else:
            if(sorted_list[i][2] == previous):
            
                previous = sorted_list[i][2]
                sorted_list[i][1] = sorted_list[i-1][1]
                                
            else:
                previous = sorted_list[i][2]
                sorted_list[i][1] = players-1-i
       
    for i in range(len(players_list)):
        if sorted_list[i][2] == float('inf'):
            sorted_list[i][1] = 0
         
    return sorted_list


import socket # Importing the neccessary libraries
import time
import random

server_Socket = socket.socket() #Creating a socket object for the server
serverPort = 12000 #Assigning a port number
server_Socket.bind(('127.0.0.1', serverPort)) #Binding the socket to the IP address and port number

server_Socket.listen(1)  # Listen on a port of your own choice for incoming connections
print("The server is ready to receive on port 12000.")

rematch = "yes"
Total = []  # Initializing variables
Current = []
Connection_Sockets = []
error = ""
c = ""  #for the current score message
t = ""  #for the total score message
winnert = ""

try:
    # # Initializing the players list with 16 binary numbers representing players in the game
    Players = ["0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101",
               "1110", "1111"]
    Total.append(["0000", 0, 0, " "]) # Appending the first element to the total and current lists, with an initial score of 0 and a blank name
    Current.append(["0000", 0, 0, " "])
    connection_Socket1, addr = server_Socket.accept() # Accepting the first connection from the client and appending it to the list of connection sockets
    Connection_Sockets.append(connection_Socket1) #add the first connection socket to the connection sockets list
    Connection_Sockets[0].settimeout(40)  # set the timeout of the connection socket to 40

    message = "Enter the number of players:" # Sending the message to the clients
    Connection_Sockets[0].send(message.encode())
    players = int(Connection_Sockets[0].recv(1024).decode()) # Receiving the number of players from the client

    while (players <= 1): # Ensuring that the number of players is at least 2
        players = int(Connection_Sockets[0].recv(1024).decode())

    if players > 16: players = 16 # Limiting the number of players to 16

    for i in range(players - 1): # Initializing the rest of the players in the game by creating connection sockets
        Total.append([Players[i], 0, 0, " "])    #tag-score-RTT-name
        Current.append([Players[i], 0, 0, " "])
        connection_Socket1, addr = server_Socket.accept()
        connection_Socket1.settimeout(40)    
        Connection_Sockets.append(connection_Socket1)

    for i in range(players): # Prompting each player to enter their name and updating their names in current and total lists
        message = "Enter your name: "
        if i != 0: Connection_Sockets[i].send(message.encode())
        
        Connection_Sockets[i].send(message.encode())
        name = Connection_Sockets[i].recv(1024).decode()
        Total[i][3] = name
        Current[i][3] = name

except socket.timeout: #if timeout elapsed without getting an answer from one of the players, assume game error and end the game
    print("")
    error = "\nUnable to continue game due to non-activity for a long time." 
    while i<len(Connection_Sockets):               #send the error message to each player
        try:
            Connection_Sockets[i].send(error.encode())
            Connection_Sockets[i].close()
            i=i+1#should display a message
        except:
            i = i+1
            
    print(error)        #print the error on the server side
    rematch="no"        #end the game

except:
    print("")
    error = "\nUnable to continue game due to unexpected reasons."  # If there was any error from the client side or from the server side, the proxy server
    i = 0
    while i < len(Connection_Sockets):
        try:
            Connection_Sockets[i].send(error.encode())
            Connection_Sockets[i].close()
            i = i + 1  # should display a message
        except:
            i = i + 1

    print(error)
    rematch = "no"

while (rematch == "yes" or rematch == "YES" or rematch == "Yes"):
    # Initialization

    for i in range(players): # starting or Restarting the game 
        Total[i][1] = 0
    rounds = 0
    
    while (rounds < 3):  #3 rounds
        Current = sorted(Current, key=lambda x: x[0])   #sort the lists 
        Total = sorted(Total, key=lambda x: x[0])

        try:        # Checking for each player if the answer is correct and getting RTT
        
            for i in range (0,players):
              
               x = random.randint(0,9)  #generate a random number between 0 and 9
               Start = time.time()  # Starting the time just after getting the random number
              
                   
               Connection_Sockets[i].send(str(x).encode())   # Sending the number to the player 
               data = Connection_Sockets[i].recv(1024).decode()   # Receiving the answer of this player
               End = time.time()    # End the time
               data = int(data)     #make the data received an integer to be able to compare
               
               
               if (x == data):      #player inputs the correct number
                       RTT= End - Start     # Getting the roundtrip time (period) in which the number was sent and received 
                       Current[i][2] = RTT    # Storing its value in the current array for the corresponding player
                       Total[i][2] = RTT      # Storing its value in the total array
            
               else:        #wrong number, RTT will be infinity (bigger than all other RTTs -> score 0)
                       Current[i][2] = float('inf')
                       Total[i][2] = float('inf')
                       Current[i][1] = 0

            Current = assign_scores(Current, players) # Assigning each player to his/her score
            Total = sorted(Total, key=lambda x: x[2]) #sort the total list according to RTTs  (compare RTTs)
            
            for i in range (len(Current)):
                Total[i][1] = Total[i][1] + Current[i][1]     #update the total list (score part)
            
            
            Sorted_Current = sorted(Current, key=lambda x: x[1],reverse = True) #sort the current list based on scores in decreasing order   
            Sorted_Total = sorted(Total, key=lambda x: x[1], reverse= True) #sort the total list based on scores in decreasing order
            
            #Displaying the results
            
            i=0
            j=0
            while (i<players): 
                currentscore = "Current scores: "+Sorted_Current[i][3]+" : "+str(Sorted_Current[i][1]) #the first time printing a current score
                currentscore2 = "                "+Sorted_Current[i][3]+" : "+str(Sorted_Current[i][1]) #for printing the other current scores
                if(j==0):  #if this is the first time
                    c = c + currentscore + "\n"   
                else:  
                    c = c + currentscore2 + "\n"
                #c is the string containing the current results to be displayed
                j=j+1
                i=i+1
            
            j=0
            i=0
            while (i<players):
                totalscore = "Total scores:   "+Sorted_Total[i][3]+" : "+str(Sorted_Total[i][1]) # for the first time printing a total score
                totalscore2 = "                "+Sorted_Total[i][3]+" : "+str(Sorted_Total[i][1]) #for printing the other total scores
                if(j==0): #if this is the first time
                    t = t + totalscore + "\n"
                else:
                    t = t + totalscore2 + "\n"
                #t is the string containing the total results to be displayed  
                j=j+1
                i=i+1
                
            lines = "_________________________________________________________________________________"  #to seperate rounds
            
            #print
            print("")
            print("              Round",rounds,"Results ")
            print("")
            print(c)
            print("")
            print(t)
            print(lines)
            
            for k in range(players): Connection_Sockets[k].send(c.encode())  # send the current results to all the players 
            for k in range(players): Connection_Sockets[k].send(t.encode())  # send the total results to all the players
            for k in range(players): Connection_Sockets[k].send(lines.encode())
            
            #clear c and t for the next round
            c=""
            t=""
            rounds=rounds+1 #let's go for the next round!
            
        except socket.timeout: #if timeout elapsed without getting an answer from one of the players, assume game error and end the game
            print("")
            error = "\nUnable to continue game due to non-activity for a long time." 
            while i<len(Connection_Sockets):               #send the error message to each player
                try:
                    Connection_Sockets[i].send(error.encode())
                    Connection_Sockets[i].close()
                    i=i+1#should display a message
                except:
                    i = i+1
                    
            print(error)        #print the error on the server side
            rematch="no"        #end the game
            
        except:
             print("")
             error = "\nUnable to continue game due to unexpected reasons." #If there was any error from the client side or from the server side, the game server should display a message
             i=0
             while i<players:
                 try:
                     Connection_Sockets[i].send(error.encode())       #send the error message to each player
                     Connection_Sockets[i].close()            #close each connection sockets to end the game
                     i=i+1
                 except:
                     i = i+1
             print(error)      #display the error on the server side
             break                                
    
    
    if (error == "\nUnable to continue game due to unexpected reasons."): break  #in case of any error break from the loop of the game       
    
    #AFTER FINISH THE 3 ROUNDS
    winner=0
    tie=0

    try:
        while(winner<players):
            if(Sorted_Total[winner][1] == Sorted_Total[0][1]): #check for a tie with the first detected winner
                if (tie>0):  #if there is any tie in the final scores 
                    print("")
                    winner_to_send = "Tied with:"+Sorted_Total[winner][3]+" with a score of: "+str(Sorted_Total[winner][1])+" as well"  #saving the display format of the other winner
                    print(winner_to_send)   #print the second winner
                    winnert = winnert + winner_to_send 
                else:    #no tie
                    print("")
                    winner_to_send = "And the winner is:"+Sorted_Total[winner][3]+" with a score of: "+str(Sorted_Total[winner][1])   #saving the display format of the winner
                    print(winner_to_send) 
                    winnert = winnert + winner_to_send
                    tie = tie+1   #add the current tie
                
                Congrats = "\n          Congratulations to "+str(Sorted_Total[winner][3])   #congratulation message
                winnert = winnert + "\n"+ Congrats + "\n"
                print("\n          Congratulations to ",Sorted_Total[winner][3])
            winner = winner +1    #go to the next player
             
        
        if (error == "\nUnable to continue game due to unexpected reasons."): break   #in case of any error break from the loop of the game 
    
        for k in range(players): Connection_Sockets[k].send(winnert.encode())    #send the final results to each player
        
        #clean everything
        winnert=""          
        rematching = 0
        rematch="yes"
        
        #Ask for a rematch (another play, same players (no need to connect again))
        while(rematching <players):   #enter the loop till the server asked every player
            message = 'Do you wish for a rematch?'
            Connection_Sockets[rematching].send(message.encode())    #send the question to player
            maybeRematch = Connection_Sockets[rematching].recv(1024).decode()   #save the answer received
            
            if (maybeRematch != "yes" and maybeRematch != "YES" and maybeRematch != "Yes" ):  #if one player doesn't want to play again
                rematch = "no"
                message = "no"
              
                Connection_Sockets[rematching].send(message.encode())
                
                Connection_Sockets.remove(Connection_Sockets[rematching])     #remove the player's corresponding connection socket from the connection socket list
                
                for i in range(len(Connection_Sockets)):
                    message = "The game has ended ! You had fun right ?"       #end game message
                    print(" ")
                    Connection_Sockets[i].send(message.encode())
                    Connection_Sockets[i].close()           #close every connection socket to officially end the game
                    
                break    # game ended, no need to ask other players
                server_Socket.close()   #close the server socket
                    
                
            else:
                message ="yes"
                Connection_Sockets[rematching].send(message.encode())
                
                
            rematching = rematching + 1     #ask the next player if he/she wants a rematch
    
            
    except socket.timeout: #if timeout elapsed without getting an answer from one of the players, assume game error and end the game
        print("")
        error = "\nUnable to continue game due to non-activity for a long time." 
        while i<len(Connection_Sockets):               #send the error message to each player
            try:
                Connection_Sockets[i].send(error.encode())
                Connection_Sockets[i].close()
                i=i+1#should display a message
            except:
                i = i+1
                
        print(error)        #print the error on the server side
        rematch="no"        #end the game
        
    except:
         print("")
         error = "\nUnable to continue game due to unexpected reasons." #If there was any error from the client side or from the server side, the game server should display a message
         i=0
         while i<players:
             try:
                 Connection_Sockets[i].send(error.encode())       #send the error message to each player
                 Connection_Sockets[i].close()            #close each connection sockets to end the game
                 i=i+1
             except:
                 i = i+1
         print(error)      #display the error on the server side
         break                                 
    
                  
server_Socket.close()     #officially end the game

from settings import *
from Mastermind import *

class Server(MastermindServerTCP):
    def __init__(self):
        '''
        Create an instance of the Server class which initializes the timeouts
        of connections, positions of both players, score of both players,
        Datasend, ball position and possession of ball.
        '''
        MastermindServerTCP.__init__(self, 0.5,0.5,10.0) #server refresh, connections' refresh, connection timeout

        self.DataSend = []
        self.player1pos = [0]
        self.player2pos = [0]
        self.ballpos = []
        self.player1posession, self.player2posession = True, False
        self.player1ballpos, self.player2ballpos = [],[]
        self.lastball = 1
        self.player1Score, self.player2Score = 0,0

    def callback_connect          (self                                          ):
        '''
        Called when the server connects i.e., when .connect(...) is successful.

        Returns:
        '''
        return super(Server,self).callback_connect()
    def callback_disconnect       (self                                          ):
        '''
        Called when the server disconnects i.e., when .disconnect(...) is
        called.

        Returns:
        '''
        return super(Server,self).callback_disconnect()
    def callback_connect_client   (self, connection_object                       ):
        '''
        Called when a new client connects.
        The argument "connection_object" represents the appropriate connection.

        Returns:
        '''
        return super(Server,self).callback_connect_client(connection_object)
    def callback_disconnect_client(self, connection_object                       ):
        '''
        Called when a client disconnects.
        The argument "connection_object" represents the appropriate connection.

        Returns:
        '''
        return super(Server,self).callback_disconnect_client(connection_object)

    def callback_client_receive   (self, connection_object                       ):
        '''
        Called when data is about to be received from a connection.
        The argument "connection_object" represents the appropriate connection.

        Returns:
        '''

        return super(Server,self).callback_client_receive(connection_object)
    def callback_client_handle    (self, connection_object, data                 ):
        """
        Called to handle data received from a connection.
        The argument "connection_object" represents the appropriate connection.
        Receives data from each player as a list of
        [ playernumber, player 1 position, player 2 position,
        possession of the ball, ball position and score ]
        """

        #If the data is from player 1, store the data in player1 variables
        if data[0] == 1:
            self.player1pos = data[1:3]
            self.player1posession = data[3]
            self.player1ballpos = data[4:6]
            self.player1Score = data[6]

        #If the data is from player 2, store the data in player2 variables
        else:
            self.player2pos = data[1:3]
            self.player2posession = data[3]
            self.player2ballpos = data[4:6]
            self.player2Score = data[6]

        # Check for the posession of the ball from each player and update the ball
        #   depending on who is posessing the ball.
        # If both of them are posessing the ball, it determines who the ball belongs
        #   to by looking at who had the ball last time.
        if self.player1posession == True and self.player2posession == True:
            if self.lastball == 1:
                self.ballpos = self.player2ballpos
            else:
                self.ballpos = self.player1ballpos
        elif self.player2posession == True:
            self.ballpos = self.player2ballpos
            self.lastball = 2
        elif self.player1posession == True:
            self.ballpos = self.player1ballpos
            self.lastball = 1
        elif self.player1posession == False and self.player2posession == False:
            if self.lastball == 1:
                self.ballpos = self.player1ballpos
            else:
                self.ballpos = self.player2ballpos

        # Append the data of both players to send
        self.DataSend=[self.player1pos,self.player2pos, self.ballpos, self.player1Score, self.player2Score]

        # Send Data
        self.callback_client_send(connection_object, self.DataSend)

    def callback_client_send      (self, connection_object, data,compression=None):
        '''
        Called to when data is about to be sent to a connection. If sending
        fails, the connection is silently terminated.
        The argument "data" is the data that the server is about to send to the
        connection.
        The argument "compression" determines whether the data should be
        compressed before sending.

        Returns:
        '''
        return super(Server,self).callback_client_send(connection_object, data, compression)

if __name__ == "__main__":
    server = Server()
    server.connect(server_ip,port)
    print("Start Server...")
    try:
        server.accepting_allow_wait_forever()
    except:
        #Only way to break is with an exception
        pass
    print("Ending Server...")
    server.accepting_disallow()
    server.disconnect_clients()
    server.disconnect()

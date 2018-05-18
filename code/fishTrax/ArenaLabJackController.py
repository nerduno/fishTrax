# general libraries
import os, sys, time, copy
import numpy as np

# libraries used in StreamDataReader
import struct, threading, Queue, ctypes

# Labjack libraries
import LabJackPython, u6

# TCP/IP communication 
import socket

# Logging
import logging, jsonlogger, json

# time functions
from time import sleep
from datetime import datetime

#---------------------------------------------------------------------------------------------------

class ThreadedLogger( threading.Thread ):

    def __init__(self, json_logger, in_queue = None):
        super( ThreadedLogger, self ).__init__()

        # Setup logger & queueing
        self.json_logger = json_logger
        self.in_queue = in_queue

        # Simple flags
        self._should_shutdown = False
        self.recording = False
        
    # --- Public methods --- #

    def add_tasks(self, tasks):
        """
        Callable method to add tasks to the input queue.
        The syntax of tasks and how they are run is left to self._do_tasks().
        """
        if self.in_queue is None:
            self.in_queue = Queue.Queue()            
        for i in xrange(len(tasks)):
            self.in_queue.put(tasks[i])
        
    def log(self, data, object_type='standard'):
        """
        Callable logging method that puts data in queue in a dictionary with
        timestamp, data, data type, and object type.
        """
        try:
            self.json_logger.log(data, object_type)
        except Exception, e:
            print "!!!!!!!!! Logging failed !!!!!!!!!"
            print type(e), e
        
    def run(self):
        """
        Run method called by threading.Thread(*args).start()
        """
        while self._should_shutdown is False:

            # get data and add to the logger
            self._get_data()

            # do all tasks in in_queue
            self._do_tasks()

        self._cleanup()

    def shutdown( self ):
        self._should_shutdown = True
        self.join()
        print 'Labjack thread exiting gracefully.'
                    
    # --- Private Methods --- # 

    def _cleanup(self):
        """
        Abstract method for cleaning at the end of a run.
        """
        pass

    def _do_tasks(self):
        """
        Abstract method for getting task from in_queue and executing. 
        """
        print "Not doing any tasks."

    def _get_data(self):
        """
        Abstract method for getting data and putting in the logger.
        """
        pass

#---------------------------------------------------------------------------------------------------

class LabjackLogger( ThreadedLogger ):

    def __init__(self, config_file, json_logger,in_queue=None):
        super(LabjackLogger, self).__init__(json_logger, in_queue)

        # get recording configuration
        self._load_configuration( config_file )

        # Setup channels and logfile
        # Setup channels to be recorded and the logfile
        print "Setting up channels and logging:"
        self.log('Setting up channels and logging:', 'info')
        
        if self.streaming:
            print "\t---> Streaming addresses:", self._streaming_addresses
            self.log('Streaming addresses:' + str(self._streaming_addresses), 'info')
            self._initialize_streaming()
        else:
            self.log('Initialized Labjack', 'info')
            self.labjack = u6.U6()
        if self.analog:
            print "\t---> Analog addresses:", self._analog_addresses
            self.log('Analog addresses' + str(self._analog_addresses), 'info')
            self._initialize_analog()
        if self.digital:
            print "\t---> Digital addresses:", self._digital_addresses
            self.log('Digital addresses ' + str(self._digital_addresses), 'info')
            self._initialize_digital()

        self.log('Generating logfile', 'info')

        print "\t---> Setup complete."
        self.log('Setup complete', 'info')
        
    def execute_task( self, task ):
        if task['mode'] == 'read':
            self.log( {'task':task, 'output':self.labjack.readRegister(task['register']) }, 'labjack_task' )
        elif task['mode'] == 'write':
            self.labjack.writeRegister(task['register'], task['write_value'])
            self.log( {'task':task, 'output':None }, 'labjack_task')
        else:
            self.log({'ValueError':'Mode of task was not recognized', 'value':task}, 'error')
       
    # ---- Private Methods ---- #

    def _cleanup( self ):
        """
        Close threads and labjack on exit.
        """
        self.sdr.running = False
        self.sdrThread.join()
        self.labjack.close()

    def _do_tasks(self):
        """
        Loop over input queue, running any tasks found.
        Tasks here are dictionaries containing a mode (either 'read' or 'write')
        and a register number (from the Labjack Modbus Map) for reading mode,
        or a mode, a register number, and a value to write to the register for writing mode. 
        """
        if self.in_queue is not None:
            while self.in_queue.empty() is False:
                print "----------------in queue has tasks! ------------------"
                task = self.in_queue.get()
                if task['mode'] == 'read':
                    self.log( {'task':task, 'output':self.labjack.readRegister(task['register']) }, 'labjack_task' )
                elif task['mode'] == 'write':
                    #from plugins.parameters import argon
                    #print '%10.10f' % argon.time
                    self.labjack.writeRegister(task['register'], task['write_value'])
                    self.log( {'task':task, 'output':None }, 'labjack_task')
                else:
                    self.log({'ValueError':'Mode of task was not recognized', 'value':task}, 'error')

    def _get_data(self):
        """
        Get stream data and place in the output queue. 
        """
        self.log( self._get_stream_block(), 'labjack_stream' )

    def _get_stream_block( self ):
        # Pull results out of the Queue in a blocking manner.
        errors = 0
        missed = 0

        try:
            # Pull results out of the streaming data reader queue in a blocking manner.
            result = self.sdr.data.get(True, 1)

            # If there were errors, print as much.
            if result['errors'] != 0:
                errors += result['errors']
                missed += result['missed']
                print "+++++ Total Errors: %s, Total Missed: %s" % (errors, missed)

            # Convert the raw bytes (result['result']) to voltage data.
            r = self.labjack.processStreamData(result['result'])
            #print "---- Got streaming data! ----"
            return r

        except Queue.Empty:
            print "Labjack streaming queue is empty."
            pass

    def _initialize_analog( self ):
        """
        Sets up the analog Labjack connections.
        """
        for i in range( len(self._analog_addresses) ):
            chan_id = range_check(self._analog_addresses[i], [0,5999])
            if chan_id >= 5000:
                self.labjack.writeRegister(chan_id, 0.0)

    def _initialize_digital( self, init_low=True ):
        """
        Sets up the digital Labjack connections.
        """
        for i in range( len(self._digital_addresses) ):
            chan_id = range_check(self._digital_addresses[i], [6000,6199])
            if init_low:
                self.labjack.writeRegister(chan_id, 0)
            else:
                self.labjack.writeRegister(chan_id, 1)

    def _initialize_streaming( self ):
        """
        Initialize Labjack for streaming mode and set up connections.
        """
        # At high frequencies ( >5 kHz), the number of samples will be max_packets
        # times 48 (packets per request) times 25 (samples per packet)
        self._num_samples = self._max_packets*48*25 # is this used anymore?

        # initialize LabJack U6 device
        self.labjack = u6.U6()
        self.log( 'Labjack opened.', 'info')
        
        # For applying the proper calibration to readings
        self.labjack.getCalibrationData()

        # configure stream
        print "\t---> Configuring U6 stream..."
        self.log( 'Configuring U6 stream...', 'info')
        self.labjack.streamConfig( NumChannels = self._num_analog_channels,
                                   ChannelNumbers = range(self._num_analog_channels),
                                   ChannelOptions = [0]*self._num_analog_channels,
                                   SettlingFactor = 1,
                                   ResolutionIndex = 1,
                                   SampleFrequency = self._sampling_rate )

        # get stream reader
        self.sdr = StreamDataReader(self.labjack, max_packets=self._max_packets)
        self.sdrThread = threading.Thread(target = self.sdr.readStreamData)

        # Start the stream and begin loading the result into a Queue
        self.sdrThread.start()
        
    def _load_configuration( self, config_file ):
        """
        This method parses the configuration file that specifyies which addresses
        should be logged, as well as settings for these addresses.
        
        In particular it looks for 3 sections in the configuration file:
        'streaming', 'analog', and 'digital', corresponding to
        streaming, analog, and digital signal sampling from the Labjack.

        If a section is present, additional settings related to the particular
        mode of recording are also searched for and loaded if present. 
        """
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        if len(config.sections()) == 0:
            print 'ERROR: Could not initialize labjack.  Found no addresses in file', config_file
            raise SystemExit
            
        # Check which modes of recording will be used,
        # and if a mode is present, load the relevant settings. 
        if config.has_section('streaming'):
            self.streaming = True
            self._streaming_addresses = parse_address_string( config.get('streaming', 'addresses') )
            self._max_packets = int(config.get('streaming', 'max_packets'))
            self._sampling_rate = int(config.get('streaming', 'sampling_rate'))
            self._num_analog_channels = int(config.get('streaming', 'num_analog_channels'))
        else:
            self.streaming = False

        if config.has_section('analog'):
            self.analog = True
            self._analog_addresses = parse_address_string( config.get('analog', 'addresses') )
        else:
            self.analog = False

        if config.has_section('digital'):
            self.digital = True
            self._digital_addresses = parse_address_string( config.get('digital', 'addresses') )
        else:
            self.digital = False

# Helper functions

def parse_address_string( address_string ):
    return  [int(i) for i in address_string.split(',')]

def range_check(val, desired_range):
    if val >= min(desired_range) and val <= max(desired_range):
        return val
    else:
        raise ValueError('Channel '+str(val)+' is not in range '+str(desired_range))

#---------------------------------------------------------------------------------------------------

class StreamDataReader(object):
    """
    Threaded streaming of blocks of analog data off the Labjack.
    """
    def __init__( self, device, max_packets = None ):
        self.device = device
        if max_packets is not None:
            self.max_packets = max_packets
        else:
            self.max_packets = 1e6
        self.data = Queue.Queue()
        self.dataCount = 0
        self.missed = 0
        self.running = False

    def readStreamData(self):
        self.running = True
        start = datetime.now()
        self.device.streamStart()
        while self.running:
            returnDict = self.device.streamData(convert = False).next() # converted later
            self.data.put_nowait(copy.deepcopy(returnDict))
            self.dataCount += 1
            if self.dataCount > self.max_packets:
                self.running = False
        
        print "Labjack has stopped streaming data."
        self.device.streamStop()
        stop = datetime.now()
        total = ( self.dataCount * self.device.packetsPerRequest *
                  self.device.streamSamplesPerPacket )
        print "%s requests with %s packets per request with %s samples per packet = %s samples total." % ( self.dataCount,
                                                                                                           self.device.packetsPerRequest,
                                                                                                           self.device.streamSamplesPerPacket,
                                                                                                           total )
        
        print "%s samples were lost due to errors." % (self.missed)
        total -= self.missed
        print "Adjusted number of samples = %s" % (total)
        
        runTime = (stop-start).seconds + float((stop-start).microseconds)/1000000
        print "The experiment took %s seconds." % (runTime)
        print ( "%s samples / %s seconds = %s Hz" %
                ( total, runTime, float(total)/runTime ) )

#---------------------------------------------------------------------------------------------------
# Unit tests

def test_LabjackLogger():
    """
    Unit test for LabjackLogger class.
    """
    # Get configuration file
    config_path = '/Users/logang/Documents/Data/labjack_config.cfg'

    # Instantiate LabjackLogger and test simple logging
    labjack_logger = LabjackLogger(config_path)
    labjack_logger.log('Test standard logging.')

    # --- Make some tasks
    tasks = []
    
    # read-only analog task
    tasks.append( { 'mode':'read', 'register':10 } )
 
    # read-write analog tasks
    tasks.append( { 'mode':'read', 'register':5000 } )
    tasks.append( { 'mode':'write', 'register':5000, 'write_value':1.5 } )
    tasks.append( { 'mode':'read', 'register':5000 } )

    # read-write digital tasks
    tasks.append( { 'mode':'read', 'register':6000 } )
    tasks.append( { 'mode':'write', 'register':6000, 'write_value':1 } )
    tasks.append( { 'mode':'read', 'register':6000 } )

    # Add the tasks to the input queue
    labjack_logger.add_tasks(tasks)

    # Run threaded logging
    labjack_logger.start()

    time.sleep(1) # wait a sec

    # Exit and save to logfile
    labjack_logger.shutdown()
    1/0

#---------------------------------------------------------------------------------------------------
# Main

if __name__ == '__main__':
    test_LabjackLogger()

#---------------------------------------------------------------------------------------------------
# EOF

# class TCPLogger( ThreadedLogger ):

#     def __init__(self, options, queue):
#         # set options
#         super(TCPLogger, self).__init__()
#         self.outfile = options.outfile
#         self.config_file = options.config_file
#         self.queue = queue

#         # get addresses
#         self._load_configuration( config_file )

#         # list container
#         self.socket_cxns = []

#         # Setup channels and logfile
#         self.initialize()
        
#     # ---- Public Methods ---- #

#     def exit( self ):
#         """
#         Cleans up and closes all connections.
#         """
#         # clean up socket connections
#         self._cleanup()

#         # exit
#         raise SystemExit # what is the best way to exit more gracefully?

#     def initialize( self ):
#         """
#         Callable method to reinitialize labjack and start a new logfile.
#         """
#         # Setup channels to be recorded and logfile
#         print "Setting up channels and logging:"
#         print "\t---> TCP/IP addresses:", self.socket_addresses
#         self.setup_channels()
#         self.setup_logging()
#         print "\t---> Setup complete."

#     def log( self ):
#         """
#         Convert dictionary objects returned in data properties to json, add time and date information, 
#         and write to log file. 
#         """
#         pass

#     def run( self ):
#         """
#         Main run method for Labjack Logger. Loops over all provided addresses,
#         reading data and writing data_objects to dictionaries, and these
#         dictionaries to a json log.
#         """
#         # Start recording
#         print "Recording..."
#         while True:
#             try:
#                 if self.streaming:
#                     self.log( self.stream_data )
#                 if self.analog:
#                     self.log( self.analog_data )
#                 if self.digital:
#                     self.log( self.digital_data )
#                     self.recording = not self._check_for_interrupt( self.digital_data )
#                 if self.sockets:
#                     self.log( self.socket_data )
#                     self.recording = not self._check_for_interrupt( self.socket_data )
#                 if self.recording is False:
#                     break
#             except KeyboardInterrupt:
#                 self.recording = False
#                 break
#             except Exception, e:
#                 print type(e), e
#                 self.recording = False
#                 break
#             finally:
#                 self._cleanup()

#     def setup_channels(self):
#         """
#         Setup channels to be recorded and logging.
#         """
#         # setup channels that will be recorded from
#         if self.streaming:
#             self._initialize_streaming()
#         if self.analog:
#             self._initialize_analog()
#         if self.digital:
#             self._initialize_digital()
#         if self.sockets:
#             self._initialize_sockets()

#     def setup_logging(self):
#         """
#         Setup logging. 
#         """
#         pass

#     @property
#     def socket_data(self):
#         return self._get_socket_data()

#     @property
#     def stream_data(self):
#         return self._get_stream_block()

#     # ---- Private Methods ---- #

#     def _check_for_interrupt(self, in_list, interrupt=sys.maxint):
#         """
#         Checks through a list for an interrupt signal, returning
#         True if one is found.
#         """
#         for i in xrange(len(in_list)):
#             if in_list[i] == interrupt:
#                 return True
#             else:
#                 return False
        
#     def _cleanup( self ):
#         """
#         Closes socket connections and resets Labjack to default state.
#         """
#         self._close_socket_connections()
#         self._reset_labjack_to_default()

#     def _close_socket_connections( self ):
#         """
#         Close all socket TCP connections.
#         """
#         for i in range( len(self.socket_cnxs) ):
#             self.socket_cnxs[i].close()

#     def _get_connection(self, port_num):
#         """
#         Start a TCP server that listens for connections from clients,
#         and return this connection.
#         """
#         # Create a TCP socket
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#         # Bind the socket to the port
#         server_address = ('localhost', port_num)
#         print 'Starting server at' % server_address
#         sock.bind(server_address)

#         # Listen for incoming connection
#         sock.listen(1)
#         while True:
#             # Wait for connection
#             if self.debug:
#                 print '\t---> ...waiting for a connection'
#             connection, client_address = sock.accept()


#             if self.debug:
#                 print '\t---> received connection from', client_address

#             # Handshake
#             while True:
#                 data = connection.recv(16)
#                 if data:
#                     self.run_event(data)
#                     if data == 1415:
#                         print '\t---> andshaking with client ', client_address
#                     connection.sendall(data)
#                     return connection
#                 else:
#                     if self.debug:
#                         print 'No data from', client_address
#                     break
                
#     def _get_analog_data(self):
#         pass

#     def _get_digital_data(self):
#         pass
    
#     def _get_socket_data(self):
#         pass

#     def _get_stream_block( self ):
#         # Pull results out of the Queue in a blocking manner.
#         result = self.sdr.data.get(True, 1)

#         # If there were errors, print as much.
#         if result['errors'] != 0:
#             errors += result['errors']
#             missed += result['missed']
#             print "+++++ Total Errors: %s, Total Missed: %s" % (errors, missed)

#         # Return the raw bytes (result['result']) converted  to voltage data.
#         return self.labjack.processStreamData(result['result'])

#     def _initialize_analog( self ):
#         """
#         Sets up the analog Labjack connections.
#         """
#         for i in range( len(self._analog_addresses) ):
#             chan_id = range_check(self._analog_addresses[i], [0,5999])
#             if chan_id >= 5000:
#                 self.labjack.writeRegister(chan_id, 0.0)

#     def _initialize_digital( self, init_low=True ):
#         """
#         Sets up the digital Labjack connections.
#         """
#         for i in range( len(self._digital_addresses) ):
#             chan_id = range_check(self._digital_addresses[i], [6000,6199])
#             if init_low:
#                 self.labjack.writeRegister(chan_id, 0)
#             else:
#                 self.labjack.writeRegister(chan_id, 1)

#     def _initialize_sockets(self):
#         """
#         Sets up the socket connections and puts them in self.sockets.
#         """
#         for i in range( len(self._socket_addresses) ):
#             chan_id = self._socket_addresses[i]
#             self.socket_cnxs.append( self._get_connection( chan_id ) )

#     def _initialize_streaming( self ):
#         """
#         Initialize Labjack for streaming mode and set up connections.
#         """
#         # At high frequencies ( >5 kHz), the number of samples will be max_packets
#         # times 48 (packets per request) times 25 (samples per packet)
#         self._num_samples = self._max_packets*48*25 # is this used anymore?

#         # initialize LabJack U6 device
#         self.labjack = u6.U6()
    
#         # For applying the proper calibration to readings
#         self.labjack.getCalibrationData()

#         # configure stream
#         print "\---> Configuring U6 stream..."
#         self.labjack.streamConfig( NumChannels = self._num_analog_channels,
#                                    ChannelNumbers = range(self._num_analog_channels),
#                                    ChannelOptions = [0]*self._num_analog_channels,
#                                    SettlingFactor = 1,
#                                    ResolutionIndex = 1,
#                                    SampleFrequency = self._sampling_rate )

#         # get stream reader
#         self.sdr = StreamDataReader(self.labjack, max_packets=self._max_packets)
#         self.sdrThread = threading.Thread(target = self.sdr.readStreamData)

#         # output list
#         self.out = []
#         self.out_arr = None
        
#     def _load_configuration( self, config_file ):
#         """
#         This method parses the configuration file that specifyies which addresses
#         should be logged, as well as settings for these addresses.
        
#         In particular it looks for 4 sections in the configuration file:
#         'streaming', 'analog', 'digital', and 'socket', corresponding to
#         streaming, analog, and digital signal sampling from the Labjack,
#         and TCP/IP signals via the socket library, respectively.

#         If a section is present, additional settings related to the particular
#         mode of recording are also searched for and loaded if present. 
#         """
#         import ConfigParser
#         config= ConfigParser.ConfigParser()
#         config.read(config_file)
#         if len(config.sections()) == 0:
#             print 'Found no addresses in file', config_file
#             sys.exit(1)
            
#         # Check which modes of recording will be used,
#         # and if a mode is present, load the relevant settings. 
#         if config.has_section('streaming'):
#             self.streaming = True
#             self._streaming_addresses = parse_address_string( config.get('streaming', 'addresses') )
#             self._max_packets = config.get('streaming', 'max_packets')
#             self._sampling_rate = config.get('streaming', 'sampling_rate')
#             self._num_analog_channels = config.get('streaming', 'num_analog_channels')
#         else:
#             self.streaming = False

#         if config.has_section('analog'):
#             self.analog = True
#             self._analog_addresses = parse_address_string( config.get('analog', 'addresses') )
#         else:
#             self.analog = False

#         if config.has_section('digital'):
#             self.digital = True
#             self._digital_addresses = parse_address_string( config.get('digital', 'addresses') )
#         else:
#             self.digital = False

#         if config.has_section('sockets'):
#             self.sockets = True
#             self._socket_addresses = parse_address_string( config.get('sockets', 'addresses') )
#         else:
#             self.sockets = False

#     def _reset_labjack_to_default(self):
#         pass

# def parse_address_string( address_string ):
#     return  [int(i) for i in address_string.split(',')]

# def range_check(val, desired_range):
#     if val >= min(desired_range) and val <= max(desired_range):
#         return val
#     else:
#         raise ValueError('Channel '+str(val)+' is not in range '+str(desired_range))

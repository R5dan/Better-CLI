import logging
import sys

class TogglableDebugLogger:
    def __init__(self, logger_name="bettercli", default_level=logging.INFO):
        # Create logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(default_level)
        
        # Create handlers
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.file_handler = logging.FileHandler('debug.cl.log')
        
        # Create formatters and add it to handlers
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console_handler.setFormatter(log_format)
        self.file_handler.setFormatter(log_format)
        
        # Add handlers to the logger
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)
        
        # Store the default level for toggling
        self.default_level = default_level
        
    def enable_debug(self):
        """Enable debug logging"""
        self.logger.setLevel(logging.DEBUG)
        self.console_handler.setLevel(logging.DEBUG)
        self.file_handler.setLevel(logging.DEBUG)
        self.logger.debug("Debug logging enabled")
        
    def disable_debug(self):
        """Disable debug logging and return to default level"""
        self.logger.debug("Debug logging disabled")
        self.logger.setLevel(self.default_level)
        self.console_handler.setLevel(self.default_level)
        self.file_handler.setLevel(self.default_level)
        
    def get_logger(self):
        """Return the logger instance"""
        return self.logger
    
    def enable_file_logging(self):
        """Enable file logging"""
        self.logger.addHandler(self.console_handler)
        self.file_handler.setLevel(logging.DEBUG)
        self.logger.debug("File logging enabled")
    
    def disable_file_logging(self):
        """Disable file logging and return to default level"""
        self.logger.removeHandler(self.file_handler)
        self.file_handler.setLevel(self.default_level)
        self.logger.debug("File logging disabled")

    def enable_console_logging(self):
        """Enable console logging"""
        self.logger.addHandler(self.file_handler)
        self.console_handler.setLevel(logging.DEBUG)
        self.logger.debug("Console logging enabled")

    def disable_console_logging(self):
        """Disable console logging and return to default level"""
        self.logger.removeHandler(self.console_handler)
        self.console_handler.setLevel(self.default_level)
        self.logger.debug("Console logging disabled")
"""
Custom email backend to handle SSL certificate issues on macOS
"""
import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class CustomEmailBackend(SMTPBackend):
    """
    Custom SMTP backend that creates an unverified SSL context.
    This fixes the "unable to get local issuer certificate" error on macOS.
    """
    
    def open(self):
        """
        Override open() to use unverified SSL context
        """
        if self.connection:
            return False
        
        connection_params = {}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout
        if self.use_ssl:
            connection_params['context'] = ssl._create_unverified_context()
        
        try:
            self.connection = self.connection_class(
                self.host, self.port, **connection_params
            )
            
            # TLS/STARTTLS
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls(context=ssl._create_unverified_context())
                self.connection.ehlo()
            
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            
            return True
        except Exception as e:
            if not self.fail_silently:
                raise


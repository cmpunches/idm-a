from configparser import ConfigParser


class IDMA_Conf:
    def __init__(self, conf_path ):
        ini_parser = ConfigParser(interpolation=None)
        ini_parser.read( conf_path )

        self.database = dict()
        self.email = dict()
        self.orientation = dict()
        self.session = dict()
        self.user_security = dict()
        self.administration = dict()

        self.database['user']   = ini_parser.get('database', 'user')
        self.database['pass']   = ini_parser.get('database', 'pass')
        self.database['host']   = ini_parser.get('database', 'host')
        self.database['dbname'] = ini_parser.get('database', 'name')

        self.email['server']    = ini_parser.get('email', 'server')
        self.email['port']      = ini_parser.get('email', 'port')
        self.email['user']      = ini_parser.get('email', 'user')
        self.email['password']  = ini_parser.get('email', 'password')
        self.email['sender']    = ini_parser.get('email', 'sender')

        self.orientation['backend_uri'] = ini_parser.get( 'orientation', 'backend_uri' )
        self.orientation['site_name'] = ini_parser.get( 'orientation', 'site_name' )

        self.session['TTL'] = ini_parser.get( 'sessions', 'TTL' )

        self.user_security['email_pattern'] = ini_parser.get( 'user_security', 'email_regex' )
        self.user_security['username_pattern'] = ini_parser.get( 'user_security', 'username_regex' )
        self.user_security['password_pattern'] = ini_parser.get( 'user_security', 'password_regex' )
        self.user_security['name_pattern'] = ini_parser.get( 'user_security', 'name_regex')

        self.administration['admin_group'] = ini_parser.get( 'administration', 'admin_group' )
